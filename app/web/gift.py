from flask import current_app, flash, redirect, url_for, render_template
from flask_login import login_required, current_user

from app.libs.enums import PendingStatus
from app.models.base import db
from app.models.drift import Drift
from app.models.gift import Gift
# from app.view_models.gift import MyGifts
from app.view_models.trade import MyTrades
from . import web
__author__ = '七月'


@web.route('/my/gifts')
@login_required
def my_gifts():
    uid = current_user.id
    gifts = Gift.get_user_gifts(uid)
    isbn_list = [gift.isbn for gift in gifts]
    wish_count_list = Gift.get_wish_counts(isbn_list)
    # Gift.get_wish_counts(isbn_list)
    view_model = MyTrades(gifts, wish_count_list)
    return render_template('my_gifts.html', gifts=view_model.trades)


@web.route('/gifts/book/<isbn>')
@login_required
def save_to_gifts(isbn):
    if current_user.can_save_to_list(isbn):
        with db.auto_commit():

            gift = Gift()
            gift.isbn = isbn
            gift.uid = current_user.id #  current_user就是一个user模型，可理解为user类的实例化对象

            current_user.beans += current_app.config['BEANS_UPLOAD_ONE_BOOK'] #  增加鱼豆
            db.session.add(gift)
            # db.session.commit()
    else:
        flash('这本书已经添加至你的赠送清单或存在于你的心愿清单，请不要重复添加')
    return redirect(url_for('web.book_detail', isbn=isbn)) #  isbn为视图函数需要的参数

@web.route('/gifts/<gid>/redraw')
@login_required
def redraw_from_gifts(gid):
    # gift_id记录存在鱼漂模型中，drift模型需要用到gift_id
    gift = Gift.query.filter_by(id=gid, launched=False).first_or_404()
    drift = Drift.query.filter_by(gift_id=gid, pending=PendingStatus.Waiting).first()
    if drift:
        flash('这个礼物正处于交易状态，请先前往鱼漂完成该交易！')
    else:
        with db.auto_commit():
            current_user.beans -= current_app.config['BEANS_UPLOAD_ONE_BOOK']
            gift.delete()



