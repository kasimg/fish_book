from flask import current_app, flash, redirect, url_for
from flask_login import login_required, current_user

from app.models.base import db
from app.models.wish import Wish
from . import web

__author__ = '七月'


@web.route('/my/wish')
def my_wish():
    pass


@web.route('/wish/book/<isbn>')
@login_required
def save_to_wish(isbn):
    if current_user.can_save_to_list(isbn):
        with db.auto_commit():

            wish = Wish()
            wish.isbn = isbn
            wish.uid = current_user.id  # current_user就是一个user模型，可理解为user类的实例化对象
            # current_user.beans += current_usent_app.config['BEANS_UPLOAD_ONE_BOOK']  # 增加鱼豆
            db.session.add(wish)
            # db.session.commit()
    else:
        flash('这本书已经添加至你的心愿清单或存在于你的赠送清单，请不要重复添加')
    return redirect(url_for('web.book_detail', isbn=isbn))  # isbn为视图函数需要的参数


@web.route('/satisfy/wish/<int:wid>')
def satisfy_wish(wid):
    pass


@web.route('/wish/book/<isbn>/redraw')
def redraw_from_wish(isbn):
    pass
