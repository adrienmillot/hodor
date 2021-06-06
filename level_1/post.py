#!/usr/bin/python3


import os
import sys

root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from classes.WebPage import WebPage

url = "http://158.69.76.135/level1.php"
webPage = WebPage(prmUrl=url, prmSession=True)

webPage.post(4096, {"id": 2701})
