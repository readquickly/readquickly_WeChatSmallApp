from Spider import *
import time

class kuaikanCctv(Spider):
    '''
    爬取 CCTV 的 [快看](http://news.cctv.com/kuaikan/)
    '''

    def __init__(self):
        self.url = 'http://news.cctv.com/kuaikan/all/data/index.json'
        # 直接用这个 url 就可以得到需要的 json 数据，整理成 useful list 就行
    
    def isFresh(self, item):
        '''
        判断新闻是否过时，以24小时（86400秒）为界
        item 中应包含：
        ```
        {..., "dateTime": "2019-04-25 14:26", ...}
        ```
        '''
        dateTime = item.get('dateTime')
        if dateTime:
            timeFormat = '%Y-%m-%d %H:%M'
            publishTime = time.mktime(time.strptime(dateTime, timeFormat))      # 发布时间 -> 时间戳
            currentTime = time.time()       # 当前时间 -> 时间戳
            if currentTime - publishTime <= 86400:
                return True
        return False

            

    def getData(self, response):
        content = response.json()
        data = content['rollData']

        result = []

        for i in data:
            if not self.isFresh(i):      # 消息过时了，不再保存
                break

            useful = {
                'title': i['title'],
                'source': 'CCTV',
                'href': i['url'],
                'time': i['dateTime'],
                'text': i['description'],
                'pic': i['image1']          # 图片质量：(best) image1 > image2 > image
            }
            result.append(useful)

        return result

if __name__ == '__main__':
    k = kuaikanCctv()
    k.run()