from pymongo import MongoClient
from pymongo.errors import ConnectionFailure



class SuperMongoDB(object):
    def __init__(self, host=None, port=27017):
        self.host = host
        self.port = port
        self.db = None
        self.collection = None

    def connectDB(self, databaseName):
        # 设置数据库timeout的时间为1s
        client = MongoClient(self.host, self.port, serverSelectionTimeoutMS= 1000)
        try:
            # The ismaster command is cheap and does not require auth.
            client.admin.command('ismaster')
        except ConnectionFailure:
            print("Server not available")
            return None

        print('连接数据库成功', client)
        connection = client[databaseName]
        self.db = connection
        return connection

    def getCollection(self, collectionName):
        if self.db == None:
            print('请先连接到数据库，connect()')
            return None
        collection = self.db[collectionName]
        # print(collection)
        self.collection = collection
        return collection

    def insert(self, data):
        """data的格式为字典
        data = {
            'aklsfj': False,
            'askldfj': 'gua',
        }
        """
        re = self.collection.insert(data)
        print('      DB: insert', re)

    def findCondition(self, query={}, field=None):
        """
        # 普通查询方法
        query = {
            '随机值': 1,
            'name': 'gua'
        }
        # 查询 随机值 大于 1 的所有数据
        query = {
            '随机值': {
                '$gt': 1
            },
        }
        # 查询 $or 
        query = {
            '$or': [
                {
                    '随机值': 2,
                },
                {
                    'name': 'GUA'
                }
            ]
        }
        # 部分查询 field 用法
        # 字段: 1 表示提取这个字段
        # 不传的 默认是 0 表示不提取
        # _id 默认是 1
        field = {
            'name': 1,
            '_id': 0,
        }
        """

              # if field == None:
        #     result = list(self.collection.find(query))
        # else:
        #     result = list(self.collection.find(query, field))
        # return result

        try:
            if field == None:
                result = list(self.collection.find(query))
            else:
                result = list(self.collection.find(query, field))
            return result
        except Exception as error:
            print('ERROR: ', error)
            return False


    def findAll(self):
        data = list(self.collection.find())
        print('所有数据', data)
        return data

    def findOne(self, query={}):
        return self.collection.find_one(query)

    def update(self, query, form, options):
        """
        :param query: 查询条件
        :param form: 更新的内容
        :param options: 是否多项修改
        :return: 
        """
        """ 用例
        query = {
            '随机值': 1,
        }
        form = {
            '$set': {
                'name': '更新 22222',
            }
        }
        options = {
            'multi': True,
        }
        """
        collection = self.collection
        collection.update(query, form, **options)


if __name__ == "__main__":
    mongoDb = SuperMongoDB(host='192.168.1.99',
                           port=27017)
    mongoDb.connectDB(databaseName='chat_robot_log')
    mongoDb.getCollection(collectionName='log_chicken')

    list = ''
    with open('./xiaohuangji.json', 'r', encoding='utf-8') as f:
        list = eval(f.read())
        print(list)
        print(type(list))

    mongoDb.insert(list)



    #
    # data = {}
    #
    # mongoDb.insert()
    #
    # query = {
    #     'question': '你好啊ddd'
    # }
    # field = {'_id': 0}
    # r = mongoDb.findCondition({},field)
    # print(r)
    # # if r != []:
    # #     answer = r[-1]['answer']
    # #     print(answer)
