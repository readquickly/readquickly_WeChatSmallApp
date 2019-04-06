import re
import time
import pymysql
from Spider import *

class SpiderFinished(Exception):
    """
    抛出一个SpiderFinished代表爬完了所有待爬数据，用来控制爬虫结束。
    """
    pass

class WeiboSpider(Spider):
    """
    爬取 [微博手机Web版](https://m.weibo.cn/) 上的 [人民日报](https://m.weibo.cn/u/2803301701)
    通过伪造 Ajax 请求，爬取目标的微博页。
    Ajax 请求中需要两个关键值：
        * uid 或叫 oid -> 可以在 https://weibo.com/ 中可在 html 中的 /html/head/script[4]/text() 中看到 一个 key 为 `oid` 的值。（有一个注释<!-- $CONFIG -->下面的脚本中）
        * containerid -> 请求 `https://m.weibo.cn/api/container/getIndex?type=uid&value={oid}` 得到的 json 中 `this.data.tabsInfo.tabs[1].containerid` （"title": "微博" 这一组中的 containerid）
    """

    def __init__(self):
        self.oid = '2803301701'
        self.containerid = '1076032803301701'
        self.data_set({'source': '人民日报|微博'})

        # 构造 Ajax 请求制定用户 “微博” 页面 使用的 url
        self.basicUrl = 'https://m.weibo.cn/api/container/getIndex?type=uid&value={oid}&containerid={containerid}'.format(
            oid=self.oid,
            containerid=self.containerid
            )

        # 仿制请求头
        self.headers_set({
                'Accept': 'application/json, text/plain, */*',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15',
                'X-Requested-With': 'XMLHttpRequest',
                'MWeibo-Pwa': '1'
                })
        
        # 数据库准备
        self.db = pymysql.connect(host='localhost', user='c', password='000123', db='readquickly')
        self.table = 'test'
        self.cursor = self.db.cursor()
        createTable = '''
        CREATE TABLE IF NOT EXISTS {name} (
            id BIGINT NOT NULL AUTO_INCREMENT,
            title VARCHAR(255),
            source VARCHAR(255),
            href VARCHAR(511),
            time VARCHAR(63),
            text VARCHAR(2047),
            pic VARCHAR(511),
            PRIMARY KEY (id)
            );
            '''.format(name=self.table)
        self.cursor.execute(createTable)

        # 爬虫已结束的标识符
        self.spiderOutOfRange = False

    def __del__(self):
        self.db.close()


    def getData(self, response):
        def parse_html(html):
            soup = BeautifulSoup(html, 'lxml')
            return soup.get_text()

        def get_weibo_pic(mblog):
            pic = None
            if mblog.get('original_pic'):           # 带图片的微博，提供有三种质量的图片：thumbnail_pic，bmiddle_pic，original_pic
                pic = mblog.get('original_pic')
            elif mblog.get('page_info'):            # 带视频的微博
                pic = mblog.get('page_info').get('page_pic').get('url')
            elif mblog.get('retweeted_status'):     # 转发&评论的微博
                pic = mblog.get('retweeted_status').get('bmiddle_pic')
            return pic or ''

        try:
            json = response.json()
            result = []

            for item in json.get('data').get('cards'):
                useful = {}                 # TODO: use self.data
                useful['source'] = '人民日报|微博'
                useful['href'] = item.get('scheme')
                mblog = item.get('mblog')
                if not mblog:
                    continue
                else:
                    if mblog.get('text').find('【') != -1:
                        part = re.findall(
                            r'【(.*?)】(.*)',
                            mblog.get('text')
                            )[0]
                        useful['title'] = parse_html(part[0])
                        useful['text'] = parse_html(part[1])
                    else:
                        useful['title'] = ''
                        useful['text'] = parse_html(mblog.get('text'))
                    useful['time'] = mblog.get('created_at')
                    useful['pic'] = get_weibo_pic(mblog)
                
                if not re.match(r'^\d+.*?前$', useful['time']):
                    raise SpiderFinished()
                result.append(useful)
        except Exception as e:
            if isinstance(e, SpiderFinished):
                self.spiderOutOfRange = True
                raise
            print('[getData Error]', e)
        finally:
            return result

    def databaseUpdate(self, data):
        keys = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))

        sql = 'INSERT INTO {table} ({keys}) VALUES ({values}) ON DUPLICATE KEY UPDATE'.format(table=self.table, keys=keys, values=values)
        update = ', '.join([' {key} = %s'.format(key=key) for key in data])

        sql += update

        try:
            if self.cursor.execute(sql, tuple(data.values()) * 2):
                # print("> Success updating database")
                self.db.commit()
        except Exception as e:
            print('[databaseUpdate Error]', e)
            self.db.rollback()


    def saveData(self, res):
        for i in res:
            self.databaseUpdate(i)


    def run(self):
        MAX_PAGE = 10       # 设置一个爬取页面数的上限，防止太多出问题
        try:
            for page in range(MAX_PAGE):
                if self.spiderOutOfRange:   # 爬虫结束
                    print('> Spider Finished <')
                    return True
                url = self.basicUrl + '&page=%s' % page
                print('爬取中...', page)
                page = self.getPage(url)
                res = self.getData(page)
                self.saveData(res)
                time.sleep(0.2)
            return True
        except Exception as e:
            print('[Spider.run Error] ', e)
            return False


if __name__ == '__main__':
    w = WeiboSpider()
    w.run()