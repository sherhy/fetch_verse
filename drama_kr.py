import requests
from bs4 import BeautifulSoup
from consts import BOOKS_KR
from env import CONFIGS_KR
from fetcher import Fetcher
from mongo import Mongo

class DramaKR(Fetcher):
    def __init__(self):
        self.url = 'https://www.duranno.com/bdictionary/result_woori.asp'
        self.requests_fnc = requests.post
        self.booklist = BOOKS_KR
        self.configs = CONFIGS_KR
        self.payload = self._get_headers_cookies()
        self._mongo_init()

    def _mongo_init(self):
        self.col = 'kr'
        self.mongo = Mongo()

    def _get_payload(self, book: int, chapter: int):
        return {
            's': 'r',
            'kd': '104',
            'vl': str(book),
            'ct': str(chapter)
        }
    
    def get_soup(self, book: int, chapter: int) -> BeautifulSoup:
        self.payload['data'] = self._get_payload(book, chapter)
        response = self.requests_fnc(self.url, **self.payload)
        response.encoding = 'EUC-KR'

        soup = BeautifulSoup(response.text, 'html.parser')
        return soup
    
    def parse_soup(self, soup: BeautifulSoup, verse: int, **args) -> str:
        tables = soup.find_all('table', {'width': '98%'})
        for table in tables:
            trs = table.find_all('tr', {'valign': "top"})
            try:
                verse = next(filter(
                    lambda tr: tr.find(
                        'td',
                        {"class": "tk4br"}
                    ).get_text(strip=True) == f'{verse}.', trs
                ))
                if verse:
                    return verse.font.get_text()
            except StopIteration:
                pass
        return 'Error: verse not found'
    
    def store_to_cache(self, soup: BeautifulSoup, book: int, chapter: int):
        verse = 1
        verses = {}
        tables = soup.find_all('table', {'width': '98%'})
        for table in tables:
            trs = table.find_all('tr', {'valign': "top"})
            for tr in trs:
                if not tr.find('td', {"class": "tk4br"}).get_text(strip=True):
                    continue
                text = tr.font.get_text(strip=True)
                if not text:
                    continue
                verses[str(verse)] = text
                verse += 1

        self.mongo.db[self.col].insert_one({
            'book': book,
            'chapter': chapter,
            'verses': verses
        })
    

if __name__ == "__main__":
    Mongo.init_mongo()
    dkr = DramaKR()
    # soup = dkr.get_soup(2, 38)
    # v = dkr.parse_soup(soup, 1)
    # dkr.store_to_cache(soup, 43, 1)
    v = dkr.get_pretty_verse(16, 8, 1)
    print(v)
