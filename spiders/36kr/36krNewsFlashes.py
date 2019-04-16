from Spider import *

class NewsFlashes36Kr (Spider):
    '''
    爬取 [36 Kr 快讯](https://36kr.com/newsflashes)
    '''

    def __init__(self):
        self.url = 'https://36kr.com/pp/api/newsflash?per_page=10'
        # 直接用如上请求可以获取前十条快讯
        
    def getData(self, response):
        content = response.json()
        data = content['data']

        result = []

        for i in data['items']:
            useful = {
                'title': i['title'],
                'source': '快讯 | 36氪',
                'href': i['news_url'],
                'time': i['published_at'],
                'text': i['description'],
                'pic': ''
            }
            result.append(useful)

        return result

if __name__ == '__main__':
    n = NewsFlashes36Kr()
    n.run()