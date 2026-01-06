from fastapi import FastAPI, HTTPException
from bson import ObjectId

from db import item_collection
from schemas import ItemCreate, ItemUpdate

app = FastAPI(title="Simple CRUD API")

#create
@app.post("/items")
def create_item(item: ItemCreate):
    result = item_collection.insert_one(item.dict())
    return {"id": str(result.inserted_id)}

#read(all)
@app.get("/items")
def get_items():
    items = []
    for item in item_collection.find():
        item["_id"] = str(item["_id"])
        items.append(item)
    return items

#read(one)
@app.get("/items/{item_id}")
def get_item(item_id: str):
    item = item_collection.find_one({"_id": ObjectId(item_id)})
    if not item:
        raise HTTPException(404, "Item not found")
    item["_id"] = str(item["_id"])
    return item

#update
@app.put("/items/{item_id}")
def update_item(item_id: str, item: ItemUpdate):
    result = item_collection.update_one(
        {"_id": ObjectId(item_id)},
        {"$set": {k: v for k, v in item.dict().items() if v is not None}}
    )
    if result.matched_count == 0:
        raise HTTPException(404, "Item not found")
    return {"message": "Item updated"}

#delete
@app.delete("/items/{item_id}")
def delete_item(item_id: str):
    result = item_collection.delete_one({"_id": ObjectId(item_id)})
    if result.deleted_count == 0:
        raise HTTPException(404, "Item not found")
    return {"message": "Item deleted"}
