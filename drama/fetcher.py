from abc import ABC, abstractmethod
from typing import Any, Dict

from bs4 import BeautifulSoup


class Fetcher(ABC):
    def _get_headers_cookies(self) -> Dict[str, Any]:
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

    def check_cache(self, book: int, chapter: int) -> Dict[str, Any]:
        cache = self.mongo.db[self.col].find_one({"book": book, "chapter": chapter})
        return cache

    @abstractmethod
    def store_to_cache(self, soup: BeautifulSoup, **args) -> None:
        """parses soup and stores all verses in mongo"""
        pass

    def is_valid_verse(self, book: int, chapter: int, verse: int) -> bool:
        v_max = self.get_max_verse(book, chapter)
        return v_max >= verse

    def get_max_verse(self, book: int, chapter: int) -> int:
        try:
            v_max = self.mongo.db.kr.find_one(
                {"book": book, "chapter": chapter},
                {"len": {"$size": {"$objectToArray": "$verses"}}},
            ).get("len")
            return v_max
        except AttributeError:
            return 0  # chapter doesn't exist

    def get_verse(self, book: int, chapter: int, verse: int) -> str:
        if not self.is_valid_verse(book, chapter, verse):
            return ""
        cache = self.check_cache(book, chapter)
        if not cache:
            # set params
            soup = self.get_soup(book, chapter)
            self.store_to_cache(soup, book, chapter)
            cache = self.check_cache(book, chapter)
        return cache.get("verses").get(str(verse))

    def get_pretty_verse(self, book: int, chapter: int, verse: int) -> str:
        v = self.get_verse(book, chapter, verse)
        if not v:
            return ""
        res = f"{self.booklist[book]} {chapter}:{verse}\n"
        res += v + "\n"
        return res
