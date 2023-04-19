import requests
import os
import json
# 加载.env环境变量
from dotenv import load_dotenv
load_dotenv()

def getTitleScore(text):
    query = {"data":{"title": text,"ID":'1'}}
    response = requests.post(os.environ.get('SORT_API'), data=json.dumps(query))
    result = response.json().get('data')[0]
    return result

def get_transformer_Q(text):
    transformer_Q_value=getTitleScore(text).get('transformer_Q')
    return transformer_Q_value

def get_word2vec_Q(text):
    word2vec_Q_value=getTitleScore(text).get('word2vec_Q')
    return word2vec_Q_value

# 测试接口模型
# 支持中英文
if __name__ == '__main__':
    print(get_transformer_Q("Study: Unfair labor practices delay first union contracts"))