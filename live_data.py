import requests

server_time_req = requests.get('https://api.binance.us/api/v3/time')
server_time = int(server_time_req.json()['serverTime'])

params = {
    "symbol": "BTCUSDT",
    "interval": "5m",
    "startTime": 0,
    "endTime": server_time
}

r = requests.get('https://api.binance.us/api/v3/klines?', params=params)
print(len(r.json()))