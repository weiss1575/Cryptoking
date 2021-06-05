import snscrape.modules.twitter as sntwitter
import re
import pandas_datareader as pdr
import datetime as dt
import matplotlib.pyplot as plt

def get_tweets():
    tweets = []
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper('from:@elonmusk + since:2021-01-01 until:2021-06-04').get_items()):
        tweet_date = str(tweet.date).split()[0]
        tweet_content = re.sub('[^A-Za-z0-9]+', ' ', tweet.content).lower()
        tweets.append([tweet_date, tweet_content])
    return tweets


def filter_tweets(tweets):
    BTC_KEYWORDS = ['Bitcoin', 'bitcoin', 'BITCOIN', 'btc', 'BTC', 'Btc']
    DOGE_KEYWORDS = ['Dogecoin', 'dogecoin', 'DOGECOIN', 'doge', 'DOGE', 'Doge']
    btc_tweets = []
    doge_tweets = []
    for tweet in tweets:
        for btc_word in BTC_KEYWORDS:
            if btc_word in tweet[1]:
                btc_tweets.append(tweet[0])
                break
        for doge_word in DOGE_KEYWORDS:
            if doge_word in tweet[1]:
                doge_tweets.append(tweet[0])
                break
    return btc_tweets, doge_tweets


def get_yahoo_finance_data():
    crypto_data = pdr.get_data_yahoo(['BTC-USD', 'DOGE-USD'], '2021-01-01', '2021-06-04')['Adj Close']
    return crypto_data


def plot_data(crypto_data, btc_dates, doge_dates):
    fig, ax1 = plt.subplots()
    ax1.set_title("CryptoKing", fontsize = 24)

    color = 'red'
    ax1.set_xlabel('Date', fontsize=16)
    ax1.set_ylabel('BTC-USD', color=color, fontsize=16)
    ax1.plot(crypto_data.index, crypto_data['BTC-USD'], color=color)
    ax1.tick_params(axis = 'both', which = 'major', labelsize = 12)
    ax2 = ax1.twinx()

    color = 'blue'
    ax2.set_ylabel('DOGE-USD', color=color, fontsize=16)
    ax2.plot(crypto_data.index, crypto_data['DOGE-USD'], color=color)
    ax2.tick_params(axis = 'both', which = 'major', labelsize = 12)

    for date in btc_dates:
        y = crypto_data.loc[date]['BTC-USD']
        ax1.scatter(dt.datetime.strptime(date, "%Y-%m-%d").date(), y, c='green', s=150, alpha=0.5)

    for date in doge_dates:
        y = crypto_data.loc[date]['DOGE-USD']
        ax2.scatter(dt.datetime.strptime(date, "%Y-%m-%d").date(), y, c='green', s=150, alpha=0.5)

    plt.show()


if __name__ == "__main__":
    cryptoking_tweets = get_tweets()
    btc_tweets, doge_tweets = filter_tweets(cryptoking_tweets)
    crypto_data = get_yahoo_finance_data()
    plot_data(crypto_data, btc_tweets, doge_tweets)