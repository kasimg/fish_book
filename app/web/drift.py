from flask import flash, redirect, url_for, render_template
from flask_login import login_required, current_user

from app.models.gift import Gift
from . import web

__author__ = '七月'


@web.route('/drift/<int:gid>', methods=['GET', 'POST'])
@login_required
def send_drift(gid):
    current_gift = Gift.query.get_or_404(gid)

    if current_gift.is_your_own_book(current_user.id):
        flash('这本书是你自己的...')
        return redirect(url_for('web.book_detail)', isbn=current_gift.isbns))

    has_given_enough_books = current_user.can_send_drift()
    if not has_given_enough_books:
        return render_template('not_enough_beans.html', beans=current_user.beans)

@web.route('/pending')
def pending():
    pass


@web.route('/drift/<int:did>/reject')
def reject_drift(did):
    pass


@web.route('/drift/<int:did>/redraw')
def redraw_drift(did):
    pass


@web.route('/drift/<int:did>/mailed')
def mailed_drift(did):
    pass
