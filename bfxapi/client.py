from .websocket import BfxWebsocketClient

from enum import Enum

class Constants(str, Enum):
    WSS_HOST = "wss://api.bitfinex.com/ws/2"
    PUB_WSS_HOST = "wss://api-pub.bitfinex.com/ws/2"

class Client(object):
    def __init__(self, WSS_HOST: str = Constants.WSS_HOST, API_KEY: str = None, API_SECRET: str = None, log_level: str = "INFO"):
        self.wss = BfxWebsocketClient(host=WSS_HOST, log_level=log_level, API_KEY=API_KEY, API_SECRET=API_SECRET)