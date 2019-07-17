from flask import flash, redirect, url_for, render_template, request
from flask_login import login_required, current_user
from sqlalchemy import or_, desc

from app.forms.book import DriftForm
from app.libs.email import send_email
from app.libs.enums import PendingStatus
from app.models.base import db
from app.models.drift import Drift
from app.models.gift import Gift
from app.models.user import User
from app.models.wish import Wish
from app.view_models.drift import DriftCollection
from . import web

__author__ = '七月'


@web.route('/drift/<int:gid>', methods=['GET', 'POST'])
@login_required
def send_drift(gid):
    current_gift = Gift.query.get_or_404(gid)

    if current_gift.is_your_own_book(current_user.id):
        flash('这本书是你自己的...')
        return redirect(url_for('web.book_detail', isbn=current_gift.isbn))

    has_given_enough_books = current_user.can_send_drift()
    if not has_given_enough_books:
        flash('鱼豆不足或者你需要送出一本书！')
        return render_template('not_enough_beans.html', beans=current_user.beans)

    form = DriftForm(request.form)
    if request.method == 'POST' and form.validate():
        save_drift(form, current_gift)
        send_email(current_gift.user.email, '有人想要一本书', 'email/get_gift.html',
                   wisher=current_user,
                   gift=current_gift)
        return redirect(url_for('web.pending'))
    return render_template('drift.html',
                           gifter=current_gift.user.summary,
                           user_beans=current_user.beans,
                           form=form)


@web.route('/pending')
@login_required
def pending():
    drifts = Drift.query.filter(
        or_(Drift.taker_id == current_user.id, Drift.giver_id == current_user.id)).order_by(
        desc(Drift.create_time)).all()

    views = DriftCollection(drifts, current_user.id)
    return render_template('pending.html', drifts=views.data)


@web.route('/drift/<int:drift_id>/reject')
@login_required
def reject_drift(drift_id):
    with db.auto_commit():
        drift = Drift.query.filter(Gift.uid == current_user.id, Drift.id == drift_id).first_or_404()
        drift.pending = PendingStatus.Reject
        taker = User.query.get_or_404(drift.taker_id)
        taker.beans += 1
    return redirect(url_for('web.pending'))
    pass


@web.route('/drift/<int:drift_id>/redraw')
def redraw_drift(drift_id):
    with db.auto_commit():
        drift = Drift.query.filter_by(taker_id=current_user.id, id=drift_id).first_or_404()
        drift.pending = PendingStatus.Cancel
        current_user.beans += 1
    return redirect(url_for('web.pending'))
    pass


@web.route('/drift/<int:drift_id>/mailed')
def mailed_drift(drift_id):
    with db.auto_commit():
        # 防止超权操作，有可能用户会更改drift_id
        # 必须保证当前用户的id和drift记录id同时满足条件才可以
        drift = Drift.query.filter_by(giver_id=current_user.id, id=drift_id).first_or_404()
        drift.pending = PendingStatus.Success
        current_user.beans += 1  # 成功赠送书，增加一鱼豆

        # 改变赠送清单中记录的状态
        gift = Gift.query.filter_by(id=drift.gift_id).first_or_404()
        gift.launched = True

        # 改变心愿清单中记录的状态
        wish = Wish.query.filter_by(isbn=drift.isbn,
                             uid=drift.taker_id,
                             launched=False).first_or_404()
        wish.launched = True
        return redirect(url_for('web.pending'))


def save_drift(drift_form, current_gift):
    with db.auto_commit():
        drift = Drift()
        # 把表单中的信息复制到模型中
        # 必要条件是，模型中的字段名和表单中的字段名相同
        drift_form.populate_obj(drift)

        drift.gift_id = current_gift.id
        drift.taker_id = current_user.id
        drift.taker_nickname = current_user.nickname
        drift.giver_id = current_gift.user.id
        drift.giver_nickname = current_gift.user.nickname

        book = current_gift.book

        drift.book_title = book['title']
        drift.book_author = book['author']
        drift.book_img = book['image']
        drift.isbn = book['isbn']

        current_user.beans -= 1

        db.session.add(drift)
