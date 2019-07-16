"""
Created by kasim on 2019/7/16 16:56
"""
from math import floor

from app.libs.enums import PendingStatus
from sqlalchemy import Column, String, Integer, ForeignKey, SmallInteger
from sqlalchemy.orm import relationship
from app.models.base import Base
from app.models.gift import Gift


class Drift(Base):
    """
        一次具体的交易信息
    """
    __tablename__ = 'drift'

    def __init__(self):
        self.pending = PendingStatus.waiting
        super(Drift, self).__init__()

    id = Column(Integer, primary_key=True)

    # 邮寄信息
    recipient_name = Column(String(20), nullable=False)
    address = Column(String(100), nullable=False)
    message = Column(String(200))
    mobile = Column(String(20), nullable=False)

    # 书籍信息
    isbn = Column(String(13))
    book_title = Column(String(50))
    book_author = Column(String(30))
    book_img = Column(String(50))
    # requester_id = Column(Integer, ForeignKey('user.id'))
    # requester = relationship('User')

    # 请求者信息
    taker_id = Column(Integer)
    taker_nickname = Column(String(20))

    # 赠送者信息
    giver_id = Column(Integer)
    gift_id = Column(Integer)
    giver_nickname = Column(String(20))
    _pending = Column('pending', SmallInteger, default=1)
    # gift_id = Column(Integer, ForeignKey('gift.id'))
    # gift = relationship('Gift')

    @property
    def pending(self):
        return PendingStatus(self._pending)

    @pending.setter
    def pending(self, status):
        self._pending = status.value

    def can_send_drift(self):
        if self.beans < 1:
            return False
        given_count = Gift.query.filter_by(
            uid=self.id, launched=True).count()
        received_count = Drift.query.filter_by(
            taker_id=self.id, pending=PendingStatus.Success).count()

        return True if \
            floor(given_count / 2) <= floor(received_count)\
            else False