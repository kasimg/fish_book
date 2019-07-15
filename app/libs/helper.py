"""
Created by kasim on 2019/7/9 8:52
"""
def is_isbn_or_key(word):
    """
    判断查询参数是isbn码还是关键字
    :param word: 查询参数
    :return: 查询参数的类型
    """
    isbn_or_key = 'key'
    if len(word) == 13 and word.isdigit():
        isbn_or_key = 'isbn'
    short_word = word.replace('-', '')
    if '-' in short_word and len(short_word) == 10 and short_word.isdigit:
        isbn_or_key = 'isbn'
    return isbn_or_key