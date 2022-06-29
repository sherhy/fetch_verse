from abc import ABC, abstractmethod

from bs4 import BeautifulSoup


class Fetcher(ABC):
    def _get_headers_cookies(self):
        return {
            "cookies": self.configs.get("cookies"),
            "headers": self.configs.get("headers"),
        }

    @abstractmethod
    def _mongo_init(self):
        pass

    @abstractmethod
    def _get_payload(self, book: int, chapter: int) -> dict:
        pass

    @abstractmethod
    def get_soup(self, book: int, chapter: int) -> BeautifulSoup:
        pass

    @abstractmethod
    def parse_soup(self, soup: BeautifulSoup, **args) -> str:
        """parses soup and returns verse in string"""

    def check_cache(self, book, chapter):
        cache = self.mongo.db[self.col].find_one({"book": book, "chapter": chapter})
        return cache

    @abstractmethod
    def store_to_cache(self, soup: BeautifulSoup, **args):
        """parses soup and stores all verses in mongo"""
        pass

    def is_valid_verse(self, book, chapter, verse):
        try:
            v_max = self.mongo.db.kr.find_one(
                {"book": book, "chapter": chapter},
                {"len": {"$size": {"$objectToArray": "$verses"}}},
            ).get("len")
        except AttributeError:
            return False  # chapter doesn't exist
        return v_max >= verse

    def get_verse(self, book: int, chapter: int, verse: int):
        if not self.is_valid_verse(book, chapter, verse):
            return ""
        cache = self.check_cache(book, chapter)
        if not cache:
            # set params
            soup = self.get_soup(book, chapter)
            self.store_to_cache(soup, book, chapter)
            cache = self.check_cache(book, chapter)
        return cache.get("verses").get(str(verse))

    def get_pretty_verse(self, book: int, chapter: int, verse: int):
        v = self.get_verse(book, chapter, verse)
        if not v:
            return ""
        res = f"{self.booklist[book]} {chapter}:{verse}\n"
        res += v + "\n"
        return res
