# -*- coding: utf-8 -*-
import scrapy
import csv
from new.items import Movie
import datetime


class MovieSpider(scrapy.Spider):
    name = 'movie'
    allowed_domains = ['mtime.com']
    start_urls = []
    data_file = "{}.csv".format(datetime.datetime.now().isoformat())

    def __init__(self):
        self.readCsv()
        # self.start_urls.append('http://movie.mtime.com/105799/')

    def parse(self, response):
        movie = Movie()
        movie['name'] = response.css('div.db_head')[
            0].css('h1::text').extract_first()
        movie['year'] = response.css('div.db_head').css(
            'p.db_year').css('a::text').extract_first()
        movie['english_name'] = response.css('div.db_head').css(
            'p.db_enname::text').extract_first()
        movie['length'] = response.css(
            'div.db_head').css('span::text').extract_first()
        genres = response.css('div.db_head').css('div.otherbox').css(
            'a[property*=genre]::text').extract()
        movie['genres'] = ' '.join(genres)
        movie['release_date'] = response.css('div.db_head div.otherbox').css(
            'a[property*=initialReleaseDate]::text').extract_first()
        movie['location'] = response.css('div.db_head').css(
            'div.otherbox::text')[-1].extract()
        movie['director'] = response.css(
            'a[rel*=directedBy]::text').extract_first()
        movie['company'] = response.css(
            'dl.info_l a[href*=company]::text').extract_first()
        movie['nation'] = response.css(
            'dl.info_l a[href*=nation]::text').extract_first()
        movie['link'] = response.request.url
        self.writeToCsv(movie)
        print(movie)

    def readCsv(self):
        with open('movies.csv', 'r') as f:
            spamreader = csv.reader(f)
            for row in spamreader:
                self.start_urls.append(row[-1])

    def writeToCsv(self, data):
        with open(self.data_file, 'a') as f:
            fieldnames = ['year', 'name', 'english_name', 'length', 'genres',
                          'release_date', 'location', 'nation',
                          'director', 'company', 'link']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writerow([s.encode("gbk") for s in data])
