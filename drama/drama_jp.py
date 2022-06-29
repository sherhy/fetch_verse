import requests
from bs4 import BeautifulSoup

from drama.consts import BOOKS_JP
from drama.env import CONFIGS_JP
from drama.fetcher import Fetcher
from drama.mongo import Mongo


class DramaJP(Fetcher):
    def __init__(self):
        self.url = "https://bible.prsi.org/ja/Player/getpage"
        self.requests_fnc = requests.get
        self.booklist = BOOKS_JP
        self.configs = CONFIGS_JP
        self.payload = self._get_headers_cookies()
        self._mongo_init()

    def _mongo_init(self):
        self.mongo = Mongo()
        self.col = "jp"

    def _get_payload(self, book: int, chapter: int):
        return {"book": str(book - 1), "chapter": str(chapter - 1)}

    def get_soup(self, book: int, chapter: int) -> BeautifulSoup:
        self.payload["params"] = self._get_payload(book, chapter)
        response = self.requests_fnc(self.url, **self.payload)
        json_obj = response.json()
        html = json_obj.get("HTML")
        soup = BeautifulSoup(html, "html.parser")
        return soup

    def parse_soup(self, soup: BeautifulSoup, book: int, chapter: int, verse: int) -> str:
        verse_id = f"v{book:02d}{chapter:03d}{verse:03d}"  # 'v01001001'
        content = soup.find("verse", id=verse_id)
        if not content:
            return ""
        verse_text = content.get_text()
        i = verse_text.index(str(verse)) + len(str(verse))
        return verse_text[i:]

    def store_to_cache(self, soup: BeautifulSoup, book: int, chapter: int) -> None:
        v_max = self.mongo.db.kr.find_one(
            {"book": book, "chapter": chapter},
            {"len": {"$size": {"$objectToArray": "$verses"}}},
        ).get("len")
        verses = {}
        for i in range(1, v_max + 1):
            verse = self.parse_soup(soup, book, chapter, i)
            # print(f'{i} {verse[:10]}')
            verses[str(i)] = verse
        if i != v_max:
            print("Error: verse count doesn't match")

        self.mongo.db[self.col].insert_one({"book": book, "chapter": chapter, "verses": verses})


if __name__ == "__main__":
    Mongo.init_mongo()
    djp = DramaJP()
    # soup = djp.get_soup(book=16, chapter=7)
    # v = djp.parse_soup(soup, 16, 7, 1)
    v = djp.get_pretty_verse(43, 5, 1)
    print(v)
