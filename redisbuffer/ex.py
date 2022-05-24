# -*- coding:utf-8 -*-
# !/usr/bin/env python 3.9.11
"""
@File    :  ex.py
@Time    :  2021/5/21 20:16
@Author  :  YuYanQing
@Version :  1.0
@Contact :  mryu168@163.com
@License :  (C)Copyright 2022-2026
@Desc    :
"""

from typing import Callable, Optional, Any


class LazyProperty(object):
    def __init__(self, getter: Callable, setter: Optional[Callable] = None):
        self._getter = getter
        self._setter = setter
        self._value: Optional[Any] = None

    def __get__(self, instance, owner):
        if not instance:
            return self
        if not self._value:
            self._value = self._getter(instance)
        return self._value

    def __set__(self, instance, value):
        if not instance:
            return value
        if self._setter:
            self._value = self._setter(instance, value)
        raise AttributeError("can't set attribute")
