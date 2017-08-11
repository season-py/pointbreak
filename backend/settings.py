#!/usr/bin/env python
# coding=utf-8
import os

WORKSPACE = os.path.dirname(os.path.abspath(__file__))

SETTINGS = {
    'debug': True,
    'cookie_secret': '61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=',
    'xsrf_cookies': True,
    'autoreload': True,
    'login_url': '/login',
    'template_path': os.path.join(WORKSPACE, 'templates'),
    'static_path': os.path.join(WORKSPACE, 'static'),
    'media_path': os.path.join(WORKSPACE, 'media'),
    'database': os.path.join(WORKSPACE, 'db/point_break.sqlite'),
    'yb_account': 'haishan09@gmail.com',
    'yb_password': 'i3vTKyPlwLjm2GH3',
    'yb_access_key': 'an4Xo6J4nRisN5bCKEYxDbxSg3xw5K0WYCMWrxBc',
    'yb_secret_key': 'b0Uu3GhCeqLhQop7kBYCgFMKhGtNmHfUWCqu0hOx',
    'phantomjs_path': '/home/season/Workspace/point-break/phantomjs',
    'user_agent': 'Mozilla/5.0 (Linux; Android 5.1.1; Nexus 6 Build/LYZ28E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.23 Mobile Safari/537.36',
}

