import snscrape.modules.twitter as sntwitter
import re
import pandas_datareader as pdr
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
import numpy as np

def get_tweets():
    '''
    Uses snscrape to retrieve all of Elons tweets from 2021. Twitter API was not used because of the current limitations of 3200 tweets going back only 1 week
    Returns tweets, a list of tweets
    '''
    tweets = []
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper('from:@elonmusk + since:2021-01-01 until:2021-06-04').get_items()):
        tweet_date = str(tweet.date).split()[0]
        tweet_content = re.sub('[^A-Za-z0-9]+', ' ', tweet.content).lower()
        tweets.append([tweet_date, tweet_content])
    return tweets


def filter_tweets(tweets):
    '''
    Filters and seperates tweets based on bitcoin and doge keywords.
    Returns btc_tweets, a list of tweets containing bitcoin keywords, and doge_tweets, a list of tweets containing dogecoin keywords.
    '''
    BTC_KEYWORDS = ['bitcoin', 'btc']
    DOGE_KEYWORDS = ['dogecoin', 'doge']
    btc_tweets = []
    doge_tweets = []
    for tweet in tweets:
        if any([btc_word in tweet[1] for btc_word in BTC_KEYWORDS]):
            btc_tweets.append(tweet[0])
        if any([doge_word in tweet[1] for doge_word in DOGE_KEYWORDS]):
            doge_tweets.append(tweet[0])
    return btc_tweets, doge_tweets


def get_yahoo_finance_data():
    '''
    Uses pandas datareader to get bitcoin and dogecoin price data directly from yahoo finance.
    Returns crypto_data, a dataframe containing all of the price data for btc and doge.
    '''
    crypto_data = pdr.get_data_yahoo(['BTC-USD', 'DOGE-USD'], '2021-01-01', '2021-06-04')['Adj Close']
    return crypto_data


def plot_data(crypto_data, btc_dates, doge_dates):
    '''
    Uses matplotlib to plot price data as well as points where elon tweeted about the currency
    '''

    plt.style.use('dark_background')
    # Make plot and set title
    fig, ax1 = plt.subplots(figsize = (15, 9))
    ax1.set_title("CryptoKing", fontsize = 24)

    # Add x-axis minor ticks and format
    fmt_day = mdates.DayLocator()
    ax1.xaxis.set_minor_locator(fmt_day)
    fig.autofmt_xdate()

    # Bitcoin Price plot
    color = 'red'
    ax1.set_xlabel('Date', fontsize=16)
    ax1.set_ylabel('BTC-USD', color=color, fontsize=16)
    ax1.plot(crypto_data.index, crypto_data['BTC-USD'], color=color)
    ax1.tick_params(axis = 'both', which = 'major', width=2, length=6, labelsize = 16)
    ax1.yaxis.set_minor_locator(AutoMinorLocator())

    # Dogecoin Price plot
    ax2 = ax1.twinx()
    color = 'blue'
    ax2.set_ylabel('DOGE-USD', color=color, fontsize=16)
    ax2.plot(crypto_data.index, crypto_data['DOGE-USD'], color=color)
    ax2.tick_params(axis = 'both', which = 'major', width=2, length=6, labelsize = 16)
    ax2.yaxis.set_minor_locator(AutoMinorLocator())

    # Plot Elons BTC tweets as scatter points
    x = [dt.datetime.strptime(date, "%Y-%m-%d").date() for date in btc_dates]
    y = [crypto_data.loc[date]['BTC-USD'] for date in btc_dates]
    ax1.scatter(x, y, c='yellow', s=200, alpha=0.7, marker='x', label = 'Elon Tweet')

    # Plot Elons Doge tweets as scatter points
    x = [dt.datetime.strptime(date, "%Y-%m-%d").date() for date in doge_dates]
    y = [crypto_data.loc[date]['DOGE-USD'] for date in doge_dates]
    ax2.scatter(x, y, c='yellow', s=200, alpha=0.7, marker='x')

    ax1.legend(fontsize=12)
    plt.show()


if __name__ == "__main__":
    cryptoking_tweets = get_tweets()
    btc_tweets, doge_tweets = filter_tweets(cryptoking_tweets)
    crypto_data = get_yahoo_finance_data()
    plot_data(crypto_data, btc_tweets, doge_tweets)