#!/usr/bin/env python
# -*- coding: utf-8 -*-
# time: 2022/7/21 14:01
# file: api.py
# author: 臧成龙
# QQ: 939589097
from typing import List 
# 用于获取404错误，或者获取对象
from django.shortcuts import get_object_or_404
from ninja import Field, ModelSchema, Query, Router, Schema
# 用于分页
from ninja.pagination import paginate
# 用于CRUD操作
from utils.fu_crud import create, delete, retrieve, update
# 添加自定义的过滤器和分页器
from utils.fu_ninja import FuFilters, MyPagination
# 从 utils 应用中导入 FuResponse 类，用于封装返回的数据。
from utils.fu_response import FuResponse
# 从 utils 应用中导入 list_to_route 和 list_to_tree 方法，用于将列表转化为树形结构。
from utils.list_to_tree import list_to_route, list_to_tree
# 使用es dsl工具
from elasticsearch_dsl import connections, Search, Q
import json
from datetime import datetime, timedelta, date
from .apis.nlpir_cloud_new_words_finder import new_words_finder
from .apis.domianTransModel import reconstructDomainTypeNum
from .apis.nlpir_cloud_key_extract import key_extract
router = Router()

from demo.models import Demo
from utils.fu_crud import (
    ImportSchema,
    create,
    delete,
    export_data,
    import_data,
    retrieve,
    update,
)
from utils.fu_ninja import FuFilters, MyPagination

router = Router()


# 设置过滤字段
class Filters(FuFilters):
    name: str = Field(None, alias="name")
    code: str = Field(None, alias="code")
    status: int = Field(None, alias="status")
    id: str = Field(None, alias="demo_id")


# 设置请求接收字段
class DemoSchemaIn(ModelSchema):
    remark: list

    class Config:
        model = Demo
        model_fields = ['name', 'code', 'sort', 'status']


# 设置响应字段
class DemoSchemaOut(ModelSchema):

    class Config:
        model = Demo
        model_fields = ['id', 'name', 'code', 'sort', 'status', 'remark', 'create_datetime']


# 创建Demo
@router.post("/demo", response=DemoSchemaOut)
def create_demo(request, data: DemoSchemaIn):
    data.remark = ','.join(data.remark)
    demo = create(request, data, Demo)
    return demo


# 删除Demo
@router.delete("/demo/{demo_id}")
def delete_demo(request, demo_id: int):
    delete(demo_id, Demo)
    return {"success": True}


# 更新Demo
@router.put("/demo/{demo_id}", response=DemoSchemaOut)
def update_demo(request, demo_id: int, data: DemoSchemaIn):
    data.remark = ','.join(data.remark)
    demo = update(request, demo_id, data, Demo)
    return demo


# 获取Demo
@router.get("/demo", response=List[DemoSchemaOut])
@paginate(MyPagination)
def list_demo(request, filters: Filters = Query(...)):
    qs = retrieve(request, Demo, filters)
    return qs


# 导入
@router.get("/demo/all/export")
def export_demo(request):
    export_fields = ['name', 'code', 'status']
    return export_data(request, Demo, DemoSchemaOut, export_fields)


# 导出
@router.post("/demo/all/import")
def import_demo(request, data: ImportSchema):
    import_fields = ['name', 'code', 'status']
    return import_data(request, Demo, DemoSchemaIn, data, import_fields)



# ===============================================接口API==================================================


# Define a default Elasticsearch client
connections.create_connection(hosts=['http://score.lingjoin.com:80'])
conn = connections.get_connection()
def date_range(range_id):
    today = date.today()
    start_date = today - timedelta(days=range_id)
    end_date = today
    return {'start_date':start_date, 'end_date':end_date}


@router.post("/xuanti_list_count/{range_id}")
def get_info_source_count(request,range_id: int):
    start_date = date_range(range_id).get('start_date')
    end_date = date_range(range_id).get('end_date')
    query = Q('match', xuantilist=1) & Q('range', publishTime={'gte': start_date, 'lte': end_date})
    search = Search(using=conn, index='es_index_v3').query(query)
    result = search.count()
    return {"xuanti_list_count": result,"range_id":range_id,"start_time":start_date,"end_time":end_date}

@router.post("/zhengbian_list_count/{range_id}")
def get_info_source_count(request, range_id:int):
    start_date = date_range(range_id).get('start_date')
    end_date = date_range(range_id).get('end_date')
    query = Q('match', zhengbianlist=1) & Q('range', publishTime={'gte': start_date, 'lte': end_date})
    search = Search(using=conn, index='es_index_v3').query(query)
    result = search.count()
    return {"zhengbian_list_count": result,"range_id":range_id,"start_time":start_date,"end_time":end_date}

@router.post("/shenhe_list_count/{range_id}")
def get_info_source_count(request, range_id:int):
    start_date = date_range(range_id).get('start_date')
    end_date = date_range(range_id).get('end_date')
    query = Q('match', shenhelist=1) & Q('range', publishTime={'gte': start_date, 'lte': end_date})
    search = Search(using=conn, index='es_index_v3').query(query)
    result = search.count()
    return {"shenhe_list_count": result,"range_id":range_id,"start_time":start_date,"end_time":end_date}

@router.post("/jianxun_list_count/{range_id}")
def get_info_source_count(request, range_id:int):
    start_date = date_range(range_id).get('start_date')
    end_date = date_range(range_id).get('end_date')
    search = Search(using=conn, index='es_index_v3') \
             .query(Q('match', jianxunlist=1) & Q('range', publishTime={'gte': start_date, 'lte': end_date}))
    result=search.count()
    return {'jianxun_list_count': result, 'range_id': range_id, 'start_time': start_date, 'end_time': end_date}

@router.post("/smart_recommendation/{range_id}")
def get_smart_recommendation(request, range_id:int):
    start_date = date_range(range_id).get('start_date')
    end_date = date_range(range_id).get('end_date')
    search = Search(using=conn, index='es_index_v3') \
             .query(Q('term', delectlist=0) & Q('range', publishTime={'gte': start_date, 'lte': end_date})) \
             .sort('-word2vec_Q')
    response = search[:7].source(['title', 'publishTime']).execute()
    result_list = [{'title': hit.title, 'publishTime': hit.publishTime} for hit in response.hits]
    return {'domain_count': result_list}

@router.post("/domain_count/{range_id}")
def get_domain_count(request, range_id:int):
    start_date = date_range(range_id).get('start_date')
    end_date = date_range(range_id).get('end_date')
    search = Search(using=conn, index='es_index_v3')\
            .query(Q('range', publishTime={'gte': start_date, 'lte': end_date}))
    domaintype_counts = {}
    for hit in search.execute():
        domaintype = hit.domaintype
        if domaintype not in domaintype_counts:
            domaintype_counts[domaintype] = 0
        domaintype_counts[domaintype] += 1
    domain_count_list=[]
    for domaintype, count in domaintype_counts.items():
        domain_count_list.append((reconstructDomainTypeNum(domaintype), count))
    domain_count_list.sort(key=lambda x: x[1], reverse=True)
    return {"domain_count": domain_count_list[:7]}

@router.post("/new_word_discovery/{range_id}")
def get_new_word_discovery(request, range_id:int):
    start_date = date_range(range_id).get('start_date')
    end_date = date_range(range_id).get('end_date')
    query = Q('range', publishTime={'gte': start_date, 'lte': end_date})
    search = Search(using=conn, index='es_index_v3').query(query)
    response = search.execute()
    data_list = []
    for hit in response:
        data_list.append(hit.contentAbstract)
    res = new_words_finder(data_list)
    return {"new_word_discovery": res, "range_id": range_id, "start_time": start_date, "end_time": end_date}


@router.post("/information_hotspot/{range_id}")
def get_information_hotspot(request, range_id:int):
    query = Q('match', starlist=1)
    search = Search(using=conn, index='es_index_v3').query(query)
    response = search.execute()
    data_list = []
    for hit in response:
        data_list.append(hit.contentAbstract)
    res = key_extract(data_list)
    print(res)
    return {"information_hotspot": res}

@router.post("/word_cloud/{range_id}")
def get_word_cloud(request, range_id:int):
    query = Q('match', starlist=1)
    search = Search(using=conn, index='es_index_v3').query(query)
    response = search.execute()
    data_list = []
    for hit in response:
        data_list.append(hit.contentAbstract)
    res = key_extract(data_list)
    print(res)
    return {"word_cloud": res}


@router.post("/data_trend/{range_id}")
def get_data_trend(request, range_id:int):
    query = Q('range', publishTime={'gte': 'now-1y', 'lte': 'now'})

    # 统计每个月份的文档数量
    month_counts = {}
    current_month = datetime.now().replace(day=1)
    for i in range(12):
        # 计算本月的起始时间和结束时间
        start_time = current_month - timedelta(days=current_month.day-1)
        end_time = current_month + timedelta(days=32-current_month.day)
        current_month -= timedelta(days=current_month.day)

        # 创建一个查询对象，只包含 publishtime 属性在本月的文档
        month_query = query & Q('range', publishTime={'gte': start_time, 'lte': end_time})

        # 创建一个搜索对象，并执行查询
        search = Search(using=conn, index='es_index_v3').query(month_query)
        response = search.execute()

        # 统计本月份的文档数量
        count = response.hits.total.value
        month_counts[start_time.strftime('%Y-%m')] = count

    # # 输出表格形式的结果
    month_counts_list = []
    for month, count in month_counts.items():
        month_counts_list.append((month, count))
    return {"data_trend": month_counts_list}

from django.contrib import auth
from django.forms import model_to_dict
from django.shortcuts import get_object_or_404
from ninja import Router, ModelSchema, Query, Schema, Field

from fuadmin.settings import SECRET_KEY, TOKEN_LIFETIME
from system.models import Users, Role, MenuButton, MenuColumnField
from utils.fu_jwt import FuJwt
from utils.fu_response import FuResponse
from utils.request_util import save_login_log
from utils.usual import get_user_info_from_token



# ================登录相关接口=================
class SchemaOut(ModelSchema):

    class Config:
        model = Users
        model_exclude = ['password', 'role', 'post']


class LoginSchema(Schema):
    username: str = Field(None, alias="username")
    password: str = Field(None, alias="password")


class Out(Schema):
    multi_depart: str
    sysAllDictItems: str
    departs: str
    userInfo: SchemaOut
    token: str

@router.post("/login", response=Out, auth=None)
def login(request, data: LoginSchema):
    user_obj = auth.authenticate(request, **data.dict())
    if user_obj:
        request.user = user_obj
        role = user_obj.role.all().values('id')
        post = list(user_obj.post.all().values('id'))
        role_list = []
        post_list = []
        for item in role:
            role_list.append(item['id'])
        for item in post:
            post_list.append(item['id'])
        user_obj_dic = model_to_dict(user_obj)
        user_obj_dic['post'] = post_list
        user_obj_dic['role'] = role_list
        del user_obj_dic['password']
        del user_obj_dic['avatar']

        time_now = int(datetime.now().timestamp())
        jwt = FuJwt(SECRET_KEY, user_obj_dic, valid_to=time_now + TOKEN_LIFETIME)
        # 将生成的token加入缓存
        # cache.set(user_obj.id, jwt.encode())
        token = f"bearer {jwt.encode()}"
        data = {
            "multi_depart": 1,
            "sysAllDictItems": "q",
            "departs": "e",
            'userInfo': user_obj_dic,
            'token': token
        }
        save_login_log(request=request)
        return data
    else:
        return FuResponse(code=500, msg="账号/密码错误")