"""
Created by kasim on 2019/7/15 16:17
"""
from app.view_models.book import BookViewModel


class TradeInfo:
    def __init__(self, goods):
        self.total = 0
        self.trades = [] #  存放具体信息
        self.__parse(goods)

    def __parse(self, goods):
        self.total = len(goods)
        self.trades = [self.__map_to_trade(single) for single in goods]

    def __map_to_trade(self, single):
        if single.create_datetime:
            time = single.create_datetime.strftime('%Y-%m-%d')
        else:
            time = '未知'
        return dict(
            user_name=single.user.nickname,
            time=time,
            id=single.id
        )

class MyTrade:
    id = 0
    book = None
    trade_count = 0

    def __init__(self, id, book, trade_count):
        self.id = id
        self.book = book
        self.trade_count = trade_count


class MyTrades:
    def __init__(self, trades, trade_count_list):
        # self.trades = []

        self.__trades = trades
        self.__trade_count_list = trade_count_list

        self.trades = self.__parse()

    def __parse(self):
        # 不建议在方法中直接改变实例属性，而是要把结果返回回去
        # 否则如果函数很多的话，容易不知道属性在哪个函数中被改变
        temp_trades = []
        for trade in self.__trades:  # 遍历每一本要送出的书，看看有没有人想要
            my_trade = self.__matching(trade)
            temp_trades.append(my_trade)
        return temp_trades

    def __matching(self, trade):
        count = 0
        for trade_count in self.__trade_count_list:  # 遍历心愿清单，查看要送出的书是否有人想要
            if trade.isbn == trade_count['isbn']:  # 如果书的isbn编号在心愿清单中，那么表示有人想要这本书
                count = trade_count['count']  # 把要这本书的人数取出来
        r = dict(
            trades_count=count,
            book=BookViewModel(trade.book),
            id=trade.id
        )
        return r
        # my_gift = MyGift(gift.id, BookViewModel(gift.book), count)  # 实例化礼物视图莫兴国
        # return my_gift
