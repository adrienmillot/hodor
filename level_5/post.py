#!/usr/bin/python3


import os
import sys

root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from classes.WebPage import WebPage

url = "http://158.69.76.135/level5.php"
headers = {"referer": url, "User-Agent": "Mozilla/5.0 (Windows NT 6.1) Gecko/20100101 Firefox/88.0.1"}
webPage = WebPage(prmUrl=url, prmHeaders=headers, prmSession=True)

webPage.post(1024, {"id": 2701})
