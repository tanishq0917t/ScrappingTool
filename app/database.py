import json
from .MongoConnection import MongoCollection
from .caching import Cache

class LocalStorage:
    def __init__(self, file_path: str = "products.json"):
        self.collection = MongoCollection().getCollection()
        self.cache = Cache()

    def load_data(self):
        print("Loading Data.......................")
        documents = self.collection.find({}, {"_id": 0})
        data = {doc["product_title"]: doc for doc in documents}
        for product_title, doc in data.items():
            self.cache.set(product_title, json.dumps(doc))
        print(f"Loaded {len(data)} products")

    def save_data(self, data):
        for item in data:
            self.collection.update_one(
                {"product_title": item["product_title"]},
                {"$set": item},
                upsert=True
            )

    def update_data(self, products):
        for product in products:
            product_title = product["product_title"]
            self.collection.update_one(
                {"product_title": product_title},
                {"$set": product}
            )
