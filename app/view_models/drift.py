"""
Created by kasim on 2019/7/17 10:16
"""
from flask_login import current_user

from app.libs.enums import PendingStatus


class DriftViewModel:

    def __init__(self, drift, current_user_id):
        self.data = {}
        self.data = self.__parse(drift, current_user_id)

    @staticmethod
    def taker_or_giver(drift, current_user_id):
        if drift.taker_id == current_user_id:
            return 'taker'
        return  'giver'


    def __parse(self, drift, current_user_id):
        you_are = self.taker_or_giver(drift, current_user_id)
        pending_status = PendingStatus.pending_str(drift.pending, you_are)

        r = {
            'drift_id': drift.id,
            'you_are': you_are,
            # 'book_title': drift.gift.book.title,
            # 'book_author': drift.gift.book.author_str,
            'book_title': drift.book_title,
            'book_author': drift.book_author,
            'book_img': drift.book_img,
            'operator': drift.taker_nickname if you_are != 'taker' \
                else drift.giver_nickname,
            'date': drift.create_datetime.strftime('%Y-%m-%d'),
            'message': drift.message,
            'address': drift.address,
            'recipient_name': drift.recipient_name,
            'mobile': drift.mobile,
            'status_str': pending_status,
            'status': drift.pending
        }
        return r

class DriftCollection:
    def __init__(self, drifts, current_user_id):
        self.data = []

        self.__parse(drifts, current_user_id)

    def __parse(self, drifts, current_user_id):
        for drift in drifts:
            temp = DriftViewModel(drift, current_user_id)
            self.data.append(temp.data)