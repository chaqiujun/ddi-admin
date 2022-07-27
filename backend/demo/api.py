#!/usr/bin/env python
# -*- coding: utf-8 -*-
# time: 2022/7/21 14:01
# file: api.py
# author: 臧成龙
# QQ: 939589097

from typing import List
from ninja import Router, ModelSchema, Query, Field
from ninja.pagination import paginate

from demo.models import Demo
from utils.fu_crud import create, delete, update, retrieve, ImportSchema, export_data, import_data
from utils.fu_ninga import MyPagination, FuFilters

router = Router()


# 设置过滤字段
class Filters(FuFilters):
    name: str = Field(None, alias="name")
    code: str = Field(None, alias="code")
    status: int = Field(None, alias="status")
    id: str = Field(None, alias="demo_id")


# 设置请求接收字段
class DemoSchemaIn(ModelSchema):
    class Config:
        model = Demo
        model_fields = ['name', 'code', 'sort', 'status']


# 设置响应字段
class DemoSchemaOut(ModelSchema):
    class Config:
        model = Demo
        model_fields = "__all__"


# 创建Demo
@router.post("/demo", response=DemoSchemaOut)
def create_demo(request, data: DemoSchemaIn):
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
    title_dict = {
        'name': '名称',
        'code': '编码',
        'status': '状态',
        'sort': '排序',
    }
    return export_data(request, Demo, DemoSchemaOut, title_dict)


# 导出
@router.post("/demo/all/import")
def import_demo(request, data: ImportSchema):
    title_dict = {
        '名称': 'name',
        '编码': 'code',
        '状态': 'status',
        '排序': 'sort',
    }
    return import_data(request, Demo, DemoSchemaIn, data, title_dict)