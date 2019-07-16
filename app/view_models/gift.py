"""
Created by kasim on 2019/7/16 9:59
"""
from collections import namedtuple

from app.view_models.book import BookViewModel


class MyGift:
    id = 0
    book = None
    wishes_count = 0

    def __init__(self, id, book, wishes_count):
        self.id = id
        self.book = book
        self.wishes_count = wishes_count


class MyGifts:
    def __init__(self, gifts, wish_count_list):
        self.gifts = []

        self.__gifts = gifts
        self.__wish_count_list = wish_count_list

        self.gifts = self.__parse()

    def __parse(self):
        # 不建议在方法中直接改变实例属性，而是要把结果返回回去
        # 否则如果函数很多的话，容易不知道属性在哪个函数中被改变
        temp_gifts = []
        for gift in self.__gifts:  # 遍历每一本要送出的书，看看有没有人想要
            my_gift = self.__matching(gift)
            temp_gifts.append(my_gift)
        return temp_gifts

    def __matching(self, gift):
        count = 0
        for wish_count in self.__wish_count_list:  # 遍历心愿清单，查看要送出的书是否有人想要
            if gift.isbn == wish_count['isbn']:  # 如果书的isbn编号在心愿清单中，那么表示有人想要这本书
                count = wish_count['count']  # 把要这本念书的人数取出来
        r = dict(
            wishes_count=count,
            book=BookViewModel(gift.book),
            id=gift.id
        )
        return r
        # my_gift = MyGift(gift.id, BookViewModel(gift.book), count)  # 实例化礼物视图莫兴国
        # return my_gift
