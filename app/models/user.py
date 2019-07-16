"""
Created by kasim on 2019/7/12 9:04
"""
from flask import current_app
from sqlalchemy import Column, Integer, String, Boolean, Float
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from app import login_manager
from app.libs.helper import is_isbn_or_key
from app.models.base import Base, db

from flask_login import UserMixin

from app.models.gift import Gift
from app.models.wish import Wish
from app.spider.yushu_book import YuShuBook


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


    def can_save_to_list(self, isbn):
        """
        放在这里可以提升复用性
        :param isbn:
        :return:
        """
        if is_isbn_or_key(isbn) != 'isbn': #  如果isbn号不合法，那么不允许存入
            return False
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(isbn)
        if not yushu_book.only_book: #  如果库中没有，那么无法添加到心愿清单
            return False
        #  书赠送出去之前，不允许添加同ISBN号的书
        #  一个用户不可能同时是赠送者或者索要者
        in_gift_list = Gift.query.filter_by(uid=self.id, isbn=isbn, launched=False).first()
        in_wish_list = Wish.query.filter_by(uid=self.id, isbn=isbn, launched=False).first()

        if not in_gift_list and not in_wish_list:
            return True
        else:
            return False
    # def get_id(self):
    #     """
    #     和login_user配合使用，要用的话就必须定义这样的若干个固定函数
    #     更好的处理方法是直接继承相关的类
    #     如果模型中不是使用id来表示身份，那么有必要重写这个函数，返回表示id的属性
    #     :return:
    #     """
    #     return self.id

    def generate_token(self, expiration=600):
        """
        生成token
        :param expiration:
        :return:
        """
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'id': self.id}).decode('utf-8')

    @staticmethod
    def reset_password(token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))  # 因为参数要求是字节码，所以要编码
        except:
            return False
        uid = data.get('id')
        with db.auto_commit():
            user = User.query.get(uid)  # 主键查询时可以简化操作，直接使用get
            user.password = new_password
        return True
@login_manager.user_loader
def get_user(uid):
    """
    和login_required装饰器配合使用
    根据id把用户数据转化为user模型
    和数据库配合使用
    :param uid:
    :return:
    """
    return User.query.get(int(uid))