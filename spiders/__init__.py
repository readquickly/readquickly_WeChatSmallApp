'''
# 爬虫模块

## 爬虫实现

- [peoplesdaily]: 爬取「人民日报」，获取重要新闻资讯

- [kr36NewsFlashes]：爬取「36氪快讯」

- 🚫[guinnessworldrecords]: 爬取「吉尼斯世界纪录」(暂不可用)

## 内部机制

- [Spider]: 爬虫模版类，所有爬虫实现的接口

- [NewsDatabase]: 处理爬虫和数据库的交互

## 使用说明

```
import spiders
spiders.run()
```
'''

def run():
    print('爬取"人民日报微博"...')
    p = peoplesdaily.WeiboSpider()
    p.run()
    print('完成。')

    print('爬取"36氪快讯"...')
    k = kr36NewsFlashes.NewsFlashes36Kr()
    k.run()
    print('完成。')


if __name__ == '__main__':
    import peoplesdaily
    import kr36NewsFlashes
    
    run()
