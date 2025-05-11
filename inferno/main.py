import os
import pika
import json
import logging
from time import time

from src.config import settings
from src.hyperliquid.collection import HyperliquidCollector
from src.donchian.donchian import DonchianStrategy
from src.ml.preprocessor import PreProcessor
from src.ml.loader import ModelLoader
from src.ml.inference import ModelInference
from src.types.signal import (
    SignalType, Suggestion, SignalResponse, SignalRequest
)
from src.types.prediction import Prediction


logging.basicConfig(level=logging.DEBUG)

# set up data collection
hl_collector = HyperliquidCollector(
    test_net=settings.TEST_NET,
    symbols=['BTC', 'ETH'],
    interval='1m',
    max_candles=500
)
hl_collector.start()

# set up base technical strategy
donchian = DonchianStrategy(
    LOOK_BACK_WINDOWS=settings.LOOK_BACK_WINDOWS,
    TARGET_VOLATILITY=settings.TARGET_VOLATILITY,
    MAX_ALLOCATION=settings.MAX_ALLOCATION,
    VOLATILITY_WINDOW=settings.VOLATILITY_WINDOW,
    TRADING_DAYS_PER_YEAR=settings.TRADING_DAYS_PER_YEAR,
    RISK_FREE_RATE=settings.RISK_FREE_RATE
)

# set up ml
preprocessor = PreProcessor()
loader = ModelLoader(settings.MODELS_DIR)
inference = ModelInference(os.path.join(settings.MODELS_DIR, settings.MODEL_FILE), loader, preprocessor, donchian)

# main generator
def generate(request: SignalRequest) -> SignalResponse:
    raw_candles = hl_collector.get_candles(symbol=request.symbol)
    candles = preprocessor.convert(raw_candles) 
    if request.signal_type == SignalType.TECHNICAL:
        last_candle_timestamp, last_candle_suggestion = donchian.get_signal(candles)
        return SignalResponse(
            success=True,
            suggestion=last_candle_suggestion,
            timestamp=last_candle_timestamp
        )
    elif request.signal_type == SignalType.ML:
        suggestion, prediction = inference.predict(candles)

        return SignalResponse(
            success=True,
            suggestion=suggestion,
            timestamp=candles.iloc[-1]['timestamp'],
            prediction=prediction
        )
    else:
        return SignalResponse(
            success=False,
            suggestion=Suggestion.HOLD,
            timestamp=int(time()*1000)
        )

# set up queue
connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host=settings.RABBITMQ_HOST,
        credentials=pika.PlainCredentials(
            settings.RABBITMQ_DEFAULT_USER,
            settings.RABBITMQ_DEFAULT_PASS
        )
    )
)
channel = connection.channel()

channel.queue_declare(queue=settings.RABBITMQ_QUEUE)


def on_request(ch, method, props, body):
    data = json.loads(body)
    request = SignalRequest(**data)

    response = generate(request)

    ch.basic_publish(
        exchange='',
        routing_key=props.reply_to,
        properties=pika.BasicProperties(
            correlation_id=props.correlation_id
        ),
        body=json.dumps(response.model_dump()))
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=settings.RABBITMQ_QUEUE, on_message_callback=on_request)

channel.start_consuming()
