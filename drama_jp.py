import requests
from bs4 import BeautifulSoup
from env import CONFIGS_JP


def get_drama_jp(book, chapter, verse):
    params = {
        'book': str(book-1),
        'chapter': str(chapter-1)
    }

    cookies = CONFIGS_JP.get("cookies")
    headers = CONFIGS_JP.get("headers")

    response = requests.get('https://bible.prsi.org/ja/Player/getpage', params=params, cookies=cookies, headers=headers)

    json = response.json()

    html = json.get("HTML")

    soup = BeautifulSoup(html, 'html.parser')

    verse_id = f'v{book:02d}{chapter:03d}{verse:03d}'
    b_content = soup.find(id=verse_id)
    verse_text =  b_content.get_text()

    return verse_text[len(str(verse)):]


if __name__ == "__main__":
    # get_drama_jp('v01001001')
    v = get_drama_jp(book=3, chapter=17, verse=10)
    print(v)
