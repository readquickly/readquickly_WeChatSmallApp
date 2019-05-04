from . import wieboPeoplesDaily
from . import kr36NewsFlashes
from . import cctvKuaikan

def run():
    print('爬取"CCTV快看"...')
    c = cctvKuaikan.kuaikanCctv()
    c.run()
    print('完成。')

    print('爬取"36氪快讯"...')
    k = kr36NewsFlashes.NewsFlashes36Kr()
    k.run()
    print('完成。')

    print('爬取"人民日报微博"...')
    p = wieboPeoplesDaily.WeiboSpider()
    p.run()
    print('完成。')


if __name__ == '__main__':
    run()
