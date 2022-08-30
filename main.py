import logging

import tornado
import tornado.ioloop
from tornado.web import Application, RequestHandler, url

from drama.drama_jp import DramaJP
from drama.drama_kr import DramaKR
from drama.mongo import Mongo

logging.basicConfig(level=logging.INFO, format="%(asctime)s:%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)
plugins = []


def main():
    PORT = 8004
    app = Application([url(r"^/api/bible", FetchHandler)])
    app.listen(PORT)
    Mongo.init_mongo()
    load_plugins()
    print(f"Service started on port: {PORT}")
    tornado.ioloop.IOLoop.current().start()


def load_plugins():
    global plugins
    dkr = DramaKR()
    djp = DramaJP()
    plugins = [djp, dkr]


class FetchHandler(RequestHandler):
    def get(self):
        try:
            book = int(self.get_argument("book"))
            chapter = int(self.get_argument("chapter"))
            verse = int(self.get_argument("verse"))
            verse_until = int(self.get_argument("verseUntil", "0"))
        except ValueError:
            self.set_status(400)
            self.finish()

        verses = "\n".join(fetch_verses(book, chapter, verse, verse_until))
        self.finish({"text": verses})


def fetch_verses(book: int, chapter: int, verse: int, verse_until: int = 0):
    global plugins
    v_max = plugins[0].get_max_verse(book, chapter)
    if verse > v_max:
        verse = v_max
    if not verse_until:
        verse_until = verse  # verse_until doesn't exist
    elif verse_until > v_max or verse_until < verse:
        verse_until = v_max  # verse_until is too large

    for v in range(verse, verse_until + 1):
        for plugin in plugins:
            text = plugin.get_pretty_verse(book, chapter, v)
            if not text:
                continue
            yield text


if __name__ == "__main__":
    main()
