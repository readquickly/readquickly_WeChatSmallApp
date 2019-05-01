import pymongo
import time

'''
爬取的数据（Notices）的数据库（MongoDB）的读写
    数据库在本地，端口默认（localhost:27017）
    `getDatabaseName()`: 得到 MongoDB 中的 Database name
    `getDatabaseCollection()`: 得到要使用的 Collection
    `writeToDatabase(databaseName, databaseCollection, data)`: 把 (useful list) data 写入 MongoDB
    `readFromDatabase(databaseName, databaseCollection)`: 从数据课中读出一个 useful list
    `parseReadData(data)`: 在 readFromDatabase 中使用，将从 MongoDB 中读取的数据转化为 useful list
    `updataLiveNotices()`: 在 readFromDatabase 中检测消息是否过期，依此分类
    Collections：
        使用一个固定的名称"live"，来代表现在还有效的消息。
        把过期的消息放到一个名叫"outdated"的collection。
'''

LIVE_COLLECTION = "live"
OUTDATE_COLLECTION = "outdated"

def getDatabaseName():
    '''
    获取用来储存结果的 MongoDB 中的数据库名称，"readquickly_notices"
    '''
    return "readquickly_notices"


def getDatabaseCollection():
    '''
    获取储存有效的（未过期的）消息的 Collection 名称
    '''
    return LIVE_COLLECTION


def getOutdateCollection():
    '''
    获取已过期的消息 Collection 名称
    '''
    return OUTDATE_COLLECTION


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
        print('[NoticesDatabase.writeToDatabase Error] False to write data to database: %s' % e)
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

def isFresh(item):
    '''
    判断是否还有效，expires为数据的到期时长(int，小时为单位)
    '''
    dateTime = item.get('time')
    expiresHour = item.get('expires') or 0
    expiresHour = int(expiresHour)
    expireSecond = expiresHour * 60 * 60
    
    if dateTime:
        timeFormat = '%Y-%m-%d %H:%M'
        publishTime = time.mktime(time.strptime(dateTime, timeFormat))      # 发布时间 -> 时间戳
        currentTime = time.time()       # 当前时间 -> 时间戳
        if currentTime - publishTime <= expireSecond:
            return True
    return False


def updataLiveNotices(collection):
    try:
        # 遍历，查找新过期的
        outdates = []
        for item in collection.find():
            if not isFresh(item):
                outdates.append(item)
        # 写入过期集
        writeToDatabase(getDatabaseName(), getOutdateCollection(), outdates)
        # 从有效集删除
        for item in outdates:
            collection.delete_one({'title': item.get('title', '')})
    except Exception as e:
        print('[NoticesDatabase.updateDatabase Error] False to update database: %s' % e)


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
        # 更新数据库
        updataLiveNotices(collection)
        # 读取数据
        raw = collection.find()
        if raw:
            ls = list(raw)
            data = parseReadData(ls)
    except Exception as e:
        print('[NoticesDatabase.readFromDatabase Error] False to read data from database: %s' % e)
    finally:
        # 关闭数据库连接
        client.close()
        return data

