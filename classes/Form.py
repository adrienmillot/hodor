#!/usr/local/bin/python3

from datetime import datetime
import os
from typing import Dict
import requests
import sys
import pytesseract
from urllib.parse import urlparse

root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from classes.Log import Log
from classes.WebComponent import WebComponent
from bs4.element import PageElement


class Form(WebComponent):

    def __init__(self, prmElement: PageElement, prmParentELement):
        super().__init__(prmElement, prmParentELement)


    def __getValues(self):
        values = {}

        if self.__hasKey() is True:
            values["key"] = self.key.get("value")

        if self.__hasCaptcha() is True:
            values["captcha"] = self.captcha


        values[self.submit().get("name")] = "submit"

        return values


    @property
    def captcha(self) -> PageElement:
        response = self.webPage.session.get(self.__captchaUrl())
        file = open("captcha.png", "wb")
        file.write(response.content)
        file.close()
        value = pytesseract.image_to_string("captcha.png").strip()
        os.remove("captcha.png")
        return value

    def __captchaUrl(self):
        domain = urlparse(self.webPage.url).netloc
        captcha = self.element.find("img")

        if captcha is None:
            return None

        return "http://" + domain + "/captcha.php"


    @property
    def key(self) -> PageElement:
        return self.element.find("input", {"name": "key"})


    def submit(self) -> PageElement:
        return self.element.find("input", {"type": "submit"})


    def __hasCaptcha(self):
        element = self.element.find("img")

        if element is None:
            return False

        return True


    def __hasKey(self):
        element = self.element.find("input", {"name": "key"})

        if element is None:
            return False

        return True


    def post(self, prmData={}, prmProxyPool=None):
        try:
            data = self.__getValues()

            if len(prmData) > 0:
                data = self.__mergeTwoDicts(data, prmData)

            if self.webPage.session is not None:
                response = self.__sessionPost(prmData=data, prmProxyPool=prmProxyPool)
                self.webPage.initSession()
            else:
                response = self.__defaultPost(prmData=data)

            return response
        except Exception as exception:
            log = Log()
            log.error(str(exception.args[0]))


    def __mergeTwoDicts(self, prmDicA, prmDicB):
        if type(prmDicA) is not dict:
            raise TypeError("DicA should be a dictionary")
        if type(prmDicB) is not dict:
            raise TypeError("DicB should be a dictionary")

        z = prmDicA.copy()
        z.update(prmDicB)

        return z


    def mergeTwoList(self, prmListA, prmListB):
        return prmListA + prmListB


    def __defaultPost(self, prmData={}, prmTimeout=5):
        try:
            response = requests.post(self.webPage.url, headers=self.webPage.headers, data=prmData, timeout=prmTimeout)
            self.__printResponse(response)

            return response
        except Exception as exception:
            log = Log()
            log.error(str(exception.args[0]))


    def __sessionPost(self, prmData={}, prmTimeout=5, prmProxyPool=None):
        log = Log()
        try:
            if prmProxyPool is not None:
                proxy = next(prmProxyPool)
                self.webPage.session.proxies = {"http": "http://" + proxy, "https": "https://" + proxy}

            response = self.webPage.session.post(self.webPage.url, headers=self.webPage.headers, data=prmData, timeout=prmTimeout)
            self.__printResponse(response)

            return response
        except TimeoutError as exception:
            log.warning(str(exception.args[0]))
        except Exception as exception:
            log.error(str(exception.args[0]))

    def __printResponse(self, prmResponse):
        log = Log()
        if prmResponse.status_code == 200:
            log.info("Request was executed in {:0.2f}s".format(prmResponse.elapsed.total_seconds()))
        else:
            log.warning("Failed request was executed in {:0.2f}s".format(prmResponse.elapsed.total_seconds()))

