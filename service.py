import json

import pymongo
import websockets

client = pymongo.MongoClient("mongodb://root:drumb0t2o21@3.141.244.21:27017/")
db = client.robin_hood
collection = db["notifications"]


def cretate_notification(notification: dict) -> dict:
    new_notification = collection.insert_one(notification)
    created_notification = collection.find_one({"_id": new_notification.inserted_id})
    created_notification["_id"] = str(created_notification["_id"])
    return created_notification


async def notify():
    uri = "ws://localhost:6789"
    async with websockets.connect(uri) as websocket:
        data = {"action": "notify"}
        await websocket.send(json.dumps(data))
