from fastapi import APIRouter, Depends, Query
from app.auth import authenticate
from app.scrapper import Scraper
from app.database import LocalStorage
from app.caching import Cache

router = APIRouter()
storage = LocalStorage()
existing_data = storage.load_data()

@router.post("/scrape")
def scrape(
    base_url: str = Query(..., description="Base URL to scrape from"),
    pages: int = Query(5, description="Number of pages to scrape"),
    proxy: str = Query(None, description="Proxy string for scraping"),
):
    print(f"Base URL: {base_url}")
    if base_url[-1]=='/':
        base_url=base_url[0:-1]
    scraper = Scraper(base_url=base_url, proxy=proxy)
    cache = Cache()

    scraped_products = []
    
    print(len(existing_data))

    for page in range(1, pages + 1):
        for product in scraper.scrape_page(page):
            cached_price = cache.get(product["product_title"])
            if cached_price and cached_price == product["product_price"]:
                print("Continuing")
                continue

            cache.set(product["product_title"], product["product_price"])
            if product["product_title"] in existing_data:
                del existing_data[product["product_title"]]
            scraped_products.append(product)
            print("Adding")
            print(f"Cached: {cached_price}   |   Price: {product['product_price']}")
            existing_data[product["product_title"]]=product

    storage.save_data(scraped_products)
    print(f"Scraped {len(scraped_products)} new products.")
    return {"scraped_products": len(scraped_products)}
