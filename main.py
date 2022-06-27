from drama_jp import get_drama_jp
from drama_kr import get_drama_kr
from consts import BOOKS_JP, BOOKS_KR

def main(book, chapter, verse):
    res = f"{BOOKS_JP[book]} {chapter}:{verse}\n"
    jp = get_drama_jp(book, chapter, verse)
    res += jp + '\n'

    res += "\n"

    res += f"{BOOKS_KR[book]} {chapter}:{verse}\n"
    kr = get_drama_kr(book, chapter, verse)
    res += kr + '\n'

    print(res)

if __name__ == "__main__":
    import sys
    args = map(int, sys.argv[1:])
    main(*args)

