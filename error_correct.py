import json
import time
from bs4 import BeautifulSoup
from drama_jp import DramaJP
from drama_kr import DramaKR
from mongo import Mongo

Mongo.init_mongo()

fnames_jp = ['jp_16_7', 'jp_40_11', 'jp_40_17', 'jp_40_23', 'jp_40_9', 'jp_41_15', 'jp_41_9', 'jp_42_23', 'jp_44_19', 'jp_44_28', 'jp_45_16', 'jp_22_7', 'jp_40_15', 'jp_40_18', 'jp_40_24', 'jp_41_11', 'jp_41_7', 'jp_42_17', 'jp_44_15', 'jp_44_24', 'jp_44_8']
def fix_jp(fname):
    djp = DramaJP()
    _, book, chapter = fname.split('_')
    book = int(book)
    chapter = int(chapter)

    with open(f'htmls/{fname}') as f:
        content = f.read()
        if True:
            j = json.loads(content)
            content = j.get("HTML")

    soup = BeautifulSoup(content, 'html.parser')
    v = djp.parse_soup(soup, book=int(book), chapter=int(chapter), verse=1)
    print(v)
    v = djp.store_to_cache(soup, book=int(book), chapter=int(chapter))

def fix_kr():
    dkr = DramaKR()

    fnames_kr = [
        (6, 14), (6, 15),
        (11, 4), (11, 10),
        (12, 4), (13, 3),
    ]
    for error in read_errors_kr():
        book_name, chapter = error.split()

        book = dkr.booklist.index(book_name)
        chapter = int(chapter)

        res = Mongo().db.kr.delete_many({'book': book, 'chapter': chapter})
        print(f'{res.deleted_count} docs deleted')
        v = dkr.get_pretty_verse(book, chapter, 1)
        print(v)
        time.sleep(1)
    
    for b_c in fnames_kr:
        book, chapter = b_c

def read_errors_kr():
    with open('errors.txt') as f:
        lines = f.readlines()
    for line in lines:
        if len(line.split()) != 2:
            continue
        yield line
