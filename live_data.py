import requests
from datetime import datetime, timedelta
import pandas as pd
from load_dotenv import load_dotenv
import account_info
import time
import json
import os
load_dotenv()

window = 24
momentum_trigger = 20
risk = 0.2 #from optimizer
tp = 0.21 #from optimizer

server_time_req = requests.get('https://api.binance.us/api/v3/time')
server_time = int(server_time_req.json()['serverTime'])
window_time_ago = int((datetime.fromtimestamp(server_time/1000) - timedelta(hours=window)).timestamp() * 1000)

params = {
    "symbol": "BTCUSDT",
    "interval": "1h",
    "startTime": window_time_ago,
    "endTime": server_time
}

r = requests.get('https://api.binance.us/api/v3/klines?', params=params)
window_bars = pd.DataFrame(r.json())
window_bars.columns=['openTime', 'open', 'high', 'low', 'close', 'volume', 'closeTime', 'quoteVolume', 'numTrades', 'takerBase', 'takerVolume','unused']
print(window_bars)
pct_change = pd.Series(window_bars['close'].astype(float)).pct_change()
print(pct_change)
momentum = pct_change.product()-1
print(momentum)

account_data_uri_path = "/api/v3/account"
account_params = {
    "timestamp": int(round(time.time() * 1000)),
}
current_price = float(requests.get('https://api.binance.us/api/v3/ticker/price?symbol=BTCUSDT').json()['price'])
get_account_result = account_info.binanceus_get_request(account_data_uri_path, account_params, os.getenv('PUBLIC_KEY'), os.getenv('PRIVATE_KEY'))
current_balance = float(json.loads(get_account_result)['balances'][4]['free'])
quan = round(1/current_price, 5)
print('{0:.5f}'.format(quan))
order_uri_path = "/api/v3/order"
order_params = {
    'symbol': 'BTCUSDT',
    'side': 'BUY',
    'type': 'MARKET',
    'quantity': '{0:.5f}'.format(quan),
    'timestamp': int(round(time.time() * 1000))
}

submit_order_request = account_info.binanceus_post_request(order_uri_path, order_params, os.getenv('PUBLIC_KEY'), os.getenv('PRIVATE_KEY'))
print(order_params)
print("POST {}: {}".format(order_uri_path, submit_order_request))

if momentum > momentum_trigger:
    pass
    # Sell
elif momentum < -momentum_trigger:
    #Buy
    pass