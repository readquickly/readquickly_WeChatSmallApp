from Spider import *

class NewsFlashes36Kr(Spider):
    '''
    爬取 CCTV 的 [快看](http://news.cctv.com/kuaikan/)
    '''

    def __init__(self):
        self.url = 'http://news.cctv.com/kuaikan/all/data/index.json'
        # 直接用这个 url 就可以得到需要的 json 数据，整理成 useful list 就行
        
    def getData(self, response):
        content = response.json()
        data = content['rollData']

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