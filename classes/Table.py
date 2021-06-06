#!/usr/local/bin/python3


from lxml.html import fromstring
import os
import requests
import sys


root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from classes.WebComponent import WebComponent
from bs4.element import PageElement


class Table(WebComponent):

    def __init__(self, prmElement: PageElement, prmParentELement):
        super().__init__(prmElement, prmParentELement)

    def getVote(self, prmId):
        content = requests.get(self.webPage.url)
        parser = fromstring(content.text)
        for tr in parser.xpath("//table/tr"):
            if tr.xpath(".//td[1][contains(text(), '" + str(prmId) + "')]"):
                vote = tr.xpath("./td[2]/text()")[0]
                return int(vote)

        return -1
