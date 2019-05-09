import re
import time
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
        例如 ('http://www.guinnessworldrecords.cn/records/showcase/celebrity', '明星')
        '''
        def __init__(self):
            self.baseUrl = 'http://www.guinnessworldrecords.cn'
            self.url = 'http://www.guinnessworldrecords.cn/records/showcase/'

        def getData(self, response):
            pattern = r'<article.*?<a href="(.*?)".*?<h4>(.*?)</h4>'
            result = re.findall(pattern, response.text, re.S)

            return result

        def run(self):
            response = self.getPage(self.url)
            result =  self.getData(response)
            return result
            

    class ShowcaseCategory(Spider):
        '''
        爬取「吉尼斯世界纪录-纪录展示」的某个具体类别
        '''

        class ItemContentSpider(Spider):
            '''
            爬取一个条具体世界记录的内容
            '''
            def __init__(self, href):
                self.url = href

            def getData(self, response):
                html = response.text
                pattern = r'<div xmlns="http://www.w3.org/1999/xhtml"><p>(.*?)</p>'
                content = re.findall(pattern, html, re.S)
                # 得到的会是一个 ['text']，只取出 'text' 来返回使用
                return content[0]
            
            def run(self):
                response = self.getPage(self.url)
                result =  self.getData(response)
                return result

                
        def __init__(self, category):
            '''
            需要提供具体类别的 category:
            形如：('http://www.guinnessworldrecords.cn/records/showcase/celebrity', '明星')
            '''
            self.baseUrl = 'http://www.guinnessworldrecords.cn/'
            self.url = self.baseUrl + category[0]
            self.source = category[1]

        def getData(self, response):
            result = []

            pattern = r'</article>.*?<a href="(.*?)".*?<article.*?<img src="(.*?)".*?alt="(.*?)".*?/>.*?</figure>'
            # 匹配到的是：("原文链接", "图片链接", "标题")
            # 注意：由于第一项前部定位困难，没有匹配到第一项
            datas = re.findall(pattern, response.text, re.S)

            for i in datas:
                useful = {
                    'title': i[2],
                    'source': '吉尼斯世界纪录展示 | ' + self.source,
                    'href': self.baseUrl + i[0],
                    'time': '',
                    'text': '',
                    'pic': self.baseUrl + i[1]
                }
                # 添加具体内容(text)
                useful['text'] = self.ItemContentSpider(useful['href']).run()

                result.append(useful)

            return result
            

    def __init__(self):
        pass

    def getPage(self):      # 用来获取「分类列表」
        categories = self.ShowcaseIndex().run()
        return categories

    def getData(self, category):  # 用来获取某个「具体类别」
        spider = self.ShowcaseCategory(category)
        spider.run()

    def run(self):
        index = self.getPage()
        total = len(index)
        count = 1
        for i in index:
            print('>> Geting %s of %s.' % (count, total))
            self.getData(i)
            count += 1
            time.sleep(0.5)


if __name__ == "__main__":
    # hall_of_fame = GuinnessWorldRecords_HallOfFame()
    # hall_of_fame.run()
    showcase = GuinnessWorldRecords_Showcase()
    showcase.run()