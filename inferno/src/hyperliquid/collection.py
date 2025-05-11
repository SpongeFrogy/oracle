from typing import Any
from datetime import datetime
import logging

from .connection import HyperliquidConnection

logger = logging.getLogger(__name__)


class HyperliquidCollector:
    def __init__(
        self,
        test_net: bool,
        symbols: list[str],
        interval: str,
        max_candles: int
    ):
        self._connection = HyperliquidConnection(test_net=test_net)
        self._symbols = symbols
        self._interval = interval
        self._max_candles = max_candles
        self.candles: dict[str, list[dict[str, Any]]] = {}

    @property
    def symbols(self):
        return self._symbols

    @property
    def interval(self):
        return self._interval

    @property
    def max_candles(self):
        return self._max_candles

    def start(self):
        for symbol in self._symbols:
            self.candles[symbol] = self._connection.candles_snapshot(
                symbol, self._interval, self.max_candles
            )
            self._connection.subscribe(
                interval=self._interval,
                coin=symbol,
                callback=self.handle_message
            )
        logger.debug(f'started collection for symbols: {self.symbols} (interval: {self.interval})')

    def stop(self):
        for symbol in self._symbols:
            self._connection.unsubscribe(self._interval, symbol)

    def merge_candle(self, symbol: str, data: dict[str, Any]) -> None:
        """Merge new candle data with existing candles."""
        if not symbol in self.candles.keys():
            self.candles[symbol] = [data]
            return

        latest_candle = self.candles[symbol][-1]
        if latest_candle['t'] == data['t']:
            self.candles[symbol][-1] = data
        else:
            self.candles[symbol].append(data)
            logger.debug(f"Add new candle to {symbol}")

    def check_max_candles(self, symbol: str) -> None:
        """Ensure we don't exceed the maximum number of candles."""
        if len(self.candles[symbol]) > self.max_candles:
            self.candles[symbol] = self.candles[symbol][-self.max_candles:]
            logger.debug(f"Trimmed candles to {self.max_candles}")

    def handle_message(self, msg: dict[str, Any]):
        symbol = msg['data']['s']
        self.handle_candles(symbol=symbol, data=msg)

    def handle_candles(self, symbol: str, data: dict[str, Any]):
        """Handle incoming candle updates."""
        try:
            if 'data' in data:
                self.merge_candle(symbol, data['data'])
                self.check_max_candles(symbol)
                logger.debug(
                    f"Updated candles at {datetime.fromtimestamp(data['data']['t']/1000)}")
        except Exception as e:
            logger.error(f"Error handling candles: {str(e)}")

    def get_candles(self, symbol: str):
        return self.candles[symbol]
