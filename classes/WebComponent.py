#!/usr/local/bin/python3

import os
import sys

root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)


from bs4.element import PageElement


class WebComponent:
    __element = None
    __webPage = None

    def __init__(self, prmElement: PageElement, prmParentELement):
        self.element = prmElement
        self.webPage = prmParentELement


    @property
    def element(self) -> PageElement:
        return self.__element


    @element.setter
    def element(self, prmValue):
        self.__element = prmValue


    @property
    def webPage(self):
        return self.__webPage


    @webPage.setter
    def webPage(self, prmValue):
        self.__webPage = prmValue
