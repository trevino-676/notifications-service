import json

# import ssl
# import pathlib

import pymongo
import websockets

client = pymongo.MongoClient("mongodb://root:drumb0t2o21@3.141.244.21:27017/")
db = client.robin_hood
collection = db["notifications"]

# ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
# pem_file = pathlib.Path(__file__).with_name("cert.pem")
# ssl_context.load_verify_locations(pem_file)


def __convert_supplier_to_user(notification: dict):
    if "suppliers" not in notification:
        return notification

    filters = {"suppliers": {"$in": notification["suppliers"]}}
    companies = db["companies"].find(filters)
    companies_rfc = [item["rfc"] for item in list(companies)]
    company_filters = {"companies": {"$in": companies_rfc}}
    users = db["users"].find(company_filters)
    notification["users"] = [str(item["_id"]) for item in list(users)]
    notification.pop("suppliers")
    return notification


def __convert_company_to_user(notification: dict):
    if "companies" not in notification:
        return notification

    filters = {"companies": {"$in": notification["companies"]}}
    users = db["users"].find(filters)
    notification["users"] = [str(item["_id"]) for item in list(users)]
    notification.pop("companies")
    return notification


def cretate_notification(notification: dict) -> dict:
    notification = __convert_supplier_to_user(notification)
    notification = __convert_company_to_user(notification)
    if "is_active" not in notification:
        notification["is_active"] = True

    new_notification = collection.insert_one(notification)
    created_notification = collection.find_one({"_id": new_notification.inserted_id})
    created_notification["_id"] = str(created_notification["_id"])
    return created_notification


async def notify():
    uri = "wss://ws.sonar32.com.mx"
    async with websockets.connect(uri, ssl=True) as websocket:
        data = {"action": "notify"}
        await websocket.send(json.dumps(data))
