# -*- coding: utf-8 -*-
import scrapy
import csv


class MovieSpider(scrapy.Spider):
    name = 'movie'
    allowed_domains = ['mtime.com']
    start_urls = ['http://mtime.com/']

    def parse(self, response):
        self.readCsv()

    def readCsv(self):
        with open('movies.csv', 'r') as f:
            spamreader = csv.reader(f)
            for row in spamreader:
                print(", ".join(row))
