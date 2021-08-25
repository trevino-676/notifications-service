import ssl
import json
import pathlib
from os import environ

import websockets

from logger import logger

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
certificate = pathlib.Path(__file__).with_name(environ.get("CERTIFICATE"))
ssl_context.load_verify_locations(certificate)


async def notify():
    uri = environ.get("WS_URI")
    try:
        async with websockets.connect(uri, ssl=ssl_context) as ws:
            data = {"action": "notify"}
            await ws.send(json.dumps(data))
            return True
    except Exception as e:
        logger.error(e)
        return False
