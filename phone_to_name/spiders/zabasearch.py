# -*- coding: utf-8 -*-
import pandas as pd
import re
import scrapy
from bs4 import BeautifulSoup


class ZabasearchSpider(scrapy.Spider):
    name = 'zabasearch'
    # allowed_domains = ['www.zabasearch.com/']
    start_urls = ['https://www.zabasearch.com/phone/']

    def __init__(self):
        self.start_url = 'https://www.zabasearch.com/phone/'
        phone_numbers = pd.read_csv('source_files/phone_numbers.csv', header=None)
        phone_numbers.columns = ['Phone Numbers']
        self.parsed_phone_numbers = phone_numbers['Phone Numbers'].apply(lambda s: re.sub(r'\(|\)|\ |-', '', s))

    def parse(self, response):
        for number in self.parsed_phone_numbers:
            next_page_url = self.start_url + number
            yield response.follow(next_page_url, self.parse_search_results)

    def parse_search_results(self, response):
        search_results = response.xpath('//div[@id="searchResults"]//div[contains(@class, "result-person-info")]')
        phone = re.findall('[0-9]{10}', response.url)[0]
        if search_results:
            for result in search_results:
                person_details = self.parse_person_details(result, phone)
                yield person_details
        else:
            print('No result found')

    def parse_person_details(self, result, phone):
        item = {}
        item['Phone'] = phone
        for field in result.xpath('div')[:3]:
            key = BeautifulSoup(field.xpath('span')[0].get(),
                    'xml').text.strip(': ')
            value = BeautifulSoup(field.xpath('span')[1].get(),
                    'xml').text.strip()
            item[key] = value
        return item
