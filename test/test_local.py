"""
Created by kasim on 2019/7/10 15:57
"""
from werkzeug.local import Local, LocalStack
import threading

my_stack = LocalStack()

my_stack.push(1)

print(my_stack.top)

def thread():
    my_stack.push(2)
    print(my_stack.top)

my_thread = threading.Thread(target=thread)
my_thread.start()

# my_stack.push(100)