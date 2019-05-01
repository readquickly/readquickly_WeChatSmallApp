from flask import Flask, request, abort, redirect
from flask import render_template

import json
import time

from . import content
from .notice import superNotice

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


@app.route('/readquickly/admin/notice', methods=['GET', 'POST'])
def notice():
    error = None
    if request.method == 'POST':
        if request.form['title']:
            useful = {
                'title': request.form['title'],
                'source': request.form['source'] or 'Admin',
                'href': request.form['href'],
                'time': time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time())),
                'text': request.form['text'],
                'pic': request.form['pic'],
                'expires': request.form['expires']
            }
            superNotice.saveData([useful])
            return 'Succeed!'
        else:
            error = 'Invalid Data!'
            return error
    return render_template('notice.html')