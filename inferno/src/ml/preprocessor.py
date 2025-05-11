from typing import Any
import numpy as np
import pandas as pd
import pandas_ta as ta


class PreProcessor:
    FEATURE_COLS = [
        "rsi_14",
        "mom_10d",
        "mom_30d",
        "stochk_14_3_3",
        "stochd_14_3_3",
        "macd_hist",
        "adx_14",
        "plus_di_14",
        "minus_di_14",
        "sma_50_ratio",
        "ema_20_ratio",
        "atr_14_norm",
        "bbands_width_20_2",
        "volatility_30d",
        "volatility_90d",
        "obv_pct_change_10d",
        "donchian_width_rel_60",
    ]

    @classmethod
    def convert(cls, data: list[dict[str, Any]]) -> pd.DataFrame:
        df = pd.DataFrame(
            data=data,
        ).rename(
            columns={
                "T": "end",
                "o": "open",
                "c": "close",
                "h": "high",
                "l": "low",
                "v": "volume",
                "t": "timestamp",
            }
        )
        df['end'] = df["end"].astype(int)
        df['open'] = df["open"].astype(float)
        df['close'] = df["close"].astype(float)
        df['high'] = df["high"].astype(float)
        df['low'] = df["low"].astype(float)
        df['volume'] = df["volume"].astype(float)
        df['timestamp'] = df["timestamp"].astype(int)

        return df

    @classmethod
    def _features(cls, data: pd.DataFrame) -> pd.DataFrame:
        data["rsi_14"] = ta.rsi(data["close"], length=14)

        data["mom_10d"] = data["close"].pct_change(periods=10)
        data["mom_30d"] = data["close"].pct_change(periods=30)

        data[["stochk_14_3_3", "stochd_14_3_3"]] = ta.stoch(
            data["high"], data["low"], data["close"], k=14, d=3, smooth_k=3
        )

        data["macd_hist"] = ta.macd(data["close"])["MACDh_12_26_9"]  # type: ignore[reportOptionalMemberAccess]

        data[["adx_14", "plus_di_14", "minus_di_14"]] = ta.adx(
            data["high"], data["low"], data["close"], length=14
        )

        data["sma_50_ratio"] = data["close"] / ta.sma(data["close"], length=50) - 1  # type: ignore[reportOptionalMemberAccess]
        data["ema_20_ratio"] = data["close"] / ta.ema(data["close"], length=50) - 1  # type: ignore[reportOptionalMemberAccess]

        data["atr_14_norm"] = ta.atr(data["high"], data["low"], data["close"], length=14) / data["close"]  # type: ignore[reportOptionalMemberAccess]

        _bbands = ta.bbands(data["close"], length=20, std=2)
        data["bbands_width_20_2"] = (_bbands["BBU_20_2.0"] - _bbands["BBL_20_2.0"]) / _bbands["BBM_20_2.0"]  # type: ignore[reportOptionalMemberAccess]

        data["log_returns_1d"] = np.log(data["close"] / data["close"].shift(1))
        data["volatility_30d"] = data["log_returns_1d"].rolling(window=30).std()
        data["volatility_90d"] = data["log_returns_1d"].rolling(window=90).std()

        data["obv_pct_change_10d"] = ta.obv(data["close"], data["volume"]).pct_change(
            periods=10
        )

        _dc = ta.donchian(
            high=data["high"], low=data["low"], lower_length=60, upper_length=60
        )
        data["donchian_width_rel_60"] = (_dc["DCU_60_60"] - _dc["DCL_60_60"]) / data["close"]  # type: ignore[reportOptionalMemberAccess]

        data.drop(columns=["log_returns_1d"], errors="ignore", inplace=True)

        data[cls.FEATURE_COLS] = data[cls.FEATURE_COLS].shift(1)

        data.ffill(inplace=True)
        data.bfill(inplace=True)

        return data

    @classmethod
    def process(cls, data: list[dict[str, Any]]) -> pd.DataFrame:
        _data = cls.convert(data)
        return cls._features(_data)
