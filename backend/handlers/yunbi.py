#!/usr/bin/env python
# coding=utf-8
import json
import hmac
import time
import hashlib
from datetime import datetime
from urllib import urlencode
from collections import OrderedDict
from pony.orm import select, db_session
from tornado import gen
from tornado.web import asynchronous
from tornado.httpclient import HTTPRequest

from utils.urlmap import urlmap
from models import Coin, CoinYunbiShot
from settings import SETTINGS
from handlers.base import BaseHandler

BaseUri = 'https://yunbi.com'
AccessKey = SETTINGS['yb_access_key']
SecretKey = SETTINGS['yb_secret_key']


class SignMixin(BaseHandler):

    signin_uri = '/signin'
    auth_uri = '/auth/identity/callback'

    def ensure_authenticated(self):
        self.auth()

    def auth(self):
        self.phantomjs_proxy.fetch(BaseUri + self.signin_uri)
        token_element = self.phantomjs_proxy.find_element_by_name('authenticity_token')
        token = token_element.get_attribute('value')
        body = {
            'authenticity_token': token,
            'auth_key': SETTINGS['yb_account'],
            'password': SETTINGS['yb_password'],
            'commit': u'登录',
        }
        request = HTTPRequest(
            url=BaseUri + self.auth_uri,
            method='POST',
            body=json.dumps(body),
            validate_cert=False,
            request_timeout=60,
            follow_redirects=False,
        )
        response = self.http_client.fetch(request)
        print response.code, response.body, response.headers

    def get_tonce(self):
        return int(1000 * time.time())

    def urlencode(self, params):
        ordered_params = OrderedDict()
        for k, v in sorted(params.items(), key=lambda kv: kv[0]):
            ordered_params[k] = v
        return urlencode(ordered_params)

    def sign(self, method, path, params):
        params.update({'tonce': self.get_tonce(), 'access_key': AccessKey})
        query = self.urlencode(params)
        messge = '|'.join([method, path, query])
        signature = hmac.new(SecretKey, msg=messge, digestmod=hashlib.sha256).hexdigest()
        return '{0}&signature={1}'.format(query, signature)

@urlmap(url=r'/yunbi/ticker')
class TickerHandler(SignMixin):

    ticker_uri = '/api/v2/tickers.json'

    @asynchronous
    @gen.coroutine
    def get(self):
        yield self.async_http_client.fetch(
            BaseUri + self.ticker_uri, self.callback)

    def callback(self, response):
        jsonify_ticker = json.loads(response.body)
        with db_session:
            for symbol, ticker in jsonify_ticker.items():
                symbol = symbol.strip('cny')
                price = ticker['ticker']['last']
                volume = ticker['ticker']['vol']
                shotted_at = ticker['at']
                coin = select(c for c in Coin if c.symbol == symbol).get()
                if not coin:
                    continue
                CoinYunbiShot(
                    coin=coin,
                    price=price, 
                    volume=volume, 
                    shotted_at=datetime.fromtimestamp(shotted_at))
        self.finish()


@urlmap(url=r'/yunbi/deposits')
class DepositHandler(SignMixin):

    deposits_uri = '/api/v2/deposits.json'

    @asynchronous
    @gen.coroutine
    def get(self):
        params = {'currency': 'btc'}
        query = self.sign('GET', self.deposits_uri, params)
        uri = BaseUri + self.deposits_uri + '?' + query
        yield self.async_http_client.fetch(
            uri, self.callback)

    def callback(self, response):
        jsonify_deposits = json.loads(response.body)
        print jsonify_deposits
        self.finish()


@urlmap(url=r'/yunbi/trades')
class TradeHandler(SignMixin):

    deposits_uri = '/api/v2/trades/my.json'

    @asynchronous
    @gen.coroutine
    def get(self):
        self.ensure_authenticated()
        params = {'market': 'btccny'}
        query = self.sign('GET', self.deposits_uri, params)
        uri = BaseUri + self.deposits_uri + '?' + query
        yield self.async_http_client.fetch(
            uri, self.callback)

    def callback(self, response):
        jsonify_deposits = json.loads(response.body)
        print jsonify_deposits
        self.finish()


@urlmap(url=r'/yunbi/user_profile')
class UserProfileHandler(SignMixin):

    deposits_uri = '/api/v2/members/me.json'

    @asynchronous
    @gen.coroutine
    def get(self):
        params = {}
        query = self.sign('GET', self.deposits_uri, params)
        uri = BaseUri + self.deposits_uri + '?' + query
        yield self.async_http_client.fetch(
            uri, self.callback)

    def callback(self, response):
        jsonify_deposits = json.loads(response.body)
        print jsonify_deposits
        self.finish()
