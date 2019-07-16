"""
Created by kasim on 2019/7/12 9:11
"""
from sqlalchemy import Column, Integer, ForeignKey, Boolean, String, desc, func
from sqlalchemy.orm import relationship

from app.models.base import Base, db



class Wish(Base):
    id = Column(Integer, primary_key=True)
    user = relationship('User')
    uid = Column(Integer, ForeignKey('user.id'))
    isbn = Column(String(15), nullable=False)
    # book = relationship('Book')
    # bid = Column(Integer, ForeignKey('book.id'))
    launched = Column(Boolean, default=False)

    @classmethod
    def get_user_wishes(cls, uid):
        """
        获取心愿清单中该用户的记录
        :param uid:
        :return:
        """
        wishes = Wish.query.filter_by(uid=uid, launched=False).order_by(
            desc(Wish.create_time)).all()

        return wishes

    @classmethod
    def get_gift_counts(cls, isbn_list):
        """
        根据传入的一组isbn，到gift表中查询出都有哪些人要送这本书
        :return:
        """
        from app.models.gift import Gift
        # query后面跟的是对查询结果的操作，根据业务需求返回想要的数据
        count_list = db.session.query(Gift.isbn, func.count(Wish.id)).filter(
            Wish.launched == False,
            Wish.isbn.in_(isbn_list),
            Wish.status == 1).group_by(
            Wish.isbn).all()
        # [dict(isbn=record[0], count=record[1]) for record in count_list]
        return [dict(isbn=record[0], count=record[1]) for record in count_list]

# 此模块第一次被执行时，类对象被初始化，初始化过程只涉及类变量
# 只要类变量的定义过程中没有使用Gift，那么就可以把Gift的导入放到最后
# 之后，再调用要使用Wish的方法时，此模块已经执行完成，Gift已经被导入
# from app.models.gift import Gift