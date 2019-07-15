"""
Created by kasim on 2019/7/11 8:40
"""
class BookViewModel:
    def __init__(self, book):
        # self.__cut_book_data(book)
        # self.title = ''
        # self.a = type(book['title'])
        setattr(self, 'title', book['title'])
        setattr(self, 'publisher', book['publisher'])
        setattr(self, 'pages', book['pages'])
        setattr(self, 'author', book['author'])
        setattr(self, 'price', book['price'])
        setattr(self, 'summary', book['summary'])
        setattr(self, 'image', book['image'])
        setattr(self, 'pubdate', book['pubdate'])
        setattr(self, 'binding', book['binding'])
        self.isbn = book['isbn']
        # self.title = book['title'],
        # self.publisher = book['publisher'],
        # self.pages = book['pages'] or '',
        # self.author = '、'.join(book['author']),
        # self.price = book['price'],
        # self.summary = book['summary'] or '',
        # self.image = book['image']

    # def __setattr__(self, key, value):
    #     setattr(self, key, value)
    # def __cut_book_data(self, book):
    #     self.title = book['title'],
    #     self.publisher = book['publisher'],
    #     self.pages = book['pages'] or '',
    #     self.author = '、'.join(book['author']),
    #     self.price = book['price'],
    #     self.summary = book['summary'] or '',
    #     self.image = book['image']
    @property
    def intro(self):
        intros = filter(lambda x: True if x else False,
                        [' '.join(self.author), self.publisher, self.price])
        return ' / '.join(intros)

class BookCollenction:
    """
    在这个类中将两种关键字查询的返回结果统一封装
    """
    def __init__(self):
        self.books = []
        self.total = 0
        self.keyword = ''
        # self.keyword = keyword

    def wrap_collection(self, records, keyword):
        self.keyword = keyword
        self.total = records['total']
        self.books = [BookViewModel(book) for book in records['books']]

    def get_collection(self):
        """
        获取书籍信息
        :return: 书籍信息
        """
        pass
class _BookViewModel:
    """
    把两种关键字的查询结果返回的数据包装成同一种数据结构，防止麻烦和不必要的错误
    """
    @classmethod
    def single_record(cls, origin_record, keyword):
        altered_record = {
            'books': [],
            'total': 0,
            'keyword': keyword
        }
        if origin_record:
            altered_record['total'] = 1
            altered_record['books'] = [cls.__cut_book_data(origin_record)]
        return altered_record

    @classmethod
    def multi_records(cls, origin_record, keyword):
        altered_record = {
            'books': [],
            'total': 0,
            'keyword': keyword
        }
        if origin_record:
            altered_record['total'] = origin_record['title']
            altered_record['books'] = [cls.__cut_book_data(book) for book in origin_record['books']]
        return altered_record

    @classmethod
    def __cut_book_data(cls, data):
        altered_data = {
            'title': data['title'],
            'publisher': data['publisher'],
            'pages': data['pages'] or '',
            'author': '、'.join(data['author']),
            'price': data['price'],
            'summary': data['summary'] or '',
            'image': data['image']
        }
        return altered_data