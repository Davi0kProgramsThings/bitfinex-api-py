from typing import Type, Tuple, List, Dict, TypedDict, Union, Optional, Any

from .. notification import Notification

JSON = Union[Dict[str, "JSON"], List["JSON"], bool, int, float, str, Type[None]]

#region Type hinting for Rest Public Endpoints

class PlatformStatus(TypedDict):
    OPERATIVE: int

class TradingPairTicker(TypedDict):
    SYMBOL: Optional[str]
    BID: float
    BID_SIZE: float
    ASK: float
    ASK_SIZE: float
    DAILY_CHANGE: float
    DAILY_CHANGE_RELATIVE: float
    LAST_PRICE: float
    VOLUME: float
    HIGH: float
    LOW: float

class FundingCurrencyTicker(TypedDict):
    SYMBOL: Optional[str]
    FRR: float
    BID: float
    BID_PERIOD: int
    BID_SIZE: float
    ASK: float
    ASK_PERIOD: int
    ASK_SIZE: float
    DAILY_CHANGE: float
    DAILY_CHANGE_RELATIVE: float
    LAST_PRICE: float
    VOLUME: float
    HIGH: float
    LOW: float
    FRR_AMOUNT_AVAILABLE: float

class FundingCredits(TypedDict):
    ID: int
    SYMBOL: str
    SIDE: int
    MTS_CREATE: int
    MTS_UPDATE: int
    AMOUNT: float
    FLAGS: JSON
    STATUS: str
    RATE_TYPE: str
    RATE: float
    PERIOD: int
    MTS_OPENING: int
    MTS_LAST_PAYOUT: int
    NOTIFY: int
    HIDDEN: int
    RENEW: int
    NO_CLOSE: int
    POSITION_PAIR: str

class TickersHistory(TypedDict):
    SYMBOL: str
    BID: float
    ASK: float
    MTS: int

class TradingPairTrade(TypedDict):
    ID: int 
    MTS: int 
    AMOUNT: float 
    PRICE: float

class FundingCurrencyTrade(TypedDict):
    ID: int 
    MTS: int 
    AMOUNT: float 
    RATE: float 
    PERIOD: int

class TradingPairBook(TypedDict):
    PRICE: float 
    COUNT: int 
    AMOUNT: float
    
class FundingCurrencyBook(TypedDict):
    RATE: float 
    PERIOD: int 
    COUNT: int 
    AMOUNT: float
        
class TradingPairRawBook(TypedDict):
    ORDER_ID: int
    PRICE: float 
    AMOUNT: float
            
class FundingCurrencyRawBook(TypedDict):
    OFFER_ID: int 
    PERIOD: int 
    RATE: float 
    AMOUNT: float

class Statistic(TypedDict):
    MTS: int
    VALUE: float

class Candle(TypedDict):
    MTS: int
    OPEN: float
    CLOSE: float
    HIGH: float
    LOW: float
    VOLUME: float

class DerivativesStatus(TypedDict):
    KEY: Optional[str]
    MTS: int
    DERIV_PRICE: float
    SPOT_PRICE: float
    INSURANCE_FUND_BALANCE: float
    NEXT_FUNDING_EVT_TIMESTAMP_MS: int
    NEXT_FUNDING_ACCRUED: float
    NEXT_FUNDING_STEP: int
    CURRENT_FUNDING: float
    MARK_PRICE: float
    OPEN_INTEREST: float
    CLAMP_MIN: float
    CLAMP_MAX: float

class Liquidation(TypedDict):
    POS_ID: int
    MTS: int
    SYMBOL: str
    AMOUNT: float
    BASE_PRICE: float
    IS_MATCH: int
    IS_MARKET_SOLD: int
    PRICE_ACQUIRED: float

class Leaderboard(TypedDict):
    MTS: int
    USERNAME: str
    RANKING: int
    VALUE: float
    TWITTER_HANDLE: Optional[str]

class FundingStatistic(TypedDict): 
    TIMESTAMP: int
    FRR: float
    AVG_PERIOD: float
    FUNDING_AMOUNT: float
    FUNDING_AMOUNT_USED: float
    FUNDING_BELOW_THRESHOLD: float

#endregion

#region Type hinting for Rest Authenticated Endpoints

class Wallet(TypedDict):
    WALLET_TYPE: str
    CURRENCY: str
    BALANCE: float
    UNSETTLED_INTEREST: float
    AVAILABLE_BALANCE: float
    LAST_CHANGE: str
    TRADE_DETAILS: JSON

class Order(TypedDict):
    ID: int
    GID: int
    CID: int
    SYMBOL: str
    MTS_CREATE: int
    MTS_UPDATE: int
    AMOUNT: float
    AMOUNT_ORIG: float
    ORDER_TYPE: str
    TYPE_PREV: str
    MTS_TIF: int
    FLAGS: int
    ORDER_STATUS: str
    PRICE: float
    PRICE_AVG: float
    PRICE_TRAILING: float
    PRICE_AUX_LIMIT: float
    NOTIFY: int
    HIDDEN: int
    PLACED_ID: int
    ROUTING: str
    META: JSON

class FundingOffer(TypedDict):
    ID: int
    SYMBOL: str
    MTS_CREATE: int
    MTS_UPDATE: int
    AMOUNT: float
    AMOUNT_ORIG: float
    OFFER_TYPE: str
    FLAGS: int
    OFFER_STATUS: str
    RATE: float
    PERIOD: int
    NOTIFY: bool
    HIDDEN: int
    RENEW: bool
    
class Trade(TypedDict):
    ID: int 
    SYMBOL: str 
    MTS_CREATE: int
    ORDER_ID: int 
    EXEC_AMOUNT: float 
    EXEC_PRICE: float 
    ORDER_TYPE: str 
    ORDER_PRICE: float 
    MAKER: int
    FEE: float
    FEE_CURRENCY: str
    CID: int

class OrderTrade(TypedDict):
    ID: int
    PAIR: str
    MTS_CREATE: int
    ORDER_ID: int
    EXEC_AMOUNT: float
    EXEC_PRICE: float
    MAKER: int
    FEE: float
    FEE_CURRENCY: str
    CID: int

class Position(TypedDict):
    SYMBOL: str
    STATUS: str
    AMOUNT: float
    BASE_PRICE: float
    FUNDING: float
    FUNDING_TYPE: int
    PL: float
    PL_PERC: float
    PRICE_LIQ: float
    LEVERAGE: float
    POSITION_ID: int
    MTS_CREATE: int
    MTS_UPDATE: int
    TYPE: int
    COLLATERAL: float
    COLLATERAL_MIN: float
    META: JSON

class Ledger(TypedDict):
    ID: int
    CURRENCY: str 
    MTS: int
    AMOUNT: float
    BALANCE: float
    description: str

#endregion