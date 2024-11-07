#!/usr/bin/env python3
""" Redis module"""

import redis

from uuid import uuid4
from typing import Optional, Callable, Union

class Cache:
    """Cache redis class"""

    def __init__(self):
        """Initializes"""

        self._redis = redis.Redis()
        self._redis.flushdb()

    def get(self, key: str, fn: Optional[callable] = None) -> Union[str, None]:
        """Take a string argument and optional argument"""

        if fn:
            return fn(self._redis.get(key))
        data = self._redis.get(key)

        return data

    def store(self, data):
        """defines the store method"""

        key = str(uuid4())
        self._redis.mset({key: data})

        return key
