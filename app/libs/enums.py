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