#!/usr/bin/env python3
""" Redis module"""

import redis
import uuid


class Cache:
    """Cache redis class"""

    def __init__(self):
        """Initializes"""

        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data):
        """defines the store method"""

        key = str(uuid.uuid4())
        self._redis.mset({key: data})

        return key
