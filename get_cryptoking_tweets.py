import snscrape.modules.twitter as sntwitter
import json
import re

tweets = []
for i, tweet in enumerate(sntwitter.TwitterSearchScraper('from:@elonmusk + since:2021-01-01 until:2021-06-01').get_items()):
    tweet_date = str(tweet.date).split()[0]
    tweet_content = re.sub('[^A-Za-z0-9]+', ' ', tweet.content).lower()
    tweets.append([tweet_date, tweet_content])
with open('tweets.json', 'w', encoding='utf-8') as fh:
   json.dump(tweets, fh, ensure_ascii=False)


BTC_KEYWORDS = ['Bitcoin', 'bitcoin', 'BITCOIN', 'btc', 'BTC', 'Btc']
DOGE_KEYWORDS = ['Dogecoin', 'dogecoin', 'DOGECOIN', 'doge', 'DOGE', 'Doge']
btc_tweets = []
doge_tweets = []
with open('tweets.json', encoding='utf-8') as fp:
    data = json.load(fp)
for tweet in data:
    for btc_word in BTC_KEYWORDS:
        if btc_word in tweet[1]:
            btc_tweets.append(tweet[0])
            break
    for doge_word in DOGE_KEYWORDS:
        if doge_word in tweet[1]:
            doge_tweets.append(tweet[0])
            break
with open('doge.json', 'w', encoding='utf-8') as fh:
    json.dump(doge_tweets, fh)
with open('btc.json', 'w', encoding='utf-8') as fh:
    json.dump(btc_tweets, fh)