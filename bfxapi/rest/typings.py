from typing import Type, Tuple, List, Dict, TypedDict, Union, Optional, Any

#region Type hinting for Rest Public Endpoints

PlatformStatus = TypedDict("PlatformStatus", {
    "OPERATIVE": int
})

TradingPairTicker = TypedDict("TradingPairTicker", {
    "SYMBOL": Optional[str],
    "BID": float,
    "BID_SIZE": float,
    "ASK": float,
    "ASK_SIZE": float,
    "DAILY_CHANGE": float,
    "DAILY_CHANGE_RELATIVE": float,
    "LAST_PRICE": float,
    "VOLUME": float,
    "HIGH": float,
    "LOW": float
})

FundingCurrencyTicker = TypedDict("FundingCurrencyTicker", {
    "SYMBOL": Optional[str],
    "FRR": float,
    "BID": float,
    "BID_PERIOD": int,
    "BID_SIZE": float,
    "ASK": float,
    "ASK_PERIOD": int,
    "ASK_SIZE": float,
    "DAILY_CHANGE": float,
    "DAILY_CHANGE_RELATIVE": float,
    "LAST_PRICE": float,
    "VOLUME": float,
    "HIGH": float,
    "LOW": float,
    "FRR_AMOUNT_AVAILABLE": float
})

TickerHistory = TypedDict("TickerHistory", {
    "SYMBOL": str,
    "BID": float,
    "ASK": float,
    "MTS": int
})

TickerHistories = List[TickerHistory]

(TradingPairTrade, FundingCurrencyTrade) = (
    TypedDict("TradingPairTrade", { "ID": int, "MTS": int, "AMOUNT": float, "PRICE": float }),
    TypedDict("FundingCurrencyTrade", { "ID": int, "MTS": int, "AMOUNT": float, "RATE": float, "PERIOD": int })
)

(TradingPairTrades, FundingCurrencyTrades) = (List[TradingPairTrade], List[FundingCurrencyTrade])

#endregion