"""
Created by kasim on 2019/7/12 9:11
"""
from contextlib import contextmanager

from flask import current_app
from flask_login import current_user
from sqlalchemy import Column, Integer, ForeignKey, Boolean, String, desc, func
from sqlalchemy.orm import relationship

from app.models.base import Base, db
from app.spider.yushu_book import YuShuBook


class Gift(Base):
    id = Column(Integer, primary_key=True)
    user = relationship('User')
    uid = Column(Integer, ForeignKey('user.id'))
    isbn = Column(String(15), nullable=False)
    # a = Wish()Wish
    # book = relationship('Book')
    # bid = Column(Integer, ForeignKey('book.id'))
    launched = Column(Boolean, default=False)

    def is_your_own_book(self, uid):
        return True if self.uid == uid else False

    @classmethod
    def get_user_gifts(cls, uid):
        """
        获取赠送清单中该用户的所有记录
        :param uid:
        :return:
        """
        gifts = Gift.query.filter_by(uid=uid, launched=False).order_by(
            desc(Gift.create_time)).all()

        return gifts

    @classmethod
    def get_wish_counts(cls, isbn_list):

        """
        根据传入的一组isbn，到wish表中查询出某个礼物的心愿数量
        :return:
        """
        from app.models.wish import Wish
        # query后面跟的是对查询结果的操作，根据业务需求返回想要的数据
        count_list = db.session.query(Wish.isbn, func.count(Gift.id)).filter(
            Gift.launched == False,
            Gift.isbn.in_(isbn_list),
            Gift.status == 1).group_by(
            Gift.isbn).all()
        # [dict(isbn=record[0], count=record[1]) for record in count_list]
        return [dict(isbn=record[0], count=record[1]) for record in count_list]

    @property
    def book(self):
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(self.isbn)
        return yushu_book.only_book

    # 对象表示一个礼物，具体
    # 类表示礼物这一概念，抽象
    @classmethod
    def recent(cls):
        """
        all()是触发函数，遇到all就会生成一条sql
        :return:
        """
        recent_gift = Gift.query.filter_by(
            launched=False).group_by(
            Gift.isbn).order_by(
            desc(Gift.create_time)).limit(
            current_app.config['RECENT_BOOK_COUNT']).distinct().all()
        return recent_gift
    # def add_gift_to_list(self):
    #     gift = Gift()
    #     gift.isbn = self.isbn
    #     gift.uid = current_user.id  # current_user就是一个user模型，可理解为user类的实例化对象
    #
    #     current_user.beans += current_app.config['BEANS_UPLOAD_ONE_BOOK']  # 增加鱼豆
    #     db.session.add(gift)
    #     db.session.commit()
    # yield gift
    # db.session.rollback()  # 如果出错则需要回滚

    # @contextmanager
    # def gift_ctx_manager(self):
    #     pass
# 此模块第一次被执行时，类对象被初始化，初始化过程只涉及类变量
# 只要类变量的定义过程中没有使用Wish，那么就可以把Wish的导入放到最后
# 之后，再调用要使用Wish的方法时，此模块已经执行完成，Wish已经被导入
# from app.models.wish import Wish