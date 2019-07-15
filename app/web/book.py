"""
Created by kasim on 2019/7/9 10:32
"""
# 视图函数
# 返回response对象（包含status code、content-type等内容）
import json

from flask import jsonify, request, render_template, url_for, flash
from app.forms.book import SearchForm

from . import web
from app.libs.helper import is_isbn_or_key
from app.spider.yushu_book import YuShuBook
from app.view_models.book import BookViewModel, BookCollenction

@web.route('/book/<isbn>/detail') #  没有斜杠开头会报错
def book_detail(isbn):
    yushu_book = YuShuBook()
    yushu_book.search_by_isbn(isbn)
    book = BookViewModel(yushu_book.only_book)
    return render_template('book_detail.html', book=book, wishes=[], gifts=[])

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

