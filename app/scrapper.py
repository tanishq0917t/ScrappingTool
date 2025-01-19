import requests
from bs4 import BeautifulSoup
from time import sleep

class Scraper:
    def __init__(self, base_url: str, proxy: str = None, retries: int = 3, delay: int = 5):
        self.base_url = base_url
        self.proxy = proxy
        self.retries = retries
        self.delay = delay

    def scrape_page(self, page_number: int):
        url = f"{self.base_url}?page={page_number}"
        print(url)
        for attempt in range(self.retries):
            try:
                response = requests.get(
                    url,
                    proxies={"http": self.proxy, "https": self.proxy} if self.proxy else None,
                    timeout=10,
                )
                # print(response.text)
                response.raise_for_status()
                print("Calling parser")
                return self.parse_products(response.text)
            except requests.RequestException:
                sleep(self.delay)
        return []

    def parse_products(self, html: str):
        print()
        print()
        soup = BeautifulSoup(html, "html.parser")
        all_products=[]
        products = soup.select("li.product.type-product")

        for product in products:
            title_elem = product.select_one(".woo-loop-product__title a")
            product_title = title_elem.text.strip() if title_elem else "No title"

            price_elem = product.select_one(".price .woocommerce-Price-amount")
            product_price = price_elem.text.strip() if price_elem else "No price"

            img_elem = product.select_one(".mf-product-thumbnail img")
            product_image = img_elem["src"] if img_elem and "src" in img_elem.attrs else "No image"

            print("Title:",product_title)
            print("Price:",product_price[1:])
            all_products.append({
                    "product_title": product_title,
                    "product_price": product_price[1:],
                    "product_image": product_image,
                })

        return all_products
