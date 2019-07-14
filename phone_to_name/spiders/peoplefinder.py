# -*- coding: utf-8 -*-
import pandas as pd
import re
import scrapy
from bs4 import BeautifulSoup


class PeoplefinderSpider(scrapy.Spider):
    name = 'peoplefinder'
    # allowed_domains = ['peoplefinder.com']
    start_urls = ['http://peoplefinder.com/']

    def __init__(self):
        self.start_url = 'http://peoplefinder.com/reverse-phone-search/'
        phone_numbers = pd.read_csv('source_files/phone_numbers.csv', header=None)
        phone_numbers.columns = ['Phone Numbers']
        self.parsed_phone_numbers = phone_numbers['Phone Numbers'].apply(lambda s: re.sub(r'\(|\)|\ |-', '', s))

    def parse(self, response):
        for number in self.parsed_phone_numbers:
            self.phone_number = number
            next_page_url = self.start_url + number
            yield response.follow(next_page_url, self.parse_search_results)

    def parse_search_results(self, response):
        # TODO: Replace with xpath specific to peoplefinder
        # search_results = response.xpath('//div[@id="searchResults"]//div[contains(@class, "result-person-info")]')
        if search_results:
            for result in search_results:
                person_details = self.parse_person_details(result)
                yield person_details
        else:
            print('No result found')

    def parse_person_details(self, result):
        item = {}
        item['Phone'] = self.phone_number
        # TODO: Replace with xpaths specific to peoplefinder
        # for field in result.xpath('div')[:3]:
            # key = BeautifulSoup(field.xpath('span')[0].get(),
                    # 'xml').text.strip(': ')
            # value = BeautifulSoup(field.xpath('span')[1].get(),
                    # 'xml').text.strip()
            # item[key] = value
        return item
