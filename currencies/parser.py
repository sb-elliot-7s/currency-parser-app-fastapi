import httpx
from bs4 import BeautifulSoup
from database import currencies_collection


class CryptoParser:
    HEADER = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
    }

    def __init__(self, url: str):
        self.url = url
        self._headers = self.HEADER

    def _prepare_bs(self):
        response = httpx.get(self.url, headers=self._headers)
        return BeautifulSoup(response.text, 'html.parser')

    def parse(self) -> list[dict]:
        soup = self._prepare_bs()
        cards = soup.find('tbody', class_='table__body').find_all('tr', class_='table__row--click')
        currencies = []
        for card in cards:
            rank = card.find('span', class_='profile__rank').text.strip().replace('\n', '')
            name = card.find('span', class_='profile__name').text.strip().replace('\n', '').split()[0]
            symbol = card.find('span', class_='profile__subtitle').text.strip().replace('\n', '')
            market_cap = ' '.join(card.find('td', class_='table__cell table__cell--2-of-8 table__cell--s-hide')
                                  .find('div', class_='valuta').text.strip().replace('\n', '').replace('$', '').split())

            price = ' '.join(card.find('td', class_='table__cell table__cell--2-of-8 table__cell--s-3-of-10 table__cell--responsive')
                             .find('div', class_='valuta').text.replace('\n', '').strip().split())

            change_in_procent_24H = card.find('td', class_='table__cell table__cell--1-of-8 table__cell--s-2-of-10 table__cell--right')\
                .find('div', class_='change').text.strip().replace('\n', '')
            currency = {
                'rank': rank,
                'name': name,
                'symbol': symbol,
                'market_cap': market_cap,
                'price': price,
                'change_in_procent_24H': change_in_procent_24H
            }
            currencies.append(currency)
        return currencies

    def save_currencies_to_db(self):
        currencies = self.parse()
        currencies_collection.drop()
        currencies_collection.insert_many(currencies)

    def main(self):
        print('start')
        self.save_currencies_to_db()
