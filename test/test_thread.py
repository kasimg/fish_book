"""
Created by kasim on 2019/7/10 14:51
"""
import threading
import time


def worker():
    print('I am thread')
    t = threading.current_thread()
    time.sleep(8)
    print(t.getName())

new_t = threading.Thread(target=worker, name='kasim')
new_t.start()

t = threading.current_thread()
print(t.getName())