'''
整合要传递给前端的数据
'''

import os
import sys
# 获取上一层目录**绝对路径** to find `spiders` & `weather` package
sys.path.append(os.path.split(os.path.dirname(__file__))[0])

from weather import weather
from spiders import NewsDatabase as database


def getNews():
    name = database.getDatabaseName()
    collection = database.getDatabaseCollection()

    news = database.readFromDatabase(name, collection)

    return news


def getWeather(city):
    weatherBriefing = weather.TalkWeather(city).run()
    return weatherBriefing


def getContent(city):
    news = getNews()
    weatherBriefing = getWeather(city)

    content = []
    content.append(weatherBriefing)
    content += news

    return content


if __name__ == '__main__':
    print(getContent('保定'))
