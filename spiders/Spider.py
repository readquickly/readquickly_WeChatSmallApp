import requests
from bs4 import BeautifulSoup

class Spider(object):
    """
    项目中所有爬虫的父类，所有爬虫使用这个接口实现
    """

    headers = {
            'Accept': 'application/json, text/plain, */*',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15'
    }

    def __init__(self, url):
            self.url = url
    
    def getPage(self, url):
        response = requests.get(url, headers=self.headers)
        return response

    def getData(self, response):
        data = response.text
        return data

    def saveData(self, data):
        print(data)

    def run(self):
        page = self.getPage(self.url)
        text = self.getData(page)
        self.saveData(text)


    def headers_set(self, special_headers):
        self.headers.update(special_headers)

if __name__ == "__main__":
    s = Spider("http://www.baidu.com")
    s.run()