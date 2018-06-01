# -*- coding: utf-8 -*-
import scrapy
import csv
from new.items import Movie
import datetime
import regex
import json

rating_link = 'http://service.library.mtime.com/Movie.api?Ajax_CallBack=true&Ajax_CallBackType=Mtime.Library.Services&Ajax_CallBackMethod=GetMovieOverviewRating&Ajax_CallBackArgument0={}'
fieldnames = ['year', 'name', 'english_name', 'length', 'genres',
              'release_date', 'location', 'nation',
              'director', 'company', 'link',
              'awards', 'nominations', 'mid', 'rating', 'total_box_office', 'main_actors']
movie_id_regex = regex.compile(r'http://movie.mtime.com/(\d+)/')


class AwardsSpider(scrapy.Spider):
    allowed_domains = ['mtime.com']
    start_urls = []
    data_file = "{}.csv".format(datetime.datetime.now().isoformat())
    movies = []
    index = 0

    def __init__(self):
        self.readCsv()
        print(self.start_urls)
        self.writeHeaderToCsv(fieldnames)
        # self.start_urls.append(
        # 'http://service.library.mtime.com/Movie.api?Ajax_CallBack=true&Ajax_CallBackType=Mtime.Library.Services&Ajax_CallBackMethod=GetMovieOverviewRating&Ajax_CallBackArgument0=105799')

    def parse(self, response):
        movie = self.movies[self.index]
        actors = response.css('dl.main_actor a[rel*=starring]::text').extract()
        movie['main_actors'] = ' '.join(actors)
        self.index += 1
        self.writeToCsv(movie)

    def parse_awards(self, response, movie):
        matched = regex.search(r'({.*})', response.text)
        if (matched):
            jdata = json.loads(matched[0])
            print(jdata)
            try:
                movie['rating'] = str(jdata.get(
                    'value')['movieRating']['RatingFinal'])
                office = jdata.get('value')['boxOffice']['TotalBoxOffice']
                unit = jdata.get('value')['boxOffice']['TotalBoxOfficeUnit']
                movie['total_box_office'] = office + unit
            except KeyError as e:
                self.log('>>>>>>>KeyError<<<<<<<<<')

    def readCsv(self):
        with open('movies_data2.csv', 'r') as f:
            spamreader = csv.DictReader(f, fieldnames=fieldnames)
            for row in spamreader:
                movie = Movie(row)
                link = row['link']
                print(link)
                self.movies.append(movie)
                self.start_urls.append(link)

    def writeToCsv(self, data):
        with open(self.data_file, 'a') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writerow(data)

    def writeHeaderToCsv(self, header):
        with open(self.data_file, 'a') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
