# -*- coding: utf-8 -*-
import pandas as pd
import re
import scrapy
from bs4 import BeautifulSoup


PROXY_URL = ''
AREA_CODES = ['980', '704']
FILTER_BY_AREA_CODE = True


class PeoplefinderSpider(scrapy.Spider):
    name = 'peoplefinder'
    # allowed_domains = ['peoplefinder.com']
    start_urls = ['http://peoplefinder.com/']

    def __init__(self):
        self.start_url = PROXY_URL + 'http://peoplefinder.com/reverse-phone-search/'
        phone_numbers = pd.read_csv('source_files/phone_numbers.csv', header=None)
        phone_numbers.columns = ['Phone Numbers']
        if FILTER_BY_AREA_CODE:
            phone_numbers = phone_numbers[phone_numbers['Phone Numbers'].apply(lambda x:
                    x[1:4] == '980' or x[1:4] == '704')]
        self.parsed_phone_numbers = phone_numbers['Phone Numbers'].apply(
                lambda s: re.sub(r'\(|\)|\ |-', '', s)
                )

    def parse(self, response):
        for number in self.parsed_phone_numbers:
            next_page_url = self.start_url + number
            yield response.follow(next_page_url, self.parse_search_results)

    def parse_search_results(self, response):
        single_result = response.xpath('//li[contains(@class, "detailUserInfoWrapper")]')
        # TODO: This only works for peoplefinder, truepeoplesearch and zabasearch
        phone = re.findall('[0-9]{10}', response.url)[0]
        if single_result:
            item = {}
            item['Phone'] = phone
            item['Name'] = response.xpath(
                    '//div[contains(@class, "detail-user-info")]/span[contains(@class, "detailNameHilite")]/text()'
                    ).get()
            item['Address'] = ', '.join(
                    response.xpath('//div[contains(@class, "detail-user-info")]/text()').extract()
                    )
            yield item
        else:
            search_results = response.xpath(
                    '//div[contains(@class, "ticklerResultsWrapper")]/'
                    'div[contains(@class, "ticklerResultsData")]'
                    )
            if search_results:
                for result in search_results:
                    person_details = self.parse_person_details(result, phone)
                    yield person_details
            else:
                print('No result found')

    def parse_person_details(self, result, phone):
        item = {}
        item['Phone'] = phone
        item['Name'] = result.xpath(
                'div//span[contains(@class, "ticklerResultsName")]/a/text()'
                ).get()
        item['Address'] = ', '.join(
                result.xpath(
                    'div[contains(@class, "ticklerResultsColAddr")]/text()'
                    ).extract()
                ).strip()
        return item
