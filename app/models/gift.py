"""
Created by kasim on 2019/7/12 9:11
"""
from contextlib import contextmanager

from flask import current_app
from flask_login import current_user
from sqlalchemy import Column, Integer, ForeignKey, Boolean, String
from sqlalchemy.orm import relationship

from app.models.base import Base, db


class Gift(Base):
    id = Column(Integer, primary_key=True)
    user = relationship('User')
    uid = Column(Integer, ForeignKey('user.id'))
    isbn = Column(String(15), nullable=False)
    # book = relationship('Book')
    # bid = Column(Integer, ForeignKey('book.id'))
    launched = Column(Boolean, default=False)

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