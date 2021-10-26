import flask
import json
from MongoDB import mongo_db
import random

app = flask.Flask(__name__)


@app.route('/')
def welcome():
    return 'Welcome to proxyPoolWeb!'


# 从数据库中获取一个ip代理
@app.route('/one')
def get_one():
    proxies = mongo_db.MongoDB().get_all()
    print(len(proxies))
    result = [proxy['proxy'] for proxy in proxies]
    x = random.randint(0, mongo_db.MongoDB().get_count() - 1)
    # 返回json格式的类似字典的字符串
    return json.dumps(dict(proxy=result[x]))


# 从数据库中获取所有的ip代理
@app.route('/all')
def get_all():
    #  http://127.0.0.1:5000/many?count=2
    # args = flask.request.args  # 参数提交
    proxies = mongo_db.MongoDB().get_all()
    result = [proxy['proxy'] for proxy in proxies]
    return json.dumps(result)


def run():
    app.run()


if __name__ == '__main__':
    app.run()
