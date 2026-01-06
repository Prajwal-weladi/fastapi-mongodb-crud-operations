from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client["crud_db"]

item_collection = db["items"]
