import tornado
import tornado.ioloop
from tornado.web import Application, RequestHandler, url

from utils.drama_jp import DramaJP
from utils.drama_kr import DramaKR
from utils.mongo import Mongo

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
    plugins = [dkr, djp]


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


def fetch_verses(book, chapter, verse, verse_until=None):
    global plugins
    if not verse_until:
        verse_until = verse
    for v in range(verse, verse_until + 1):
        for plugin in plugins:
            text = plugin.get_pretty_verse(book, chapter, v)
            yield text


if __name__ == "__main__":
    # Mongo.init_mongo()
    # load_plugins()
    # book = 1
    # chapter = 1
    # verse = 1
    # verse_until = None
    # verses = '\n'.join(fetch_verses(book, chapter, verse, verse_until))
    # v = tornado.escape.to_unicode(verses) # just have to echo -e `curl $URL`
    # print(v)
    main()
