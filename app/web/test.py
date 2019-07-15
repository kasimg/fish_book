"""
Created by kasim on 2019/7/12 12:00
"""
from flask import make_response

from app.web import web


@web.route('/set/cookie')
def set_cookie():
    response = make_response('kasim')
    response.set_cookie('name', 'kasim', 100)
    return response