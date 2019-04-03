import requests
from bs4 import BeautifulSoup

url_base = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=2803301701&containerid=1076032803301701'

headers = {
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15',
        'X-Requested-With': 'XMLHttpRequest',
        'MWeibo-Pwa': '1'
        }

def get_page(basicUrl, headers, page):
    url = basicUrl + '&page=%s' % page
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()      # Would return a dict
        else:
            raise RuntimeError('Response Status Code != 200')
    except Exception as e:
        print('Get Page False:', e)
        return None


def parse_html(html):
    soup = BeautifulSoup(html, 'lxml')
    return soup.get_text()
    

def get_content(data):
    result = []
    if data and data.get('data').get('cards'):
        for item in data.get('data').get('cards'):
            useful = {}
            useful['source'] = item.get('mblog').get('source')
            useful['text'] = parse_html(item.get('mblog').get('text'))

            result.append(useful)

    return result


def save_data(data):
    for i in data:
        print(i)
        print('\n')


if __name__ == '__main__':
    for page in range(1, 3):
        r = get_page(url_base, headers, page)
        d = get_content(r)
        save_data(d)
