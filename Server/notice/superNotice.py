'''
手动消息接口
'''
from . import noticesDatabase

def saveData(data):
    '''
    data: 传入结果数据的 useful list
    '''
    try:
        if data:
            dbName = noticesDatabase.getDatabaseName()
            dbCollection = noticesDatabase.getDatabaseCollection()
            noticesDatabase.writeToDatabase(dbName, dbCollection, data)
        else:
            raise RuntimeError('data == None')
    except Exception as e:
        print('[saveData Error] ', e)
        return None