# -*- coding: utf-8 -*-
import scrapy
import csv
from new.items import Movie
import datetime

AWARDS = "awards.html"
fieldnames = ['year', 'name', 'english_name', 'length', 'genres',
              'release_date', 'location', 'nation',
              'director', 'company', 'link',
              'awards', 'nominations', 'mid', 'rating',
              'total_box_office', 'main_actors']


class AwardsSpider(scrapy.Spider):
    name = 'awards'
    allowed_domains = ['mtime.com']
    start_urls = []
    data_file = "{}.csv".format(datetime.datetime.now().isoformat())
    movies = []
    index = 0

    def __init__(self):
        self.readCsv()

    def parse(self, response):
        movie = self.movies[self.index]
        actors = response.css('dl.main_actor a[rel*=starring]::text').extract()
        movie['main_actors'] = ' '.join(actors)
        self.index += 1
        self.writeToCsv(movie)

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

    def readCsv(self):
        with open('movies_data2.csv', 'r') as f:
            spamreader = csv.DictReader(f, fieldnames=fieldnames)
            for row in spamreader:
                movie = Movie(row)
                self.movies.append(movie)
                self.start_urls.append(movie['link'])

    def writeToCsv(self, data):
        with open(self.data_file, 'a') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writerow(data)
