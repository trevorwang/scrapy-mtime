# -*- coding: utf-8 -*-
import scrapy
import regex
import json
from parsel import Selector
import csv
import time

URL = "http://service.channel.mtime.com/service/search.mcs?Ajax_CallBack=true&Ajax_CallBackType=Mtime.Channel.Pages.SearchService&Ajax_CallBackMethod=SearchMovieByCategory&Ajax_CrossDomain=1&t=201832518553377686&Ajax_CallBackArgument0&Ajax_CallBackArgument1=0&Ajax_CallBackArgument2=0&Ajax_CallBackArgument3=0&Ajax_CallBackArgument4=0&Ajax_CallBackArgument5=0&Ajax_CallBackArgument6=0&Ajax_CallBackArgument7=0&Ajax_CallBackArgument8&Ajax_CallBackArgument9={0}&Ajax_CallBackArgument10={0}&Ajax_CallBackArgument14=1&Ajax_CallBackArgument16=1&Ajax_CallBackArgument17=4&Ajax_CallBackArgument18={1}&Ajax_CallBackArgument19=0"


class MtimeSpider(scrapy.Spider):
    tried_times = 0
    name = "mtime"
    urls = []

    def start_requests(self):

        for year in range(2011, 2017):
            for page in range(1, 101):
                self.urls.append(URL.format(year, page))

        for url in self.urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        self.parseData(response)

    def writeToCsv(self, data):
        with open('movies.csv', 'a') as f:
            fieldnames = ['title', 'link']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writerows(data)

    def parseData(self, response):
        matched = regex.search(r'({.*})', response.text)
        if (matched):
            jdata = json.loads(matched[0])
            try:
                html = jdata.get('value')['listHTML']
                data = self.html2Dict(html)
                self.writeToCsv(data)
            except KeyError:
                self.logger.error("An error has been occured!")
                url = response.request.url
                self.urls.insert(0, url)
                self.sleep()
            # self.log(html)
        else:
            self.logger.warn("There's something wrong!!!")

    def html2Dict(self, html):
        movieList = []
        sel = Selector(html)
        for e in sel.css('ul > li'):
            item = {}
            item['title'] = e.xpath('.//a/@title').extract_first()
            item['link'] = e.xpath('.//a/@href').extract_first()
            movieList.append(item)
        return movieList

    def sleep(self):
        if (self.tried_times >= 4):
            self.tried_times = 0
        self.tried_times += 1
        time.sleep(self.tried_times * 300)
