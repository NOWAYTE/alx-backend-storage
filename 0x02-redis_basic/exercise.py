#!/usr/bin/env python3
""" Redis module"""

import redis
from uuid import uuid4

class Cache:
    """Cache redis class"""

    def __init__(self):
        """Initializes"""

        self._redis = redis.Redis()
        self._redis.flushdb()

    def __get__(size):

    def store(self, data):
        """defines the store method"""

        key = str(uuid4())
        self._redis.mset({key: data})

        return key
