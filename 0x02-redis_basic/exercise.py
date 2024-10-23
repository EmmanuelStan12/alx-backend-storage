#!/usr/bin/env python3
"""Writing strings to Redis
"""
import redis
from typing import Union
import uuid


class Cache:
    """Cache class for all redis utils
    """
    def __init__(self) -> None:
        """Initialize redis client
        """
        self._redis = redis.Redis()
        self._redis.flushdb(True)


    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Generates a random key and saves the data
        """
        key: str = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
