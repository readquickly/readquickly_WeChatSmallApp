import re
from Spider import *

class GuinnessWorldRecords_HallOfFame(Spider):
    def __init__(self):
        self.url = 'http://www.guinnessworldrecords.cn/records/hall-of-fame/'
        self.baseUrl = 'http://www.guinnessworldrecords.cn/'

    def getData(self, response):
        result = []

        pattern = r'<a href="(.*?)".*?<figure class="promo-media">.*?src="(.*?)"></img>.*?promo-title">(.*?)</.*?promo-subtitle">(.*?)</.*?</header>'
        # 匹配到的是：["原文链接", "图片链接", "标题", "简介"]
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
        

if __name__ == "__main__":
    hall_of_fame = GuinnessWorldRecords_HallOfFame()
    hall_of_fame.run()
