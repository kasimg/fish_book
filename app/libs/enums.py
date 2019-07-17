"""
Created by kasim on 2019/7/16 17:12
"""
from enum import Enum


class PendingStatus(Enum):
    """四种交易状态"""
    Waiting = 1
    Success = 2
    Reject = 3
    Cancel = 4

    @classmethod
    def pending_str(cls, status, key):
        key_map = {
            cls.Waiting: {
                'taker': '等待对方邮寄',
                'giver': '等待你邮寄'
            },
            cls.Reject: {
                'taker': '对方已拒绝',
                'giver': '你已拒绝'
            },
            cls.Cancel: {
                'taker': '你已撤销',
                'giver': '对方已撤销'
            },
            cls.Success: {
                'taker': '对方已邮寄',
                'giver': '你已邮寄，交易完成'
            }
        }
        return key_map[status][key]
