"""
Created by kasim on 2019/7/9 15:52
"""
from sqlalchemy import Column, Integer, String  # 基础内容直接用原生包

from app.models.base import Base


class Book(Base):  # 这里的继承类导致了类中的信息被获取
    # print(11)
    # print(db.Model.metadata.tables)
    """
    书本的数据模型
    业务逻辑写在这里，即模型层中
    code first 思想，根据业务逻辑设计数据表，专注于业务而非数据库本身
        所以使用python代码生成数据表
    """
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50), nullable=True)
    author = Column(String(30), default='佚名')
    binding = Column(String(20))  # 装订版本（精装/平装）
    publisher = Column(String(50))
    price = Column(String(20))
    pages = Column(Integer)
    pub_data = Column(String(20))
    isbn = Column(String(15), nullable=False, unique=True)
    summary = Column(String(1000))
    image = Column(String(50))
    # print(db.Model.metadata.tables)
# print(2)
# print(db.Model.metadata.tables)