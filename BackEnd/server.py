from flask import Flask, request, abort, redirect
import json

'''
处理来自前端的请求响应

使用：在服务器上：
$ export FLASK_APP=server.py
$ flask run --host=0.0.0.0
'''

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello, world!'

@app.route('/readquickly/api/getnews', methods=['GET'])
def requestNews():
    error = None
    city = request.args.get('city', '')
    if city:
        print(city)
        # news = getNews()    # TODO: 调用爬好的数据，注意返回dict，在这里再 json.dumps(allDatas)
        news = {'title': '\t保定天气\n', 'source': '百度', 'href': '', 'time': '\t04月23日，保定凉爽。\n', 'text': '\t今天是04月23日 ，保定的天气凉爽，最高气温23℃，最低气温17℃。建议着厚外套加毛衣等服装。年老体弱者宜着大衣、呢外套加羊毛衫。未来几天，气温保持平稳。\n\t 今天有较强降水，建议您选择在室内进行健身休闲运动；健康防病方面，天冷风大且空气湿度大，易发生感冒，请注意适当增加衣服，加强自我防护避免感冒；如果您有爱车，今天不宜洗车，未来24小时内有雨，如果在此期间洗车，雨水和路上的泥水可能会再次弄脏您的爱车 。\n', 'pic': ''}
        if news != '':
            return json.dumps(news)
        else:
            error = {'error': 'False to get news.'}
    else:
        error = {'error': 'Bad arg (city) was given.'}

    return json.dumps(error)