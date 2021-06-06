#!/usr/local/bin/python3


from lxml.html import fromstring
import os
import requests
import sys
import validators

root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from classes.Table import Table
from classes.Log import Log


class Page:
    __content = None
    __headers = None
    __session = None
    __url     = None

    def __init__(self, prmUrl, prmHeaders={}, prmSession=False):
        self.headers = prmHeaders
        self.url = prmUrl
        if prmSession:
            self.initSession()
        else:
            self.content =  requests.get(self.url)


    @property
    def content(self):
        return self.__content


    @content.setter
    def content(self, prmValue):
        self.__content = prmValue


    @property
    def headers(self):
        return self.__headers


    @headers.setter
    def headers(self, prmValue):
        self.__headers = prmValue


    @property
    def session(self):
        return self.__session


    @session.setter
    def session(self, prmValue):
        self.__session = prmValue


    @property
    def url(self):
        return self.__url


    @url.setter
    def url(self, prmValue):
        if not validators.url(prmValue):
            raise ValueError("url should be a valid url")
        self.__url = prmValue


    def getProxies(self, prmUrl):
        try:
            response = requests.get(prmUrl)
            parser = fromstring(response.text)
            proxies = list()

            for tr in parser.xpath("//tbody/tr")[1:]:
                if tr.xpath(".//td[7][contains(text(), 'yes')]"):
                    address = ":".join([tr.xpath(".//td[1]/text()")[0], tr.xpath(".//td[2]/text()")[0]])
                    #proxies.add(address)
                    proxies.append(address)
            return proxies
        except Exception as exception:
            log = Log()
            log.error(str(exception.args[0]))


    def initSession(self):
        self.session = requests.session()
        self.content = self.session.get(self.url, headers=self.headers)
