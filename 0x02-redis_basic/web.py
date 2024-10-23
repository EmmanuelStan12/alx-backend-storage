#!/usr/bin/env python3
"""Implementing an expiring web cache and tracker
"""
import requests
import redis
from functools import wraps
from typing import Callable


store = redis.Redis()
store.flushdb(True)


def count_calls(method: Callable) -> Callable:
    """Count the number of times a page was accessed
    """
    @wraps(method)
    def wrapper(*args, **kwargs):
        """Wraps the get how much times
        """
        if args is None or len(args) == 0:
            return None
        url = args[0]
        key = "count:{}".format(url)
        if store.exists(key) != 0:
            store.incr(key)
            result = store.get(f'result:{url}')
            return result.decode('utf-8')

        result = method(*args, **kwargs)
        store.set(f'count:{url}', 1)
        store.setex(f'result:{url}', 10, result)
        return result
    return wrapper


@count_calls
def get_page(url):
    """Returns a page by running get page
    """
    return requests.get(url).text
