"""
Created by kasim on 2019/7/12 9:02
"""
from flask_sqlalchemy import SQLAlchemy  # 和数据库交互时使用flask封装后的包
from sqlalchemy import Column, Integer, SmallInteger

db = SQLAlchemy()  # 初始化db对象, app初始化时导出进行相关操作

class Base(db.Model):
    __abstract__ = True
    status = Column(SmallInteger)

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