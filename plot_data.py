import pandas_datareader as pdr
import datetime as dt
import matplotlib.pyplot as plt
import json

btc_data = pdr.get_data_yahoo(['BTC-USD', 'DOGE-USD'], '2021-01-01', '2021-06-01')['Adj Close']

fig, ax1 = plt.subplots()
ax1.set_title("CryptoKing", fontsize = 24)

color = 'red'
ax1.set_xlabel('Date', fontsize=16)
ax1.set_ylabel('BTC-USD', color=color, fontsize=16)
ax1.plot(btc_data.index, btc_data['BTC-USD'], color=color)
ax1.tick_params(axis = 'both', which = 'major', labelsize = 12)
ax2 = ax1.twinx()

color = 'blue'
ax2.set_ylabel('DOGE-USD', color=color, fontsize=16)
ax2.plot(btc_data.index, btc_data['DOGE-USD'], color=color)
ax2.tick_params(axis = 'both', which = 'major', labelsize = 12)

with open('btc.json') as fh:
    btc_dates = json.load(fh)

with open('doge.json') as fh:
    doge_dates = json.load(fh)

for date in btc_dates:
    y = btc_data.loc[date]['BTC-USD']
    ax1.scatter(dt.datetime.strptime(date, "%Y-%m-%d").date(), y, c='green', s=150, alpha=0.5)

for date in doge_dates:
    y = btc_data.loc[date]['DOGE-USD']
    ax2.scatter(dt.datetime.strptime(date, "%Y-%m-%d").date(), y, c='green', s=150, alpha=0.5)

plt.show()