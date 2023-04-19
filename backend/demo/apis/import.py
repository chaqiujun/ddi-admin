from elasticsearch_dsl import connections, Document, Text, Date, Integer, Keyword, Index, Float
import json
import requests
# 加载.env环境变量
from dotenv import load_dotenv
load_dotenv()
import os

from scoreModel import get_transformer_Q, get_word2vec_Q
from domianTransModel import getDomainTypeNum
# from translateModel import translate_article
from datetime import datetime


connections.create_connection(hosts=['http://score.lingjoin.com:80'], timeout=20)

index_name = '测试_v12'
# 如果索引存在，删除索引
if Index(index_name).exists():
    print("存在同名index，已删除。")
    Index(index_name).delete()
# 定义新的索引
index = Index(index_name)

class Article(Document):
    id = Text()
    belong_index = Text()
    # 中文的
    title_cn = Text(analyzer='ik_smart', fields={'raw': Keyword()})
    keyword_cn = Text(analyzer='ik_smart', fields={'raw': Keyword()})
    abstract_cn = Text()
    content_cn = Text()
    language_cn = Text()
    # 未经处理外文的
    title_orgin = Text()
    keyword_orgin = Text()
    abstract_orgin = Text()
    content_orgin = Text()
    language_orgin = Text()
    site_orgin = Text()
    # 通用的
    domaintype_cn = Text()
    domaintype_num = Integer()
    publish_data = Date()
    publish_datatime = Date()
    url = Text()
    transformer_Q = Float()
    word2vec_Q = Float()
    ND_scientific_field = Text()
    technology_direction = Text()
    # 工作流程相关的
    xuanti_list = Integer()
    zhibao_list = Integer()
    zhengbian_list = Integer()
    shenhe_list = Integer()
    jianxun_list = Integer()
    xuanti_type = Integer()
    delect_list = Integer()
    star_list = Integer()

    class Index:
        name = index_name
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
            "analysis": {
                "analyzer": {
                    "ik": {
                    "tokenizer": "ik_smart"
                    }
                }
            },
        }
    # def save(self, ** kwargs):
    #     self.lines = len(self.body.split())
    #     return super(Article, self).save(** kwargs)

    # def is_published(self):
    #     return datetime.now() > self.published_from

Article.init() # Create the index


def getDataFromAPI():
    response = requests.get(os.environ.get('DATA_SOURCE_API')).json()
    data = response.get("data").get("doc_list")
    return data

def getDataFromJSON(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    doc_list = data.get("data").get("doc_list")
    return doc_list

for item in getDataFromJSON('/home/ubuntu/ddi-admin/backend/diy/data_json.json'):
    # transformer_Q_value,=getTitleScore(item.get("title")).get('transformer_Q'),
    # word2vec_Q_value,=getTitleScore(item.get("title")).get('word2vec_Q'),
    # print(getTitleScore(item.get("title")).get('word2vec_Q'))
    # print(transformer_Q_value)
    # write python circle
    print('word2vec_Q_value')
    try:
        doc = Article(
            _id=item.get("docno"), 
            id=item.get("docno"),
            belong_index=index_name,
            # translate_article(item.get("title"))
            title_cn=item.get("title"),
            keyword_cn=0,
            abstract_cn=item.get("title"),
            content_cn=item.get("title"),
            language_cn=None,
            # 未经处理外文的
            title_orgin=item.get("title"),
            keyword_orgin=item.get("keywords"),
            abstract_orgin=None,
            content_orgin=item.get("content"),
            language_orgin=item.get("language"),
            site_orgin=item.get("site"),
            # 通用的
            domaintype_cn=item.get("classification")[0].get("ND_scientific_field"),
            domaintype_num=getDomainTypeNum(item.get("classification")),
            publish_data=item.get("crawled")[:10],
            publish_datatime=item.get("crawled"),
            url=item.get("url"),
            transformer_Q=get_transformer_Q(item.get("title")),
            word2vec_Q=get_word2vec_Q(item.get("title")),
            ND_scientific_field=item.get("classification")[0].get("ND_scientific_field"),
            technology_direction=item.get("classification")[0].get("technology_direction"),
            # 工作流程相关的
            xuanti_list = 1,
            zhibao_list = 0,
            zhengbian_list = 0,
            shenhe_list = 0,
            jianxun_list = 0,
            xuanti_type = 0,
            delect_list = 0,
            star_list = 0,
            )
        # 这里是待解决的bug
        # doc.transformer_Q=getTitleScore(item.get("title")).get('transformer_Q'),
        # doc.word2vec_Q=getTitleScore(item.get("title")).get('word2vec_Q'),
        # doc.publish_data=item.get("crawled")[:10]

        doc.save()
        
    except Exception as e:
        print(f"Error importing document: {str(e)}")