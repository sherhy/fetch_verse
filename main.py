from drama_jp import DramaJP
from drama_kr import DramaKR
from consts import BOOKS_JP, BOOKS_KR
from mongo import Mongo

def main(book, chapter, verse, verse_until = None):
    Mongo.init_mongo()
    dkr = DramaKR()
    djp = DramaJP()
    plugins = [dkr, djp]
    if not verse_until:
        verse_until = verse
    for v in range(verse, verse_until+1):
        for plugin in plugins:
            text = plugin.get_pretty_verse(book, chapter, v)
            print(text)

if __name__ == "__main__":
    import sys
    args = map(int, sys.argv[1:])
    main(*args)

