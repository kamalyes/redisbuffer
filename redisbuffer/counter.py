# -*- coding:utf-8 -*-
# !/usr/bin/env python 3.9.11
"""
@File    :  counter.py
@Time    :  2021/5/21 20:16
@Author  :  YuYanQing
@Version :  1.0
@Contact :  mryu168@163.com
@License :  (C)Copyright 2022-2026
@Desc    :  基於Redis的計數器工具
"""
from abc import ABCMeta, abstractmethod
from typing import Callable, Optional

from redis import Redis


class Counter(metaclass=ABCMeta):
    def __init__(self, redis: Redis, resource: str, step: int):
        self._redis = redis
        self._step = step
        self._resource = resource

    redis = property(lambda self: self._redis)
    step = property(lambda self: self._step)
    resource = property(lambda self: self._resource)

    @abstractmethod
    def get(self):
        raise NotImplementedError()


class RedCounter(Counter):
    def __init__(self, redis: Redis, resource: str, step: int, init: Optional[Callable[[], int]] = None):
        super().__init__(redis, resource, step)
        self._amount = abs(step)
        self._getter = self.decr if step < 0 else self.incr
        if init:
            redis.set(resource, init())

    value = property(lambda self: int(self._redis.get(self._resource)) or 0)

    def get(self):
        return self._getter()

    def incr(self):
        return self._redis.incrby(self._resource, self._amount)

    def decr(self):
        return self._redis.decrby(self._resource, self._amount)

    def __get__(self, instance, owner):
        if not instance:
            return self
        return self.value


class HashCounter(Counter):
    def __init__(self, redis: Redis, resource: str, key: str, step: int, init: Optional[Callable[[], int]] = None):
        super().__init__(redis, resource, step)
        self._key = key
        if init:
            redis.hset(resource, key, init())

    key = property(lambda self: self._key)
    value = property(lambda self: int(self._redis.hget(self.resource, self._key)) or 0)

    def get(self):
        return self._redis.hincrby(self.resource, self.key, self.step)

    def __get__(self, instance, owner):
        if not instance:
            return self
        return self.get()
