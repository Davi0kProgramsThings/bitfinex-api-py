from . import serializers
from .enums import Channels
from .exceptions import BfxWebsocketException

def _get_sub_dictionary(dictionary, keys):
    return { key: dictionary[key] for key in dictionary if key in keys }
    
class PublicChannelsHandler(object):
    EVENTS = [
        "t_ticker_update", "f_ticker_update",
        "t_trade_executed", "t_trade_execution_update", "f_trade_executed", "f_trade_execution_update", "t_trades_snapshot", "f_trades_snapshot",
        "t_book_snapshot", "f_book_snapshot", "t_raw_book_snapshot", "f_raw_book_snapshot", "t_book_update", "f_book_update", "t_raw_book_update", "f_raw_book_update",
        "candles_snapshot", "candles_update",
        "derivatives_status_update",
    ]

    def __init__(self, event_emitter):
        self.event_emitter = event_emitter

        self.__handlers = {
            Channels.TICKER: self.__ticker_channel_handler,
            Channels.TRADES: self.__trades_channel_handler,
            Channels.BOOK: self.__book_channel_handler,
            Channels.CANDLES: self.__candles_channel_handler,
            Channels.STATUS: self.__status_channel_handler
        }

    def handle(self, subscription, *stream):
        if channel := subscription["channel"] or channel in self.__handlers.keys():
            return self.__handlers[channel](subscription, *stream)

    def __ticker_channel_handler(self, subscription, *stream):
        if subscription["symbol"].startswith("t"):
            return self.event_emitter.emit(
                "t_ticker_update",
                _get_sub_dictionary(subscription, [ "chanId", "symbol", "pair" ]),
                serializers.TradingPairTicker.parse(*stream[0])
            )

        if subscription["symbol"].startswith("f"):
            return self.event_emitter.emit(
                "f_ticker_update",
                _get_sub_dictionary(subscription, [ "chanId", "symbol", "currency" ]),
                serializers.FundingCurrencyTicker.parse(*stream[0])
            )

    def __trades_channel_handler(self, subscription, *stream):
        if type := stream[0] or type in [ "te", "tu", "fte", "ftu" ]:
            if subscription["symbol"].startswith("t"):
                return self.event_emitter.emit(
                    { "te": "t_trade_executed", "tu": "t_trade_execution_update" }[type],
                    _get_sub_dictionary(subscription, [ "chanId", "symbol", "pair" ]),
                    serializers.TradingPairTrade.parse(*stream[1])
                )

            if subscription["symbol"].startswith("f"):
                return self.event_emitter.emit(
                    { "fte": "f_trade_executed", "ftu": "f_trade_execution_update" }[type],
                    _get_sub_dictionary(subscription, [ "chanId", "symbol", "currency" ]),
                    serializers.FundingCurrencyTrade.parse(*stream[1])
                )

        if subscription["symbol"].startswith("t"):
            return self.event_emitter.emit(
                "t_trades_snapshot",
                _get_sub_dictionary(subscription, [ "chanId", "symbol", "pair" ]),
                [ serializers.TradingPairTrade.parse(*substream) for substream in stream[0] ]
            )

        if subscription["symbol"].startswith("f"):
            return self.event_emitter.emit(
                "f_trades_snapshot",
                _get_sub_dictionary(subscription, [ "chanId", "symbol", "currency" ]),
                [ serializers.FundingCurrencyTrade.parse(*substream)  for substream in stream[0] ]
            )

    def __book_channel_handler(self, subscription, *stream):
        subscription = _get_sub_dictionary(subscription, [ "chanId", "symbol", "prec", "freq", "len", "subId", "pair" ])

        type = subscription["symbol"][0]

        if subscription["prec"] == "R0":
            _trading_pair_serializer, _funding_currency_serializer, IS_RAW_BOOK = serializers.TradingPairRawBook, serializers.FundingCurrencyRawBook, True
        else: _trading_pair_serializer, _funding_currency_serializer, IS_RAW_BOOK = serializers.TradingPairBook, serializers.FundingCurrencyBook, False

        if all(isinstance(substream, list) for substream in stream[0]):
            return self.event_emitter.emit(               
                type + "_" + (IS_RAW_BOOK and "raw_book" or "book") + "_snapshot",
                subscription, 
                [ { "t": _trading_pair_serializer, "f": _funding_currency_serializer }[type].parse(*substream) for substream in stream[0] ]
            )

        return self.event_emitter.emit(
            type + "_" + (IS_RAW_BOOK and "raw_book" or "book") + "_update",
            subscription, 
            { "t": _trading_pair_serializer, "f": _funding_currency_serializer }[type].parse(*stream[0])
        )
        
    def __candles_channel_handler(self, subscription, *stream):
        subscription = _get_sub_dictionary(subscription, [ "chanId", "key" ])

        if all(isinstance(substream, list) for substream in stream[0]):
            return self.event_emitter.emit(
                "candles_snapshot", 
                subscription, 
                [ serializers.Candle.parse(*substream) for substream in stream[0] ]
            )

        return self.event_emitter.emit(
            "candles_update", 
            subscription, 
            serializers.Candle.parse(*stream[0])
        )

    def __status_channel_handler(self, subscription, *stream):
        subscription = _get_sub_dictionary(subscription, [ "chanId", "key" ])

        if subscription["key"].startswith("deriv:"):
            return self.event_emitter.emit(
                "derivatives_status_update",
                subscription,
                serializers.DerivativesStatus.parse(*stream[0])
            )

class AuthenticatedChannelsHandler(object):
    __abbreviations = {
        "os": "order_snapshot", "on": "order_new", "ou": "order_update", "oc": "order_cancel",
        "ps": "position_snapshot", "pn": "position_new", "pu": "position_update", "pc": "position_close",
        "te": "trade_executed", "tu": "trade_execution_update",
        "fos": "funding_offer_snapshot", "fon": "funding_offer_new", "fou": "funding_offer_update", "foc": "funding_offer_cancel",
        "fcs": "funding_credit_snapshot", "fcn": "funding_credit_new", "fcu": "funding_credit_update", "fcc": "funding_credit_close",
        "fls": "funding_loan_snapshot", "fln": "funding_loan_new", "flu": "funding_loan_update", "flc": "funding_loan_close",
        "ws": "wallet_snapshot", "wu": "wallet_update",
        "bu": "balance_update",
    }

    __serializers = {
        ("os", "on", "ou", "oc",): serializers.Order,
        ("ps", "pn", "pu", "pc",): serializers.Position,
        ("te",): serializers.TradeExecuted,
        ("tu",): serializers.TradeExecutionUpdate,
        ("fos", "fon", "fou", "foc",): serializers.FundingOffer,
        ("fcs", "fcn", "fcu", "fcc",): serializers.FundingCredit,
        ("fls", "fln", "flu", "flc",): serializers.FundingLoan,
        ("ws", "wu",): serializers.Wallet,
        ("bu",): serializers.BalanceInfo
    }

    EVENTS = [ 
        "notification", 
        "on-req-notification", "ou-req-notification", "oc-req-notification",
        "oc_multi-notification",
        "fon-req-notification", "foc-req-notification",
        *list(__abbreviations.values()) 
    ]

    def __init__(self, event_emitter, strict = False):
        self.event_emitter, self.strict = event_emitter, strict

    def handle(self, type, stream):
        if type == "n":
            return self.__notification(stream)

        for types, serializer in AuthenticatedChannelsHandler.__serializers.items():
            if type in types:
                event = AuthenticatedChannelsHandler.__abbreviations[type]

                if all(isinstance(substream, list) for substream in stream):
                    return self.event_emitter.emit(event, [ serializer.parse(*substream) for substream in stream ])

                return self.event_emitter.emit(event, serializer.parse(*stream))
        
        if self.strict == True:
            raise BfxWebsocketException(f"Event of type <{type}> not found in self.__handlers.")
    
    def __notification(self, stream):
        if stream[1] == "on-req" or stream[1] == "ou-req" or stream[1] == "oc-req":
            return self.event_emitter.emit(f"{stream[1]}-notification", serializers._Notification(serializer=serializers.Order).parse(*stream))

        if stream[1] == "oc_multi-req":
            return self.event_emitter.emit(f"{stream[1]}-notification", serializers._Notification(serializer=serializers.Order, iterate=True).parse(*stream))

        if stream[1] == "fon-req" or stream[1] == "foc-req":
            return self.event_emitter.emit(f"{stream[1]}-notification", serializers._Notification(serializer=serializers.FundingOffer).parse(*stream))

        return self.event_emitter.emit("notification", serializers._Notification(serializer=None).parse(*stream))