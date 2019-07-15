"""
Created by kasim on 2019/7/10 9:58
"""
class MyResource():
    # def __enter__(self):
    #     print('connect')
    #     return self
    #
    # def __exit__(self, exe_type, exe_value, tb):
    #     """
    #     释放资源时进行的操作
    #     :param exe_type: 错误类型
    #     :param exe_value: 错误信息
    #     :param tb: 错误堆栈信息
    #     :return: 是否已处理异常，True表示已经处理，False表示未处理
    #     """
    #     if tb:
    #         print('process exception')
    #     else:
    #         print('no exception')
    #     print('close resource connection')

    def query(self):
        print('query data')

try:
    with MyResource() as resource:
        a = 1 / 0
        resource.query()
except Exception as ex:
    pass


from contextlib import contextmanager

@contextmanager
def make_myresource():
    print('connect to resource') #  这里是__enter__函数中的操作
    yield MyResource() #  这里是__enter__函数中的返回值
    print('close resource connection') #  这里是__exit__函数中的操作

with make_myresource() as r:
    r.query()