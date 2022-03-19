import json
import logging
from kafka import KafkaProducer
import websocket
import requests
logging.basicConfig(level=logging.INFO)

producer = KafkaProducer(bootstrap_servers='localhost:9092')

TICKER_LIST = ['BTCUSDT', 'ETHUSDT', 'DOGEUSDT']
TIMESTEP = "1m"
SOCK = "wss://stream.binance.com:9443/stream?streams=btcusdt@kline_"+TIMESTEP+"/ethusdt@kline_"+TIMESTEP+"/dogeusdt@kline_"+TIMESTEP
binance_api_url = 'https://api.binance.com/api/v3/klines'

for ticker in TICKER_LIST:
    print('Initial train: {}'.format(ticker))
    params = {
        'symbol': ticker,
        'interval': TIMESTEP,
        'limit': 1000
    }
    response = requests.get(binance_api_url, params=params)
    candles_data = response.json()
    for candle_data in candles_data:
        candle = {'o': candle_data[1], 'h': candle_data[2], 'c': candle_data[4], 'l': candle_data[3],
                  'v': candle_data[5], 's': ticker}
        print(candle)
        producer.send('new_data', value=json.dumps(candle).encode('utf-8'))


def on_open(ws):
    print("Now: running online")


def on_message(ws, message):
    json_message = json.loads(message)
    online_candle = json_message['data']['k']
    is_candle_closed = online_candle['x']
    if is_candle_closed:
        print(online_candle)
        producer.send('new_data', value=json.dumps(online_candle).encode('utf-8'))


def on_close(ws, close_status_code, close_msg):
    print("closed")


ws = websocket.WebSocketApp(SOCK, on_open=on_open, on_close=on_close, on_message=on_message)
ws.run_forever()
