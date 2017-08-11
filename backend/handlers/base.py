#!/usr/bin/env python
# coding=utf-8
from tornado import web
from tornado.httpclient import HTTPClient, AsyncHTTPClient

from settings import SETTINGS
from utils.phantomjs_proxy import phantomjs_proxy


class BaseHandler(web.RequestHandler):

    def __init__(self, application, request, **kwargs):
        self.phantomjs_proxy = phantomjs_proxy
        super(BaseHandler, self).__init__(application, request, **kwargs)

    @property
    def async_http_client(self):
        cli = AsyncHTTPClient(
            force_instance=True,
            defaults=dict(user_agent=SETTINGS['user_agent']))
        return cli

    @property
    def http_client(self):
        cli = HTTPClient(
            force_instance=True,
            defaults=dict(user_agent=SETTINGS['user_agent']))
        return cli

