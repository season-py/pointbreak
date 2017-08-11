#!/usr/bin/env python
# coding=utf-8
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from settings import SETTINGS

class PhantomJsProxy(object):

    def __init__(self):
        self._driver = None

    @property
    def driver(self):
        if not self._driver:
            dcap = dict(DesiredCapabilities.PHANTOMJS)
            dcap['phantomjs.page.settings.userAgent'] = (SETTINGS['user_agent'])
            self._driver = webdriver.PhantomJS(SETTINGS['phantomjs_path'], desired_capabilities=dcap)
        return self._driver

    def fetch(self, url):
        self.driver.get(url)

    def get_page_source(self, url):
        self.fetch(url)
        return self.driver.page_source

    def get_cookies(self):
        return self.driver.get_cookies()

    def close(self):
        self.driver.close()

    def find_element_by_name(self, name):
        return self.driver.find_element_by_name(name)

phantomjs_proxy = PhantomJsProxy()
