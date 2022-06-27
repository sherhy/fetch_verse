import requests
from bs4 import BeautifulSoup
from env import CONFIGS_KR

def get_drama_kr(book, chapter, verse):
    data = {
        's': 'r',
        'kd': '104',
        'vl': str(book), #book
        'ct': str(chapter), #chapter
    }
    cookies = CONFIGS_KR.get("cookies")
    headers = CONFIGS_KR.get("headers")

    response = requests.post('https://www.duranno.com/bdictionary/result_woori.asp', cookies=cookies, headers=headers, data=data)

    soup = BeautifulSoup(response.content, 'html.parser')

    tables = soup.find_all('table', {'width': '98%'})

    for table in tables:
        trs = table.find_all('tr', {'valign': "top"})

        try:
            verse = next(filter(
                lambda tr: tr.find(
                    'td',
                    {"class": "tk4br"}
                ).get_text(strip=True) == f'{verse}.', trs
            ))
            if verse:
                break
        except StopIteration:
            pass

    return verse.font.get_text()

if __name__ == "__main__":
    v = get_drama_kr(1,1,1)
    print(v)
