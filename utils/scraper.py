import time
from consts import BOOK_CHAPTERS, BOOKS_JP
from drama_jp import DramaJP
from drama_kr import DramaKR
from mongo import Mongo


def main():
    Mongo.init_mongo()
    dkr = DramaKR()
    djp = DramaJP()
    for book in range(44, 67):
        for chapter in range(1, BOOK_CHAPTERS[book] + 1):
            v = dkr.get_pretty_verse(book, chapter, 1)
            print(v)
            time.sleep(2)
            try:
                v = djp.get_pretty_verse(book, chapter, 1)
                print(v)
            except AttributeError:
                with open("errors.txt", "a") as f:
                    f.write(f"{BOOKS_JP[book]} {chapter}\n")


if __name__ == "__main__":
    main()
