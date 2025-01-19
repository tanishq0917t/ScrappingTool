'''
This is one idea, not developed completely.
'''



from fastapi import APIRouter, Depends, Query
from app.auth import authenticate
from app.scrapper import Scraper
from app.database import LocalStorage
from app.caching import Cache
from concurrent.futures import ThreadPoolExecutor, as_completed

router = APIRouter()

@router.post("/scrape")
def scrape(
    base_url: str = Query(..., description="Base URL to scrape from"),
    pages: int = Query(5, description="Number of pages to scrape"),
    proxy: str = Query(None, description="Proxy string for scraping"),
):
    print(f"Base URL: {base_url}")
    scraper = Scraper(base_url=base_url, proxy=proxy)
    storage = LocalStorage()
    cache = Cache()

    scraped_products = []
    existing_data = {item["product_title"]: item for item in storage.load_data()}

    # for page in range(1, pages + 1):
    #     for product in scraper.scrape_page(page):
    #         cached_price = cache.get(product["product_title"])
    #         print("----------------")
    #         print(cached_price)
    #         if cached_price and float(cached_price) == product["product_price"]:
    #             continue

    #         cache.set(product["product_title"], product["product_price"])
    #         if product["product_title"] not in existing_data:
    #             scraped_products.append(product)
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(scraper.scrape_page, page): page for page in range(1, pages + 1)}

        for future in as_completed(futures):
            page = futures[future]
            try:
                products = future.result()  
                print(f"Page {page} scraped successfully.")
                for product in products:
                    cached_price = cache.get(product["product_title"])
                    if cached_price and float(cached_price) == product["product_price"]: continue
                    cache.set(product["product_title"], product["product_price"])

                    

            except Exception as e:
                print(f"Error scraping page {page}: {e}")

    storage.save_data(scraped_products)
    print(f"Scraped {len(scraped_products)} new products.")
    return {"scraped_products": len(scraped_products)}
