# Get api key

import requests
import time
import os
from os.path import join, dirname
from dotenv import load_dotenv
import time
import pandas as pd
from datetime import datetime
import urllib.request
import zipfile

dates = pd.date_range(start="2021-01-14",end="2024-07-02").strftime("%Y-%m-%d").to_list()

for day in dates:
    url = "https://data.binance.us/public_data/spot/daily/klines/BTCUSDC/1h/BTCUSDC-1h-" + day + ".zip"
    print(url)
    #urllib.request.urlretrieve(url, "thing.zip")
    req = requests.get(url)
    f = open("zips/"+day+".zip", 'wb')
    f.write(req.content)
    f.close()

    try:
        with zipfile.ZipFile("zips/"+day+".zip", 'r') as zip_ref:
            zip_ref.extractall("/Users/RyanHaver/Projects/cryptoStrategies/data/")
    except zipfile.BadZipFile:
        continue

# load_dotenv()

# SECRET_KEY = os.environ.get("PUBLIC")

# server_time_req = requests.get('https://api.binance.us/api/v3/time')
# server_time = int(server_time_req.json()['serverTime'])
# print(server_time)

# id_json = {
#     "symbol": "BTCUSDT",
#     "limit": 1
# }

# most_recent_id_request = requests.get('https://api.binance.us/api/v3/trades?', params=id_json)
# most_recent_id = most_recent_id_request.json()[0]['id']

# headers = {}
# headers['X-MBX-APIKEY'] = SECRET_KEY

# for i in range(1, most_recent_id, 1000):
#     history_json = {
#         "symbol": "BTCUSDT",
#         "limit": 1000,
#         "fromId": i
#     }

#     resp = requests.get('https://api.binance.us/api/v3/historicalTrades?', params=history_json, headers=headers)

#     for trade in resp.json():
#         print(trade['id'])
#     time.sleep(2)


