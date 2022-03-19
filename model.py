import json
import logging
from kafka import KafkaConsumer
import os
import copy as cp
from river import preprocessing
from river import tree
from collections import deque

logging.basicConfig(level=logging.INFO)

consumer = KafkaConsumer(
    'new_processed_candle',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id="group_new_processed_candle",
    value_deserializer=json.loads
)


base_model = (
            preprocessing.StandardScaler() |
            tree.HoeffdingTreeRegressor(
                grace_period=100,
                leaf_prediction='adaptive',
                model_selector_decay=0.9
            )
        )


def save_data(ticker, y, y_pred):
    with open(os.path.join(BACKUP_PATH, ticker+".csv"), 'a') as fp:
        fp.write("{}, {}\n".format(y, y_pred))

RAM_BACKUP_SIZE = 20
BACKUP_PATH = "./predictions/"
state = {}
"""
state ->
"BTCUSDT": {
    model,
    previous_candles = deque()
    previous_predictions = deque()
}
"""
for msg in consumer:
    print("New msg received !")
    new_candle = msg.value
    print(new_candle)
    ticker = new_candle['ticker']
    new_candle.pop('ticker')

    if ticker not in state.keys():
        state[ticker] = {}
        state[ticker]['model'] = cp.deepcopy(base_model)
        state[ticker]['previous_candles'] = deque(maxlen=RAM_BACKUP_SIZE)
        state[ticker]['previous_candles'].append({
            'Open': 0, 'High': 0,
            'Close': 0, 'Low': 0,
            'Volume': 0, 'Slow_SMA': 0, 'Fast_SMA': 0
        })
        state[ticker]['previous_predictions'] = deque(maxlen=RAM_BACKUP_SIZE)
        state[ticker]['previous_predictions'].append(0)

    prediction = state[ticker]['model'].predict_one(new_candle)
    state[ticker]['model'].learn_one(state[ticker]["previous_candles"][-1], new_candle["Close"])
    state[ticker]["previous_candles"].append(new_candle)
    state[ticker]["previous_predictions"].append(prediction)

    save_data(ticker, new_candle["Close"], state[ticker]["previous_predictions"][-1])
    print(prediction)
