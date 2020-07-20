import requests
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

url = "https://www.imdb.com/search/title/?groups=top_1000&ref_=adv_prv"
headers = {"Accept-Language": "en-US, en;q=0.5"}
results = requests.get(url, headers=headers)

soup = BeautifulSoup(results.text, "html.parser")
titles = []
years = []
time = []
imdb_ratings = []
metascores = []
votes = []
us_gross = []

movie_div = soup.find_all('div', class_='lister-item mode-advanced')

for x in movie_div:
    name = x.h3.a.text
    titles.append(name)

    year = x.h3.find('span', class_='lister-item-year').text
    years.append(year)

    runtime = x.p.find('span', class_='runtime').text if x.p.find(
        'span', class_='runtime').text else '-'
    time.append(runtime)

    # IMDb rating
    imdb = float(x.strong.text)
    imdb_ratings.append(imdb)

    m_score = x.find('span', class_='metascore').text if x.find(
        'span', class_='metascore') else '-'
    metascores.append(m_score)

    # there are two NV containers, grab both of them as they hold both the votes and the grosses
    nv = x.find_all('span', attrs={'name': 'nv'})
    vote = nv[0].text
    votes.append(vote)

    # filter nv for gross
    grosses = nv[1].text if len(nv) > 1 else '-'
    us_gross.append(grosses)


# save data into pandas dataframes
movies = pd.DataFrame({
    'movie': titles,
    'year': years,
    'timeMin': time,
    'imbd': imdb_ratings,
    'metascore': metascores,
    'votes': votes,
    'us_grossMillions': us_gross
})
movies['year'] = movies['year'].str.extract('(\d+)').astype(int)
movies['timeMin'] = movies['timeMin'].str.extract('(\d+)').astype(int)
movies['metascore'] = movies['metascore'].astype(str)
movies['votes'] = movies['votes'].str.replace(',', '').astype(int)
movies['us_grossMillions'] = movies['us_grossMillions'].map(
    lambda x: x.lstrip('$').rstrip('M'))
movies['us_grossMillions'] = pd.to_numeric(
    movies['us_grossMillions'], errors='coerce')
# print(titles)
# print(movies)

# save data to csv
movies.to_csv('movies.csv')
