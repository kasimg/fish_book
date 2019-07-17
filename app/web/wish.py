from flask import current_app, flash, redirect, url_for, render_template
from flask_login import login_required, current_user

from app.libs.email import send_email
from app.models.base import db
from app.models.gift import Gift
from app.models.wish import Wish
from app.view_models.trade import MyTrades
# from app.view_models.wish import MyWishes
from . import web

__author__ = '七月'


@web.route('/my/wish')
@login_required
def my_wish():
    uid = current_user.id
    wishes = Wish.get_user_wishes(uid)
    isbn_list = [wish.isbn for wish in wishes]
    gift_count_list = Wish.get_gift_counts(isbn_list)
    view_model = MyTrades(wishes, gift_count_list)
    return render_template('my_wish.html', wishes=view_model.trades)


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
    """
        向想要这本书的人发送一封邮件
        注意，这个接口需要做一定的频率限制
        这接口比较适合写成一个ajax接口
    """
    wish = Wish.query.get_or_404(wid)
    gift = Gift.query.filter_by(uid=current_user.id, isbn=wish.isbn).first()
    if not gift:
        flash('你还没有上传此书，请点击“加入到赠送清单”添加此书。添加前，请确保自己可以赠送此书')
    else:
        send_email(wish.user.email, '有人想送你一本书', 'email/satisfy_wish.html', wish=wish,
                   gift=gift)
        flash('已向他/她发送了一封邮件，如果他/她愿意接受你的赠送，你将收到一个鱼漂')
    return redirect(url_for('web.book_detail', isbn=wish.isbn))


@web.route('/wish/book/<isbn>/redraw')
@login_required
def redraw_from_wish(isbn):
    # 心愿对象不存在于drift模型中，所以不需关联drift操作
    wish = Wish.query.filter_by(isbn=isbn, launched=False).first_or_404()
    with db.auto_commit():
        wish.delete()
    return redirect(url_for('web.my_wish'))
