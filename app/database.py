import json
from .MongoConnection import MongoCollection

class LocalStorage:
    def __init__(self, file_path: str = "products.json"):
        self.collection=MongoCollection().getCollection()

    def load_data(self):
        print("Loading Data.......................")
        documents = self.collection.find({}, {"_id": 0})
        return {doc["product_title"]: doc for doc in documents}

    def save_data(self, data):
        for item in data:
            self.collection.update_one(
                {"product_title": item["product_title"]},
                {"$set": item},
                upsert=True
            )