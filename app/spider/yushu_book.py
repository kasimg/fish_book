"""
Created by kasim on 2019/7/9 9:40
"""
from flask import current_app

from app.libs.my_http import HTTP


class YuShuBook:
    """
    用来获取数据的类
    """
    isbn_url = 'http://t.yushu.im/v2/book/isbn/{}'
    keyword_url = 'http://t.yushu.im/v2/book/search?q={}&count={}&start={}'

    """
        方法中没有用到self（实例对象），但是用到了类变量
        由于用cls能方便一点，所以用类方法
    """
    def __init__(self):
        self.__total = 0
        self.__books = []

    def __wrap_single(self, data):
        if data:
            self.__total = 1
            self.__books.append(data)

    def __wrap_collection(self, data):
        self.__total = data['total']
        self.__books = data['books']

    def search_by_isbn(self, isbn):
        url = self.isbn_url.format(isbn)  # 字符串的format方法
        result = HTTP.get(url)
        # result 是dict
        self.__wrap_single(result)

    def search_by_keyword(self, keyword, page=1):
        # current_app指代flask对象
        url = self.keyword_url.format(keyword, current_app.config['PER_PAGE'],
                                     self.calculate_start(page))
        result = HTTP.get(url)
        self.__wrap_collection(result)

    @property
    def record_dict(self):
        return {
            'total': self.__total,
            'books': self.__books
        }

    @property
    def only_book(self):
        return self.__books[0] if self.__total >= 1 else None

    @staticmethod
    def calculate_start(page):
        """
        计算开始取数据的位置
        :param page: 页码
        :return: 起始点
        """
        return (page - 1) * current_app.config['PER_PAGE']