#!/usr/local/bin/python3


from bs4 import BeautifulSoup
from itertools import cycle
import os
import sys

root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from classes.Form import Form
from classes.Log import Log
from classes.Page import Page
from classes.Table import Table


class WebPage(Page):
    __captcha = None
    __form    = None
    __table   = None

    def __init__(self, prmUrl, prmHeaders={}, prmSession=False):
        super().__init__(prmUrl=prmUrl, prmHeaders=prmHeaders, prmSession=prmSession)
        parser = BeautifulSoup(self.content.text, "html.parser")
        self.form = Form(parser.find("form", {"method": "post"}), self)
        self.table = Table(parser.find("table", {"border": "1"}), self)

    def initSession(self):
        super().initSession()
        parser = BeautifulSoup(self.content.text, "html.parser")
        if self.form is not None:
            self.form.element = parser.find("form", {"method": "post"})
        if self.table is not None:
            self.table.element = parser.find("table", {"border": "1"})


    @property
    def captcha(self):
        return self.__captcha


    @captcha.setter
    def captcha(self, prmValue):
        self.__captcha = prmValue


    @property
    def form(self):
        return self.__form


    @form.setter
    def form(self, prmValue):
        self.__form = prmValue


    @property
    def table(self):
        return self.__table


    @table.setter
    def table(self, prmValue):
        self.__table = prmValue


    def post(self, prmIteration, prmData={}, prmProxyUrls={}):
        repeat = 0
        proxyPool = None
        if len(prmProxyUrls) > 0:
            proxies = list()
            for url in prmProxyUrls:
                dictB = self.getProxies(url)
                proxies = self.form.mergeTwoList(proxies, dictB)
            proxyPool = cycle(proxies)
            print("Url list length: {:d}".format(len(proxies)))

        while repeat < prmIteration:
            try:
                voteBefore = self.table.getVote(int(prmData["id"]))
                response = self.form.post(prmData=prmData, prmProxyPool=proxyPool)
                voteAfter = self.table.getVote(int(prmData["id"]))
                if voteAfter == voteBefore + 1:
                    repeat += 1
            except Exception as exception:
                log = Log()
                log.error(str(exception.args[0]))
