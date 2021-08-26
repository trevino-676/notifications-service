import ssl
import json
from os import environ, path

import websockets

from logger import logger

BASEDIR = path.abspath(path.dirname(__file__))
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
certificate = path.join(BASEDIR, environ.get("CERTIFICATE"))
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
