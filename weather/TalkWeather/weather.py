import urllib, sys
import urllib.request
import urllib.parse
import requests
import ssl
import json

class TalkWeather (object):
    '''
    调用[百度智能写作API服务](https://ai.baidu.com/docs#/IntelligentWriting-API/top)来获取一篇天气简讯
    '''

    def __init__(self, city):
        '''
        构造时需要提供城市（中文城市名）
        '''
        self.city = city
        self.__baseUrl = 'https://aip.baidubce.com/rest/2.0/nlp/v1/gen_article?'
        self.__access_token = self.__getAccessToken()
        self.__url = self.__baseUrl + urllib.parse.urlencode({'access_token': self.__access_token})
        self._weather_content = self._getWeatherContent()

    def __getAccessToken(self):
        '''
        获取access_token
        '''
        # client_id 为官网获取的AK， client_secret 为官网获取的SK
        host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={AK}&client_secret={SK}'
        host = host.format(AK='pldYLytjcSPgiQu1klxDc2At', SK='IZN4yZG9K8dX59bKpQTMe4LGS8C8DOFZ')

        header = {'Content-Type': 'application/json; charset=UTF-8'}

        req = urllib.request.Request(url=host, headers=header)

        response = urllib.request.urlopen(req)
        content = response.read()

        if (content):
            # 得到的是个二进制的json
            datas = json.loads(content)
            return datas['access_token']
        else:
            raise Exception('Get Access Token Failed: get a None content.')
    
    def _parse(self, text):
        r'''
        去掉获取到的文本中的多余字符（<p>、</p>、\u200b）
        '''
        text = text.replace('<p>', '\t')
        text = text.replace('</p>', '\n')
        text = text.replace('\u200b', ' ')
        return text


    def _getWeatherContent(self):
        '''
        调用api请求天气简报
        api要求使用post！
        '''
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = {
                'project_id': '1582',
                'city': self.city
                }
        response = requests.post(self.__url, headers=headers, data=data)
        
        weather = response.json()
        '''
        数据示例:
        {
            'error_code': 0,
            'error_msg': '',
            'result': {
                'texts': [
                    '<p>天气详情</p>',
                    '<p>生活建议</p>'
                ],
                'summary': '<p>04月17日，保定凉爽。</p>',
                'title': '<p>保定天气</p>'
            }
        }
        '''
        if weather.get('error_code') == 0:
            weather = weather['result']
            useful = {
                    'title': self._parse(weather['title']),
                    'source': '百度',
                    'href': '',
                    'time': self._parse(weather['summary']),
                    'text': self._parse(weather['texts'][0] + weather['texts'][1]),
                    'pic': ''
                    }
            return useful
        else:
            raise Exception('Get Weather Failed: get a None content.')

       
    def run(self):
        '''
        使用和Spider类相似的操作，方便调用。
        '''
        print(self._weather_content)

if __name__ == '__main__':
    w = TalkWeather('保定')
    w.run()
