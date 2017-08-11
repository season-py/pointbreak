#!/usr/bin/env python
# coding=utf-8
import json
from pony.orm import select, db_session
from tornado import web, gen
from tornado.web import asynchronous
from tornado.httpclient import AsyncHTTPClient

from utils.urlmap import urlmap
from models import Coin, CoinMarketCapShot
from celery_tasks import tasks

@urlmap(url=r'/coinmarketcap/coins')
class CoinsHandler(web.RequestHandler):

    coins_uri = 'https://files.coinmarketcap.com/generated/search/quick_search.json'

    @asynchronous
    @gen.coroutine
    def get(self):
        cli = AsyncHTTPClient()
        yield cli.fetch(self.coins_uri, self.callback)

    def callback(self, response):
        jsonify_coins = json.loads(response.body)
        for coin_inf in jsonify_coins:
            symbol = coin_inf['symbol'].lower()
            name = coin_inf['name'].lower()
            rank = coin_inf['rank']
            with db_session:
                coin = select(c for c in Coin if c.symbol == symbol).get()
                if not coin:
                    coin = Coin(symbol=symbol, full_name=name, rank=rank)
        self.finish()


@urlmap(url=r'/coinmarketcap/ticker')
class CoinsHandler(web.RequestHandler):

    coins_uri = 'https://files.coinmarketcap.com/generated/search/quick_search.json'
    coin_icon_uri = 'https://files.coinmarketcap.com/static/img/coins/32x32/{}.png'
    media_dir = '/home/season/Workspace/pointbreak/backend/media/icons/'

    @asynchronous
    @gen.coroutine
    def get(self):
        cli = AsyncHTTPClient()
        yield cli.fetch(self.coins_uri, self.callback)

    def callback(self, response):
        jsonify_coins = json.loads(response.body)
        for coin_inf in jsonify_coins:
            symbol = coin_inf['symbol'].lower()
            name = coin_inf['name'].lower()
            rank = coin_inf['rank']
            with db_session:
                coin = select(c for c in Coin if c.symbol == symbol).get()
                if not coin:
                    coin = Coin(symbol=symbol, full_name=name, rank=rank)
                    tasks.fetch_icon.apply_async(
                        (self.coin_icon_uri.format(name.replace(' ', '-')), self.media_dir + symbol + '.png')
                    )
        self.finish()

