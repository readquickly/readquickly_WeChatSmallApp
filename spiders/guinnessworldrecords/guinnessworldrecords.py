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
        '''
        获取一个纪录展示具体项目的目录列表，

        result = []

        pattern = r'<article.*?<a href="(.*?)".*?<h4>(.*?)</h4>'
        # 匹配到的是：("项目链接", "标题")
        datas = re.findall(pattern, SOMETHING, re.S)
        '''
        pass    # TODO

    class ShowcaseCategory(Spider):
        '''
        爬取「吉尼斯世界纪录-纪录展示」的某个具体类别
        '''
        pass    # TODO

    def __init__(self):
        self.url = 'http://www.guinnessworldrecords.cn/records/showcase/'
        self.baseUrl = 'http://www.guinnessworldrecords.cn/'




if __name__ == "__main__":
    hall_of_fame = GuinnessWorldRecords_HallOfFame()
    hall_of_fame.run()