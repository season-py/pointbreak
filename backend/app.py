#!/usr/bin/env python
# coding=utf-8
import handlers
import tornado
from tornado import web
from tornado import ioloop
from tornado import httpserver
from tornado import log
from settings import SETTINGS
from utils.urlmap import urlmap

handlers.initiate()
log.logging.basicConfig(level=log.logging.INFO)


def runserver():
    log.logging.info(urlmap.handlers)
    _handlers = urlmap.handlers[0] + [
        (r'/media/(.*)', tornado.web.StaticFileHandler, {'path': SETTINGS['media_path']}),
    ]
    application = web.Application(_handlers, **SETTINGS)
    http_server = httpserver.HTTPServer(application)
    http_server.listen(8080)
    ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    runserver()
