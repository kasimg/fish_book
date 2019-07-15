"""
Created by kasim on 2019/7/12 9:02
"""
from datetime import datetime
from contextlib import contextmanager

from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy, BaseQuery  # 和数据库交互时使用flask封装后的包
from sqlalchemy import Column, Integer, SmallInteger

class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit() #  因为需要捕捉错误，所以这句要在这里执行
        except Exception as e:
            db.session.rollback()
            raise e

class Query(BaseQuery):
    #  重写filter_by方法，加上status关键字
    def filter_by(self, **kwargs):
        if 'status' not in kwargs.keys(): #  kwargs 是字典
            kwargs['status'] = 1
        return super(Query, self).filter_by(**kwargs) #  这里需要解包

db = SQLAlchemy(query_class=Query)  # 初始化db对象, app初始化时导出进行相关操作

class Base(db.Model):
    __abstract__ = True
    create_time = Column('create_time', Integer)
    status = Column(SmallInteger)

    def __init__(self):
        self.create_time = int(datetime.now().timestamp())

    def set_attrs(self, attrs_dict):
        """
        因为表单校验中的属性名和模型中的属性名相同
        如果有同名的key，那么就直接赋值
        :param attrs_dict:
        :return:
        """
        for key, value in attrs_dict.items():
            if hasattr(self, key) and key != 'id':
                setattr(self, key, value)

    @property
    def create_datetime(self):
        if self.create_time:
            return datetime.fromtimestamp(self.create_time)
        else:
            return None