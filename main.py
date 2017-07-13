from flask import Flask
from flask import request, redirect
import json
from hashids import Hashids
from superMongoDB import SuperMongoDB
from bson import ObjectId
import pymongo
import urllib

app = Flask(__name__)
salt = 'this is haotian'
shortURL = SuperMongoDB(host='192.168.1.99',
                 port=27017)
db = shortURL.connectDB(databaseName='shortURL')
# # 建立索引
# result = db.profiles.create_index([('uid', pymongo.ASCENDING)],
#                                    unique=True)
shortURL.getCollection(collectionName='shortURL')


def isValidUrl(url):
    # 检测url有效性
    try:
        re = urllib.request.urlopen(url)
        print(re)
        return True
    except Exception as err:
        print(err)
        return False


# /api?shorterurl=www.xx.com
@app.route('/api', methods=['POST', 'GET'])
def shorterURL():
    if request.method == 'POST':
        url = request.form.get('shorter_url', '')
    else:
        url = request.args.get('shorter_url', '')

    # 检测url有效性
    if isValidUrl(url):
        status = 'Success'
        short_url = generateID(url)
    else:
        status = 'Fail'
        short_url = None

    re = {
        'status': status,
        'raw_url': url,
        'short_url': short_url
    }
    return  json.dumps(re)


@app.route('/<hashid>')
def shortUrlDecode(hashid):
    # 查找是否有url
    query = {
        'hashid': hashid
    }
    re = shortURL.findCondition(query)
    if re == []:
        return '没有找到'

    redirect_url = re[0]['raw_url']
    i = redirect_url.find('http')
    print(i)
    if i == -1:
        return redirect('http://'+redirect_url)
    return redirect(redirect_url)


def generateID(url):
    # 查询当前maxLen
    query = {
        'name': 'Config'
    }
    re = shortURL.findCondition(query)
    for i in re:
        # maxLen = i.get('max_length')
        incre_id = i.get('incre_id')
        # print('当前MaxLen: ', maxLen)
        print('incre_id: ', incre_id)

    # 查找重复url
    query = {
                'raw_url': url,
            }
    re = shortURL.findCondition(query)
    if re != []:
        print('url已被添加')
        for i in re:
            # print('raw_url id: ', i['hashid'])
            return i['hashid']

    # 得到递增id 并更新
    coll = shortURL.getCollection(collectionName='shortURL')
    new_id = coll.find_and_modify(update={"$inc": {"incre_id_len": 1}},
                                  query={'name': 'Config'},  # 在config里面计数
                                  new=True).get("incre_id_len")
    print('new_id', new_id, type(new_id))

    # 插入
    hashids = Hashids(salt=salt)
    hashid = hashids.encode(new_id)

    data = {
        'incre_id': new_id,
        'name': 'url',
        'hashid': hashid,
        'raw_url': url
    }
    re = shortURL.insert(data)
    print(re)
    return hashid


def initialIDconfig():
    # 查找是否有初始化
    query = {
        'name': 'Config'
    }
    re = shortURL.findCondition(query)
    print(re)
    if re == []:
        data = {
            'name': 'Config',
            # 'max_length': 2,
            'incre_id_len': 0,
        }
        shortURL.insert(data)
        print('初始化成功')
    else:
        print('已初始化')


if __name__ == '__main__':
    initialIDconfig()

    config = dict(
        debug=True,
        host='0.0.0.0',
        port=1888,
    )
    app.run(**config)

