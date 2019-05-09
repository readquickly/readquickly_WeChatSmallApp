'''
整合要传递给前端的数据

使用：

```
import content
print(getContent('保定'))
```
'''

import os
import sys

from .weather import weather
from .spider import newsDatabase
from .notice import noticesDatabase


def getNews():
    name = newsDatabase.getDatabaseName()
    collection = newsDatabase.getDatabaseCollection()
    news = newsDatabase.readFromDatabase(name, collection)
    return news


def getWeather(city):
    weatherBriefing = weather.TalkWeather(city).run()
    return weatherBriefing


def getNotice():
    name = noticesDatabase.getDatabaseName()
    collection = noticesDatabase.getDatabaseCollection()
    notices = noticesDatabase.readFromDatabase(name, collection)
    return notices


def getContent(city):
    news = getNews()
    weatherBriefing = getWeather(city)
    notices = getNotice()

    content = []
    content += notices or []
    content += [weatherBriefing] or []
    content += news or []

    return content
