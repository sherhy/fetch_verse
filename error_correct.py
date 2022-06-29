import json
from bs4 import BeautifulSoup
from drama_jp import DramaJP
from drama_kr import DramaKR
from mongo import Mongo

plugin = {'jp': DramaJP(), 'kr': DramaKR()}
def get_plugin(lang):
    global plugin
    return plugin[lang]

def fix(fname):
    lang, book, chapter = fname.split('_')
    is_jp = lang == 'jp'
    book = int(book)
    chapter = int(chapter)

    with open(f'htmls/{fname}') as f:
        content = f.read()
        if is_jp:
            j = json.loads(content)
            content = j.get("HTML")

    soup = BeautifulSoup(content, 'html.parser')
    v = get_plugin(lang).parse_soup(soup, book=int(book), chapter=int(chapter), verse=1)
    print(v)
    v = get_plugin(lang).store_to_cache(soup, book=int(book), chapter=int(chapter))

Mongo.init_mongo()
fnames = ['jp_16_7', 'jp_40_11', 'jp_40_17', 'jp_40_23', 'jp_40_9', 'jp_41_15', 'jp_41_9', 'jp_42_23', 'jp_44_19', 'jp_44_28', 'jp_45_16', 'jp_22_7', 'jp_40_15', 'jp_40_18', 'jp_40_24', 'jp_41_11', 'jp_41_7', 'jp_42_17', 'jp_44_15', 'jp_44_24', 'jp_44_8']
for fname in fnames:
    fix(fname)

# fname = 'jp_44_15'
# fix(fname)
