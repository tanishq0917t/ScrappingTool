from pymongo import MongoClient
from pymongo.server_api import ServerApi
from urllib.parse import quote_plus
from bson.objectid import ObjectId
import json

class MongoCollection:
    _instance=None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def getCollection(cls):
        with open("config.json","r") as config:
            data=json.load(config)
        username = data['username']
        password = data['password']
        cluster = data['clusterID']
        db=data['db']
        collectionName=data['collection']

        encoded_username = quote_plus(username)
        encoded_password = quote_plus(password)
        uri=f"mongodb+srv://{encoded_username}:{encoded_password}@{cluster}.mongodb.net/"

        client = MongoClient(uri, server_api=ServerApi('1'))

        db=client[db]
        collection=db[collectionName]
        return collection
