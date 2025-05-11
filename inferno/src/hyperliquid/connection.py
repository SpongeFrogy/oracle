from typing import Any, Callable
from hyperliquid.info import Info
from hyperliquid.utils.constants import MAINNET_API_URL, TESTNET_API_URL
from hyperliquid.utils.types import Subscription
from time import time

class HyperliquidConnection:
    def __init__(self, test_net: bool):
        self._info = Info(
            base_url=TESTNET_API_URL if test_net else MAINNET_API_URL,
            skip_ws=False
        )
        self._perps = [coin for coin in self._info.coin_to_asset.keys() if coin.isalpha()] # filter spot
        self._subscriptions: dict[tuple[str, str], int] = {}

    @property
    def perps(self):
        return self._perps

    def subscribe(self, interval: str, coin: str, callback: Callable):
        message: Subscription = {
            'type': 'candle',
            'coin': coin,
            'interval': interval,
        }

        sub_id = self._info.subscribe(message, callback)
        self._subscriptions[(coin, interval)] = sub_id
    
    def unsubscribe(self, interval: str, coin: str):
        message: Subscription = {
            'type': 'candle',
            'coin': coin,
            'interval': interval,
        }
        sub_id = self._subscriptions.pop((coin, interval))
        self._info.unsubscribe(message, sub_id)

    def candles_snapshot(self, name: str, interval: str, limit: int) -> list[dict[str, Any]]:
        end_time = int(time() * 1000) # ms
        interval_ms = {
            "1m": 60 * 1000,
            "5m": 5 * 60 * 1000,
            "15m": 15 * 60 * 1000,
            "1h": 60 * 60 * 1000,
            "4h": 4 * 60 * 60 * 1000,
            "1d": 24 * 60 * 60 * 1000
        }.get(interval, 60 * 1000) # ms

        start_time = end_time - (interval_ms * limit) # ms

        return self._info.candles_snapshot(
            name=name,
            interval=interval,
            startTime=start_time,
            endTime=end_time
        )