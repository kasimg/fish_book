"""
Created by kasim on 2019/7/12 9:04
"""
from sqlalchemy import Column, Integer, String, Boolean, Float
from werkzeug.security import generate_password_hash, check_password_hash

from app import login_manager
from app.models.base import Base

from flask_login import UserMixin


class User(UserMixin, Base):
    # __tablename__ = 'user1' 改变表名
    id = Column(Integer, primary_key=True)
    nickname = Column(String(24), nullable=False)
    _password = Column('password', String(128), nullable=False)
    phone_number = Column(String(18), unique=True)
    email = Column(String(50), unique=True, nullable=False)
    confirmed = Column(Boolean, default=False)
    beans = Column(Float, default=0)
    send_counter = Column(Integer, default=0)
    receive_counter = Column(Integer, default=0)
    wx_open_id = Column(String(50))
    wx_name = Column(String(32))

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw_password):
        self._password = generate_password_hash(raw_password)

    def check_password(self, raw_password):
        return check_password_hash(self._password, raw_password)

    # def get_id(self):
    #     """
    #     和login_user配合使用，要用的话就必须定义这样的若干个固定函数
    #     更好的处理方法是直接继承相关的类
    #     如果模型中不是使用id来表示身份，那么有必要重写这个函数，返回表示id的属性
    #     :return:
    #     """
    #     return self.id

@login_manager.user_loader
def get_user(uid):
    """
    和login_required装饰器配合使用
    :param uid:
    :return:
    """
    return User.query.get(int(uid))