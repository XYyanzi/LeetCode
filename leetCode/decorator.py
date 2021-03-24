'''
#-*- coding: utf-8 -*-
@Author: xunyan
@Time: 2020/12/31 1:09 下午
@File: decorator.py
'''
import logging


def use_logging(func):

    def wrapper(*args, **kwargs):
        logging.warning("%s is running" % func.__name__)
        return func()   # 把 foo 当做参数传递进来时，执行func()就相当于执行foo()
    return wrapper


@use_logging
def foo():
    print('i am foo')

# foo = use_logging(foo)  # 因为装饰器 use_logging(foo) 返回的时函数对象 wrapper，这条语句相当于  foo = wrapper
foo()                   # 执行foo()就相当于执行 wrapper()