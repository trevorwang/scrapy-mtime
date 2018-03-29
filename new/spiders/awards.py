# -*- coding: utf-8 -*-
import scrapy
import csv
from new.items import Movie
import datetime

AWARDS = "awards.html"


class AwardsSpider(scrapy.Spider):
    name = 'awards'
    allowed_domains = ['mtime.com']
    start_urls = []
    data_file = "{}.csv".format(datetime.datetime.now().isoformat())

    def __init__(self):
        self.readCsv()

    def parse(self, response):
        if(response.status < 400):
            movie = Movie()
            if (AWARDS in response.request.url):
                self.parse_awards(response, movie)
            else:
                self.parse_movie(response, movie)
            print(movie)
            self.writeToCsv(movie)

    def parse_movie(self, response, movie):
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

    def parse_awards(self, response, movie):
        awards_count = '0'
        nomination_count = '0'
        nums = response.css('h3.per_awardstit strong::text').extract()
        letters = response.css('h3.per_awardstit::text').extract()
        if (len(nums) == 2):
            awards_count = nums[0]
            nomination_count = nums[1]
        elif (len(nums) == 1):
            matched = [s for s in letters if "提名" in s]
            if(matched):
                nomination_count = nums[0]
            else:
                awards_count = nums[0]

        movie['awards'] = awards_count
        movie['nominations'] = nomination_count
        movie['link'] = response.request.url

    def readCsv(self):
        with open('movies.csv', 'r') as f:
            spamreader = csv.reader(f)
            for row in spamreader:
                url = row[-1]
                # self.start_urls.append(url)
                self.start_urls.append(url + AWARDS)

    def writeToCsv(self, data):
        with open(self.data_file, 'a') as f:
            fieldnames = ['year', 'name', 'english_name', 'length', 'genres',
                          'release_date', 'location', 'nation',
                          'director', 'company', 'link',
                          'awards', 'nominations']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writerow(data)
