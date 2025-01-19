import json

class LocalStorage:
    def __init__(self, file_path: str = "products.json"):
        self.file_path = file_path

    def load_data(self):
        try:
            with open(self.file_path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def save_data(self, data):
        with open(self.file_path, "w") as f:
            json.dump(data, f, indent=4)
