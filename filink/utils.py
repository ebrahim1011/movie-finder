import re
from googlesearch import search
import requests
from bs4 import BeautifulSoup


email_address = ""
list_link = []
imdb_title = ''


def link_mink(query):
    list_link = []
    result_go = search(query, tld="com", num=25, stop=25, pause=2)

    for link in result_go:
        try:
            r = requests.get(link, timeout=5)
        except:
            continue

        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            for link in soup.find_all('a', href=True):
                if link['href'].endswith('.mkv') or link['href'].endswith('.mp4'):
                    list_link.append(link['href'])
    return list_link


def imdb(query):
    query += 'imdb'
    result_go = search(query, tld="com", num=25, stop=25, pause=2)

    for link in result_go:
        if 'https://www.imdb.com' in link:

            my_code = link[26:]
            result = re.search('/(.*)/', my_code)
            imdbid = result.group(1)
            movie = f'http://www.omdbapi.com/?i={imdbid}&apikey=c6b05d74'
            r = requests.get(movie, timeout=5)
            return r.json()

        else:
            continue
