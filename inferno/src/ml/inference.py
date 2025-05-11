from typing import Any
import pandas as pd
from sklearn.preprocessing import StandardScaler
from lightgbm import LGBMClassifier
from time import time
import logging

from .preprocessor import PreProcessor
from .loader import ModelLoader
from src.donchian.donchian import DonchianStrategy
from src.types.prediction import Prediction
from src.types.signal import Suggestion
from src.types.error import ValidateLoadingError
from src.utils.error import log_raise


logger = logging.getLogger(__name__)

class ModelInference:
    def __init__(
        self,
        file: str,
        loader: ModelLoader,
        preprocessor: PreProcessor,
        donchian: DonchianStrategy

    ):
        self._loader = loader
        self._preprocessor = preprocessor
        self._donchian = donchian
        self._loader.load_model(file)
        loading = self._loader.get_model()

        self.scaler: StandardScaler = loading['scaler']
        self.clf: LGBMClassifier = loading['clf']
        self.features: list[str] = loading['features']
        self.threshold: float = loading['threshold']

    
    def predict(self, candles: pd.DataFrame) -> tuple[Suggestion, Prediction]:
        data = self._donchian.get_weights(candles)
        
        features = self._preprocessor._features(data)
        
        x = features[self.features]
        xs = self.scaler.transform(x)
        
        last_candle_model_input = xs[-1].reshape(1, -1)
        probability = self.clf.predict_proba(last_candle_model_input)[0, 1] # type: ignore
        
        suggestion = Suggestion.HOLD
        if probability > self.threshold:
            suggestion = Suggestion.BUY
        

        return suggestion, Prediction(
            confidence=probability,
            timestamp=int(time() * 1000)
        )
