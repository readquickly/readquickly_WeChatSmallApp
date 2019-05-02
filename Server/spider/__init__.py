'''
# 爬虫模块

## 爬虫实现

- [wieboPeoplesDaily.py]: 爬取「人民日报」，获取重要新闻资讯

- [kr36NewsFlashes]：爬取「36氪快讯」

- 🚫[guinnessworldrecords]: 爬取「吉尼斯世界纪录」(暂不可用)

- [cctvKuaikan.py]: 爬取CCTV快看

## 内部机制

- [Spider]: 爬虫模版类，所有爬虫实现的接口

- [NewsDatabase]: 处理爬虫和数据库的交互

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

## 使用说明

```
import spiders
spiders.run()
```
'''
