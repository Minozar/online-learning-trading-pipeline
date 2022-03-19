import json
import logging
from kafka import KafkaConsumer, KafkaProducer
from collections import deque

logging.basicConfig(level=logging.INFO)

producer = KafkaProducer(bootstrap_servers='localhost:9092')
consumer = KafkaConsumer(
    'new_data',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id="group_new_data",
    value_deserializer=json.loads
)


def apply_moving_average(ticker_candles, window):
    ma = 0
    steps = min(len(ticker_candles), window)
    print(steps)
    for k in range(steps):
        ma += ticker_candles[-k-1]["Close"]
    return ma/steps


BACKUP_SIZE = 20
candles = {}
for msg in consumer:
    raw_new_candle = msg.value
    ticker = raw_new_candle['s']
    print("New msg received ! [{}]".format(ticker))
    new_candle = {"Open": float(raw_new_candle['o']), "High": float(raw_new_candle['h']),
                  "Close": float(raw_new_candle['c']), "Low": float(raw_new_candle['l']),
                  "Volume": float(raw_new_candle['v']), "ticker": ticker}

    if ticker not in candles.keys():
        candles[ticker] = deque(maxlen=BACKUP_SIZE)

    candles[ticker].append(new_candle)


    new_candle["Slow_SMA"] = apply_moving_average(candles[ticker], window=10)
    new_candle["Fast_SMA"] = apply_moving_average(candles[ticker], window=3)

    print(new_candle)
    producer.send('new_processed_candle', value=json.dumps(new_candle).encode('utf-8'))

