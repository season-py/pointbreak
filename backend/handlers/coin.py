#!/usr/bin/env python
# coding=utf-8
from pony.orm import db_session
from tornado import gen
from tornado.web import asynchronous

from utils.urlmap import urlmap
from models import Coin
from handlers.base import BaseHandler


@urlmap(url=r'/coins')
class TickerHandler(BaseHandler):

    @asynchronous
    @gen.coroutine
    def get(self):
        coins = []
        with db_session:
            for coin in Coin.select():
                coins.append({
                    'symbol': coin.symbol,
                    'full_name': coin.full_name,
                    'description': coin.description,
                })
        self.finish({'coins': coins})

