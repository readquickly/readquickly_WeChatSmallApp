import pymongo
import time

'''
爬取的数据（News）的数据库（MongoDB）的读写
    数据库在本地，端口默认（localhost:27017）
    `getDatabaseName()`: 得到 MongoDB 中的 Database name
    `getDatabaseCollection()`: 得到要使用的 Collection
    `writeToDatabase(databaseName, databaseCollection, data)`: 把 (useful list) data 写入 MongoDB
    `readFromDatabase(databaseName, databaseCollection)`: 从数据课中读出一个 useful list
    `parseReadData(data)`: 在 readFromDatabase 中使用，将从 MongoDB 中读取的数据转化为 useful list
'''

def getDatabaseName():
    '''
    获取用来储存结果的 MongoDB 中的数据库名称，"readquickly_news"
    '''
    return "readquickly_news"


def getDatabaseCollection():
    '''
    获取**当天**用来储存结果的 MongoDB 中的 Collection 名称，用当天的日期，例如 'Wed_2019_04_24'
    '''
    # 获得当前时间时间戳
    now = time.time()
    # 转换为需要的日期格式, 如:"Wed_2019_04_24"
    timeStruct = time.localtime(now)
    strDate = time.strftime("%a_%Y_%m_%d", timeStruct)
    # 返回格式化后的格式作为 Collection 的名称
    return strDate


def writeToDatabase(databaseName, databaseCollection, data):
    '''
    写数据库
    '''
    try:
        # 连接数据库
        client = pymongo.MongoClient(host='localhost', port=27017)
        db = client[databaseName]
        collection = db[databaseCollection]
        # 插入数据
        # 存在标题相同的则更新，不存在新建
        for item in data:
            collection.update_one(
                {'title': item['title']},
                {'$set': item},
                upsert=True
                )
    except Exception as e:
        print('[NewsDatabase.writeToDatabase Error] False to write data to database: %s' % e)
        # 为防止数据丢失，把数据写到标准输出
        print('Output data in stdout:\n%s' % ('-' * 10))
        print(data)
        print('-' * 10)
    finally:
        # 关闭数据库连接
        client.close()


def parseReadData(data):
    '''
    把 MongoDB 中读出来的数据整理成标准的 useful data
    主要是需要去掉 MongoDB 为数据加入的 '_id'，它的值不是标准对象，防止 json 时麻烦，把它删掉
    '''
    useful = data
    for i in useful:
        if i.get('_id'):
            del i['_id']
    return useful


def readFromDatabase(databaseName, databaseCollection):
    '''
    读数据库
    '''
    data = None
    try:
        # 连接数据库
        client = pymongo.MongoClient(host='localhost', port=27017)
        db = client[databaseName]
        collection = db[databaseCollection]
        # 读取数据
        raw = collection.find()
        if raw:
            ls = list(raw)
            data = parseReadData(ls)

    except Exception as e:
        print('[NewsDatabase.readFromDatabase Error] False to read data from database: %s' % e)
    finally:
        # 关闭数据库连接
        client.close()
        return data

