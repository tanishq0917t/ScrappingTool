from fastapi import APIRouter, Depends, Query
from app.auth import authenticate
from app.scrapper import Scraper
from app.database import LocalStorage
from app.caching import Cache
import json

router = APIRouter()
storage = LocalStorage()
storage.load_data()

@router.post("/scrape")
def scrape(
    base_url: str = Query(..., description="Base URL to scrape from"),
    pages: int = Query(..., description="Number of pages to scrape"),
    proxy: str = Query(None, description="Proxy string for scraping"),
):
    print(f"Base URL: {base_url}")
    if base_url == None or pages == None or pages == 0:
        return {"Usage":'curl -X POST "http://127.0.0.1:8000/scrape?base_url={target_url}&pages={number_of_pages}" -H "token: {static_token}"'}

    if base_url[-1]=='/':
        base_url=base_url[0:-1]
    scraper = Scraper(base_url=base_url, proxy=proxy)
    cache = Cache()

    scraped_products = []
    update_required=[]
    

    for page in range(1, pages + 1):
        for product in scraper.scrape_page(page):
            cached_data = cache.get(product["product_title"])
            if cached_data==None: #adding new product
                cache.set(product["product_title"], json.dumps(product))
                scraped_products.append(product)
            else:
                cached_data=json.loads(cached_data)
                if cached_data['product_price'] != product["product_price"]: #updating product
                    cache.set(product["product_title"], json.dumps(product))
                    update_required.append(product)

    storage.save_data(scraped_products)
    storage.update_data(update_required)
    print(f"Scraped {len(scraped_products)} new products.")
    return {"scraped_products": len(scraped_products),"updated_products":len(update_required)}
