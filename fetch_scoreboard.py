#!/usr/bin/env python

import sys

from bs4 import BeautifulSoup
from django.utils.text import slugify
import requests
import toml


def text_of(element):
    return element.get_text().replace('\n', '')


USER_AGENT='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15'
venue = sys.argv[1]
year  = sys.argv[2]
show  = sys.argv[3]

req = requests.get(
    'https://eurovision.tv/event/%s-%s/%s' % (venue, year, show),
    headers = {'User-Agent': USER_AGENT},
)
print(req.url, req.status_code)
soup = BeautifulSoup(req.text, 'html.parser')

# load existing data
countries = toml.load('countries.toml')
try:
    artists = toml.load('artists/%s.toml' % year)
except FileNotFoundError:
    artists = {}
try:
    singers = toml.load('singers/%s.toml' % year)
except FileNotFoundError:
    singers = {}
try:
    songs = toml.load('songs/%s.toml' % year)
except FileNotFoundError:
    songs = {}

competing = []
song_by_country = {}
songs_in_order = []

contests = toml.load('contests.toml')
if year not in contests:
    contests[year] = {
        'host': '',
    }
if 'shows' not in contests[year]:
    contests[year]['shows'] = []
contests[year]['shows'].append('%s-%s' % (year, show))

countries_handle = open('countries.toml', 'a')
artists_handle   = open('artists/%s.toml' % year, 'a+')
singers_handle   = open('singers/%s.toml' % year, 'a+')
songs_handle     = open('songs/%s.toml' % year, 'a+')

board = soup.find_all('table', class_='w-full')[0]
for row in board.select('tbody tr'):
    cells = row.select('td')

    country = text_of(cells[1])
    country_slug = slugify(country)
    competing.append(country_slug)

    artist = text_of(cells[2])
    artist_slug = slugify(artist)

    song = text_of(cells[3])
    song_slug = slugify(song)

    song_by_country[country] = song_slug
    songs_in_order.append(song_slug)

    if country_slug not in countries:
        countries_handle.write("\n[%s]\n" % country_slug)
        countries_handle.write("english = '%s'\n" % country)
        countries_handle.write("hashtag = ''\n\n")

    if artist_slug not in artists:
        artists_handle.write("[%s]\n" % artist_slug)
        artists_handle.write("name   = '%s'\n" % artist)
        artists_handle.write("singer = ['%s']\n\n" % artist_slug)

    if artist_slug not in singers:
        singers_handle.write('[%s]\n' % artist_slug)
        singers_handle.write("name        = '%s'\n" % artist)
        singers_handle.write("known_as    = '%s'\n" % artist)
        singers_handle.write("born        = 1900-00-00\n")
        singers_handle.write("died        = 1900-00-00\n")
        singers_handle.write("citizenship = ['country']\n\n")

    if song_slug not in songs:
        songs_handle.write('[%s]\n' % song_slug)
        songs_handle.write('title    = "%s"\n' % song)
        songs_handle.write("artist   = '%s'\n" % artist_slug)
        songs_handle.write("country  = '%s'\n" % country_slug)
        songs_handle.write("language = ''\n\n")

with open('scores/%s-%s.toml' % (year, show), 'w') as scores_handle:
    for country in sorted(competing):
        req = requests.get(
            'https://eurovision.tv/event/%s-%s/%s/results/%s' % (
                venue,
                year,
                show,
                country,
            ),
            headers = {'User-Agent': USER_AGENT},
        )
        print(req.url, req.status_code)

        soup = BeautifulSoup(req.text, 'html.parser')
        board = soup.find_all('table', class_='w-full')[1]

        prev_points = 0
        for row in board.select('tbody tr'):
            cells = row.select('td')
            try:
                points = text_of(cells[0])
                to = text_of(cells[1])
                prev_points = points
            except IndexError:
                to = text_of(cells[0])
                points = prev_points

            scores_handle.write('[[%s]]\n' % country)
            scores_handle.write("song   = '%s'\n" % song_by_country[to])
            scores_handle.write('points = %s\n' % points)
            scores_handle.write("source = 'jury'\n\n")

with open('shows/%s.toml' % year, 'a+') as shows_handle:
    shows_handle.write('[%s-%s]\n' % (year, show))
    shows_handle.write('date         = %s-01-01\n' % year)
    shows_handle.write("type         = '%s'\n" % show)
    shows_handle.write('performances = [\n')
    for song in songs_in_order:
        shows_handle.write("    '%s',\n" % song)
    shows_handle.write(']\n\n')
