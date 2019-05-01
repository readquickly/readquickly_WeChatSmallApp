from flask import Flask, request, abort, redirect
import json

from . import content

'''
处理来自前端的请求响应

使用：在服务器上：
$ export FLASK_APP=server.py
$ flask run --host=0.0.0.0
'''

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello, Read Quickly!'

@app.route('/readquickly/api/getnews', methods=['GET'])
def requestNews():
    error = None
    city = request.args.get('city', '')
    if city:
        print(city)
        news = content.getContent(city)
        if news:
            return json.dumps(news)
        else:
            error = {'error': 'False to get content.'}
    else:
        error = {'error': 'Bad arg (city) was given.'}

    return json.dumps(error)