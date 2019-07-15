"""
Created by kasim on 2019/7/9 10:32
"""
# 视图函数
# 返回response对象（包含status code、content-type等内容）
import json

from flask import jsonify, request, render_template, url_for, flash
from flask_login import current_user

from app.forms.book import SearchForm
from app.models.gift import Gift
from app.models.wish import Wish
from app.view_models.trade import TradeInfo

from . import web
from app.libs.helper import is_isbn_or_key
from app.spider.yushu_book import YuShuBook
from app.view_models.book import BookViewModel, BookCollenction


@web.route('/book/<isbn>/detail')  # 没有斜杠开头会报错
def book_detail(isbn):
    # 判断用户是否在这本书的心愿清单、赠送清单中的标识
    in_gift_list = False
    in_wish_list = False

    yushu_book = YuShuBook()
    yushu_book.search_by_isbn(isbn)
    book = BookViewModel(yushu_book.only_book)

    if current_user.is_authenticated: #  如果用户已经登录
        if Gift.query.filter_by(uid=current_user.id, isbn=isbn,
                                launched=False).first(): #  如果赠送列表中有记录，说明这个用户要送出这本书
            in_gift_list = True
        if Wish.query.filter_by(uid=current_user.id, isbn=isbn, #  说明用户想要这本书
                                launched=False).first():
            in_wish_list = True

    #  该书赠送列表中的所有记录
    gift_records = Gift.query.filter_by(isbn=isbn, launched=False).all()
    #  该书心愿列表中的所有记录
    wish_records = Wish.query.filter_by(isbn=isbn, launched=False).all()

    gift_models = TradeInfo(gift_records)
    wish_models = TradeInfo(wish_records)
    return render_template('book_detail.html',
                           book=book, wishes=wish_models, gifts=gift_models,
                           in_wish_list=in_wish_list, in_gift_list=in_gift_list)


@web.route('/test')
def test1():
    # from flask import request
    # from app.libs.none_local import n
    # print(n.v)
    # n.v = 2
    # print('-----------------------------')
    # print(getattr(request, 'v', None))
    # setattr(request, 'v', 2)
    # print('-----------------------------')
    # return ''
    r = {
        'name': 'kasim',
        'age': 18
    }
    # url_for()
    flash('hello, kasim')
    return render_template('test.html', data=r)


@web.route('/book/search')
def search():
    """
        :param q: 关键字，可以是普通关键字或者ISBN码
        :param page: 分页相关参数
        :return:
    """
    # a = request.args.to_dict()  把不可变字典转化成可变字典

    form = SearchForm(request.args)  # 类中找不到__init__函数，则会去父类中找
    books = BookCollenction()

    if form.validate():  # 根据验证规则进行验证
        q = form.q.data.strip()  # 取出查询参数并去掉空格
        page = form.page.data  # 取出页码参数
        isbn_or_key = is_isbn_or_key(q)
        yushu_book = YuShuBook()

        if isbn_or_key == 'isbn':
            yushu_book.search_by_isbn(q)
        else:
            yushu_book.search_by_keyword(q, page)

        books.wrap_collection(yushu_book.record_dict, q)
        # return json.dumps(books, default=lambda o: getattr(o, '__dict__', None))  # return的是ViewModel

    else:
        flash('搜索的关键字不符合要求，请重新输入')
        # return jsonify(form.errors)

    return render_template('search_result.html', books=books)
