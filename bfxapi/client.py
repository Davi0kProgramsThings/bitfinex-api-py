from .websocket import BfxWebsocketClient
from .rest import BfxRestInterface

from typing import Optional

from enum import Enum

class Constants(str, Enum):
    REST_HOST = "https://api.bitfinex.com/v2"
    PUB_REST_HOST = "https://api-pub.bitfinex.com/v2"

    WSS_HOST = "wss://api.bitfinex.com/ws/2"
    PUB_WSS_HOST = "wss://api-pub.bitfinex.com/ws/2"

class Client(object):
    def __init__(
            self,
            REST_HOST: str = Constants.REST_HOST,
            WSS_HOST: str = Constants.WSS_HOST,
            API_KEY: Optional[str] = None,
            API_SECRET: Optional[str] = None,
            log_level: str = "WARNING"
    ):
        self.wss = BfxWebsocketClient(
            host=WSS_HOST, 
            API_KEY=API_KEY, 
            API_SECRET=API_SECRET, 
            log_level=log_level
        )
        self.rest = BfxRestInterface(
            host=REST_HOST,
            API_KEY=API_KEY,
            API_SECRET=API_SECRET
        )