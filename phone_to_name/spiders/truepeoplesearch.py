# -*- coding: utf-8 -*-
import pandas as pd
import re
import scrapy
from bs4 import BeautifulSoup

class TruepeoplesearchSpider(scrapy.Spider):
    name = 'truepeoplesearch'
    # allowed_domains = ['truepeoplesearch.com']
    start_urls = ['http://truepeoplesearch.com/']

    def parse(self, response):
        pass
