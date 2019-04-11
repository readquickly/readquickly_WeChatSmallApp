import re
from Spider import *

class GuinnessWorldRecords_HallOfFame(Spider):
    '''
    爬取 [吉尼斯世界纪录-名人堂](http://www.guinnessworldrecords.cn/records/hall-of-fame/)
    里面主要陈列的三个记录
    由于「吉尼斯世界记录」的内容结构比较复杂，直接用正则表达式来提取比较方便。
    '''

    def __init__(self):
        self.url = 'http://www.guinnessworldrecords.cn/records/hall-of-fame/'
        self.baseUrl = 'http://www.guinnessworldrecords.cn/'

    def getData(self, response):
        result = []

        pattern = r'<a href="(.*?)".*?<figure class="promo-media">.*?src="(.*?)"></img>.*?promo-title">(.*?)</.*?promo-subtitle">(.*?)</.*?</header>'
        # 匹配到的是：("原文链接", "图片链接", "标题", "简介")
        datas = re.findall(pattern, response.text, re.S)

        for i in datas:
            useful = {
                'title': i[2],
                'source': '吉尼斯世界纪录名人堂 | Guinness World Records',
                'href': self.baseUrl + i[0],
                'time': '',
                'text': i[3],
                'pic': self.baseUrl + i[1]
            }
            result.append(useful)

        return result
        

class GuinnessWorldRecords_Showcase(Spider):
    '''
    爬取 [吉尼斯世界纪录-纪录展示](http://www.guinnessworldrecords.cn/records/showcase/)
    里面有各项具体的记录
    '''

    class ShowcaseIndex(Spider):
        '''
        爬取「吉尼斯世界纪录-纪录展示」的分类列表
        例如 [{'明星': 'http://www.guinnessworldrecords.cn/records/showcase/celebrity'}]
        '''
        def __init__(self):
            self.baseUrl = 'http://www.guinnessworldrecords.cn'
            self.url = 'http://www.guinnessworldrecords.cn/records/showcase/'

        def getData(self, response):
            result = []
            pattern = r'<article.*?<a href="(.*?)".*?<h4>(.*?)</h4>'
            datas = re.findall(pattern, response.text, re.S)

            for i in datas:
                result.append({
                    i[1]: self.baseUrl + i[0]
                })

            return result

        def run(self):
            response = self.getPage(self.url)
            result =  self.getData(response)
            return result
            

    class ShowcaseCategory(Spider):
        '''
        爬取「吉尼斯世界纪录-纪录展示」的某个具体类别
        '''
        def __init__(self, categoryUrl):
            '''
            需要提供具体类别的 url
            '''
            self.baseUrl = 'http://www.guinnessworldrecords.cn/'
            self.url = categoryUrl

        def getData(self, response):
            result = []

            pattern = r'</article>.*?<a href="(.*?)".*?<article.*?<img src="(.*?)".*?alt="(.*?)".*?/>.*?</figure>'
            # 匹配到的是：("原文链接", "图片链接", "标题")
            # 注意：由于第一项前部定位困难，没有匹配到第一项
            datas = re.findall(pattern, response.text, re.S)

            for i in datas:
                useful = {
                    'title': i[2],
                    'source': '吉尼斯世界纪录展示 | Guinness World Records',
                    'href': self.baseUrl + i[0],
                    'time': '',
                    'text': '',
                    'pic': self.baseUrl + i[1]
                }
                result.append(useful)

            return result
            

    def __init__(self):
        self.url = 'http://www.guinnessworldrecords.cn/records/showcase/'
        self.baseUrl = 'http://www.guinnessworldrecords.cn/'




if __name__ == "__main__":
    # hall_of_fame = GuinnessWorldRecords_HallOfFame()
    # hall_of_fame.run()
    pass