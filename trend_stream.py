# -*- coding: utf-8 -*-
# Fork : http://qiita.com/yoppe/items/3e61fd567ae1d4c40a96
from pytz import timezone
from dateutil import parser
from datetime import datetime
from elasticsearch import Elasticsearch
from twitter import Twitter, TwitterStream, OAuth
from threading import Timer, get_ident

# https://apps.twitter.com/ でTwitterアプリを登録して取得したOAuthキーを設定。
OAUTH_INFO = dict(
    token="##TOKEN##",
    token_secret="##TOKEN_SECRET##",
    consumer_key="##CONSUMER_KEY##",
    consumer_secret="##CONSUMER_SECRET##")

STREAM_INFO = dict(
    timeout=600,
    block=False,
    heartbeat_timeout=600) # デフォルトだと90秒でストリーム維持のためのheartbeatが飛んで来るので10分に設定

JST = timezone('Asia/Tokyo')
WOEID_JP = 23424856 # 日本のWOEID
ELASTICSEARCH_IP = '##IP_ADDRESS##'

class TwitterTrendStream():

    def __init__(self):
        self.__current_thread_ident = None
        self.__oauth = OAuth(**OAUTH_INFO)
        #self.__es = Elasticsearch()
        self.__es = Elasticsearch([ELASTICSEARCH_IP])

    def __fetch_trands(self, twitter):
        response = twitter.trends.place(_id=WOEID_JP)
        return [trend["name"] for trend in response[0]["trends"]]

    def __fetch_filter_stream(self, twitter_stream, track_list):
        track = ",".join(track_list)
        return twitter_stream.statuses.filter(track=track)

    def run(self):
        self.__current_thread_ident = get_ident() # 現在の実行スレッドIDを登録
        Timer(300, self.run).start()              # ５分後に新たなスレッドを開始

        twitter = Twitter(auth=self.__oauth)
        twitter_stream = TwitterStream(auth=self.__oauth, **STREAM_INFO)

        trend_list = self.__fetch_trands(twitter)
        tweet_iter = self.__fetch_filter_stream(twitter_stream, trend_list)

        for tweet in tweet_iter:
            if "limit" in tweet: # 取得上限超えた時にくるLimit Jsonは無視
                continue
