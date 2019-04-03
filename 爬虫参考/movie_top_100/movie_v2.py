import re
import json
import time

import requests

url = 'https://maoyan.com/board/4'
result = {'top movies': []}
filename = './movies_2.txt'

pattern = r'<dd>.*?board-index.*?>(.*?)</i>.*?data-src="(.*?)@.*?title="(.*?)".*?主演：(.*?)\s*</p>.*?上映时间：(.*?)</p>.*?integer">(.*?)</i>.*?fraction">(.*?)</i></p>'

headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15',
        'Accept-Language': 'zh-cn'
        }


def get_page(url):   # 抓取页面，返回html字符串
    print('\tGetting...')
    try:
        response = requests.get(url, headers=headers)
        return response.text
    except Exception as e:
        print('[Error]', e)
        return ''


def stars_split(st):
    return st.split(',')


def extract(html):  # 正则提取，返回结果dict的list
    print('\tExtracting...')
    raws = re.findall(pattern, html, re.S)   # [(排名, 图片地址, 名称, 主演, 上映时间, 评分整数部分, 评分小数部分), ...]
    result = []
    for raw in raws:
        dc = {                      # 在这里调整了顺序
                'index': raw[0],
                'title': raw[2],
                'stars': stars_split(raw[3]),   # 分离主演
                'otime': raw[4],
                'score': raw[5] + raw[6],       # 合并整数、小数
                'image': raw[1]
                }
        result.append(dc)

    return result
    

def merge(data):
    print('\nMerging...')
    result['top movies'] += data
    
    
def save(data):      # 写入文件
    print('Saving...')
    with open(filename, 'a', encoding='utf-8') as f:
        f.write(json.dumps(data, ensure_ascii=False))


if __name__ == '__main__':
    for i in range(0, 100, 10):     # 翻页
        target = url + '?offset=' + str(i)
        print('[%s%%](%s)' % (i, target))
        page = get_page(target)
        data = extract(page)
        merge(data)
        time.sleep(0.5)     # 防制请求过密集被封
        
    save(result)
    print('[100%] All Finished.\n Results in', filename)
