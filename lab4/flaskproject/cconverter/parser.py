import requests
from bs4 import BeautifulSoup
from .. import cache


# @cache.cached(key_prefix='get_full_names_currencies')
def get_full_names_currencies():
    URL = 'https://www.exchangerate-api.com/docs/supported-currencies'
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')

    article = soup.find("article", {"class": "mb-4 mb-md-6"})

    full_names_currencies = {
        short.text: f'{short.text} {full.text} {country.text}'
        for short, full, country
        in article.find_all("tr")[1:]
    }

    return full_names_currencies
