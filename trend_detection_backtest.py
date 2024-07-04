from backtesting import Backtest, Strategy
from backtesting.lib import plot_heatmaps
import pandas as pd
import numpy as np
import multiprocessing as mp
mp.set_start_method('fork')

class Momentum(Strategy):
    window = 9 # from optimizer
    momentum_trigger = 14 # from optimizer
    risk = 0.01
    tp = 0.02

    def init(self):
        pass

    def next(self):
        #print(len(self.data.Close))
        #print(type(self.data.Close))
        #input()
        if len(self.data.Close) > self.window:
            pct_change = self.data.Close[-self.window:].s.pct_change()*100+1
            momentum = pct_change.product()-1
            #print(self.data.Close[-self.window:], momentum)
            #input()
            if momentum > self.momentum_trigger:
                # Sell order
                #print("SELL")
                currentPrice = self.data.Close[-1]
                size = round((self.equity * self.risk) / currentPrice)
                sl = currentPrice * (1+self.risk)
                tp = currentPrice * (1-self.tp)
                #print(f"SELL ORDER: Price={currentPrice}, Size={size}, SL={sl}, TP={tp}")
                order = self.sell(size=size, sl=sl, tp=tp)
                #print("Self.equity", self.equity)
                #print("equity times risk", self.equity * self.risk)
                #print(self.position.pl)
                #print(self.position.size)
                #print(order.size, order.sl, order.tp)
                
            if momentum < -self.momentum_trigger:
                # Buy order
                #print("BUY")
                currentPrice = self.data.Close[-1]
                size = round((self.equity * self.risk) / currentPrice)
                sl = currentPrice * (1-self.risk)
                tp = currentPrice * (1+self.tp)
                #print("Self.equity", self.equity)
                #print(f"BUY ORDER: Price={currentPrice}, Size={size}, SL={sl}, TP={tp}")
                order = self.buy(size=size, sl=sl, tp=tp)
                #print(self.position.pl)
                #print(self.position.size)
                #print("Self.equity", self.equity)
                #print(order.size, order.sl, order.tp)
            #print(self.orders)
            #print(self.closed_trades)
                


full_data = pd.read_csv("full_data.csv")
full_data['open_time'] = pd.to_datetime(full_data['open_time'], unit='ms')
full_data.set_index('open_time', inplace=True)
full_data.drop(columns=['close_time', 'count', 'taker_buy_base_volume', 'taker_buy_quote_volume', 'quote_volume'], inplace=True)
full_data.columns = ['Open', 'High', 'Low', 'Close', 'Volume']

full_data = (full_data / 100).assign()  # μBTC OHLC prices
#print(full_data)
#input()

bt = Backtest(full_data, Momentum,cash=100000,exclusive_orders=True)
output = bt.run()
print(output)

stats, heatmap = bt.optimize(window=range(6,24,1), 
                    momentum_trigger=range(5,25,1),
                    risk=[0.01,0.02,0.03,0.04],
                    tp=[0.02,0.03,0.04,0.05],
                    return_heatmap = True,
                    )
print(stats)
print(stats._strategy)
print(heatmap)
plot_heatmaps(heatmap, agg='mean')
#bt.plot()