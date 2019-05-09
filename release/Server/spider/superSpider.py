import requests
from bs4 import BeautifulSoup

from . import newsDatabase

class Spider(object):
    """
    项目中所有爬虫的父类，所有爬虫使用这个接口实现

    s = Spider("http://www.baidu.com")
    s.run()
    """

    headers = {             # 请求头模版
            'Accept': 'application/json, text/plain, */*',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15'
    }
    
    def headers_set(self, special_headers):
        self.headers.update(special_headers)

    data = {                # 数据模版
            'title': '',
            'source': '',
            'href': '',
            'time': '',
            'text': '',
            'pic': ''
        }
    
    def data_set(self, special_data):
        self.data.update(special_data)

    def __init__(self, url):
            self.url = url
    
    def getPage(self, url):
        try:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                return response
            else:
                raise RuntimeError('Response Status Code != 200')
        except Exception as e:
            print('[getPage Error] ', e)
            return None

    def getData(self, response):
        try:
            if response:
                data = response.text
                return data
            else:
                raise RuntimeError('Response == None')
        except Exception as e:
            print('[getData Error] ', e)
            return None

    def saveData(self, data):
        '''
        # TODO: data: 传入结果数据的 useful list
        '''
        try:
            if data:
                dbName = newsDatabase.getDatabaseName()
                dbCollection = newsDatabase.getDatabaseCollection()
                newsDatabase.writeToDatabase(dbName, dbCollection, data)
            else:
                raise RuntimeError('data == None')
        except Exception as e:
            print('[saveData Error] ', e)
            return None
        

    def run(self):
        try:
            page = self.getPage(self.url)
            text = self.getData(page)
            self.saveData(text)
            return True
        except Exception as e:
            print('[Spider.run Error]', e)
            return False
