import requests
from datetime import datetime, timedelta
import pandas as pd
from load_dotenv import load_dotenv
import account_info
import time
import json
import os
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
load_dotenv()

window = 24
momentum_trigger = 20
risk = 0.2 #from optimizer
tp = 0.21 #from optimizer

open_orders_uri = "/api/v3/openOrders"
account_data_uri_path = "/api/v3/account"
order_uri_path = "/api/v3/order"
account_params = {
    "timestamp": int(round(time.time() * 1000)),
}

def get_momentum():
    server_time_req = requests.get('https://api.binance.us/api/v3/time')
    server_time = int(server_time_req.json()['serverTime'])
    window_time_ago = int((datetime.fromtimestamp(server_time/1000) - timedelta(hours=window)).timestamp() * 1000)
    window_params = {
    "symbol": "BTCUSDT",
    "interval": "1h",
    "startTime": window_time_ago,
    "endTime": server_time
    }
    historical_price_req = requests.get('https://api.binance.us/api/v3/klines?', params=window_params)
    window_bars = pd.DataFrame(historical_price_req.json())
    window_bars.columns=['openTime', 'open', 'high', 'low', 'close', 'volume', 'closeTime', 'quoteVolume', 'numTrades', 'takerBase', 'takerVolume','unused']
    pct_change = (pd.Series(window_bars['close'].astype(float)).pct_change() * 100) + 1
    momentum = pct_change.product()-1
    return momentum

def get_current_price():
    current_price_req = float(requests.get('https://api.binance.us/api/v3/ticker/price?symbol=BTCUSDT').json()['price'])
    return current_price_req

def get_account_bal():
    get_account_req = account_info.binanceus_get_request(account_data_uri_path, account_params, os.getenv('PUBLIC_KEY'), os.getenv('PRIVATE_KEY'))
    current_balance = float(json.loads(get_account_req)['balances'][4]['free'])
    return current_balance

def get_open_orders():
    open_orders_req = account_info.binanceus_get_request(open_orders_uri, account_params, os.getenv('PUBLIC_KEY'), os.getenv('PRIVATE_KEY'))
    return json.loads(open_orders_req)

def long_order():
    current_price = get_current_price()
    quan = round(get_account_bal()*risk/current_price(), 5)
    sl_price = current_price * (1-risk)
    tp_price = current_price * (1+tp)
    print('{0:.5f}'.format(quan))
    market_order_params = {
        'symbol': 'BTCUSDT',
        'side': 'BUY',
        'type': 'MARKET',
        'quantity': '{0:.5f}'.format(quan),
        'timestamp': int(round(time.time() * 1000))
    }
    market_order_request = account_info.binanceus_post_request(order_uri_path, market_order_params, os.getenv('PUBLIC_KEY'), os.getenv('PRIVATE_KEY'))
    sl_order_params = {
        'symbol': 'BTCUSDT',
        'side': 'SELL',
        'type': 'STOP_LOSS_LIMIT',
        'quantity': '{0:.5f}'.format(quan),
        'price': sl_price,
        'timestamp': int(round(time.time() * 1000))
    }
    sl_order_request = account_info.binanceus_post_request(order_uri_path, sl_order_params, os.getenv('PUBLIC_KEY'), os.getenv('PRIVATE_KEY'))
    tp_order_params = {
        'symbol': 'BTCUSDT',
        'side': 'SELL',
        'type': 'TAKE_PROFIT_LIMIT',
        'quantity': '{0:.5f}'.format(quan),
        'price': tp_price,
        'timestamp': int(round(time.time() * 1000))
    }
    tp_order_request = account_info.binanceus_post_request(order_uri_path, tp_order_params, os.getenv('PUBLIC_KEY'), os.getenv('PRIVATE_KEY'))
    return market_order_request, sl_order_request, tp_order_request

def short_order():
    current_price = get_current_price()
    quan = round(get_account_bal()*risk/current_price(), 5)
    sl_price = current_price * (1+risk)
    tp_price = current_price * (1-tp)
    print('{0:.5f}'.format(quan))
    market_order_params = {
        'symbol': 'BTCUSDT',
        'side': 'SELL',
        'type': 'MARKET',
        'quantity': '{0:.5f}'.format(quan),
        'timestamp': int(round(time.time() * 1000))
    }
    market_order_request = account_info.binanceus_post_request(order_uri_path, market_order_params, os.getenv('PUBLIC_KEY'), os.getenv('PRIVATE_KEY'))
    sl_order_params = {
        'symbol': 'BTCUSDT',
        'side': 'BUY',
        'type': 'STOP_LOSS_LIMIT',
        'quantity': '{0:.5f}'.format(quan),
        'price': sl_price,
        'timestamp': int(round(time.time() * 1000))
    }
    sl_order_request = account_info.binanceus_post_request(order_uri_path, sl_order_params, os.getenv('PUBLIC_KEY'), os.getenv('PRIVATE_KEY'))
    tp_order_params = {
        'symbol': 'BTCUSDT',
        'side': 'BUY',
        'type': 'TAKE_PROFIT_LIMIT',
        'quantity': '{0:.5f}'.format(quan),
        'price': tp_price,
        'timestamp': int(round(time.time() * 1000))
    }
    tp_order_request = account_info.binanceus_post_request(order_uri_path, tp_order_params, os.getenv('PUBLIC_KEY'), os.getenv('PRIVATE_KEY'))
    return market_order_request, sl_order_request, tp_order_request

scheduler = BackgroundScheduler()
@scheduler.scheduled_job(IntervalTrigger(hours=1))
def event_loop():
    if len(get_open_orders()) < 3:
        momentum = get_momentum()
        print(momentum)
        if momentum > momentum_trigger:
            # Sell
            short_order()
        elif momentum < -momentum_trigger:
            #Buy
            long_order()

def main():
    scheduler.start()
    while True:
        pass

if __name__ == "__main__":
    main()