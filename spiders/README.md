# Spiders

> 在该目录下实现相关爬虫。

## 实现一览

* [weibo](./weibo): 爬取「微博」中相关内容
    * [peoplesdaily](./weibo/peoplesdaily): 爬取「人民日报」，获取重要新闻资讯
* [guinnessworldrecords](./guinnessworldrecords): 爬取「吉尼斯世界纪录」
* [kr36](./kr36)：爬取「36氪快讯」
* [cctvKuaikan](./cctvKuaikan.py)：爬取「CCTV快看」

## 爬虫模版

使用 当前目录下的 `Spider.py` 作为模版接口来实现爬虫。

## 标准数据

所有最终得到的数据整理为：

```py
{
    'title': '文章标题',
    'source': '文章来源',
    'href': '原文地址',
    'time': '发布时间',
    'text': '文章内容',
    'pic': '图片url地址'
}
```

把这种格式的数据称为 `useful dict`，
`[{USEFUL-DICT}, {}, ...]` 称为 `useful list`

## TODO

1. 现在是每个爬虫分别在一个目录下，每个目录下复制了 `Spider.py`, 之后应该把 `爬虫.py` 全部提取出来放到**同一个目录里**，**用同一个 Spider.py**
2. 每一个爬虫的调用，都把其结果 `useful list` 写入数据库（暂定使用 MongoDB）。