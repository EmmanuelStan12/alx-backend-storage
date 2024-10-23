#!/usr/bin/env python3
"""Implementing an expiring web cache and tracker
"""
import requests
import redis
from functools import wraps
from typing import Callable


store = redis.Redis()


def count_calls(method: Callable) -> Callable:
    """Count the number of times a page was accessed
    """
    @wraps(method)
    def wrapper(url):
        """Wraps the get how much times
        """
        store.incr(f'count:{url}')
        result = store.get(f'result:{url}')
        if result:
            return result.decode('utf-8')

        result = method(url)
        store.setex(f'result:{url}', 10, result)
        return result

    return wrapper


@count_calls
def get_page(url: str) -> str:
    """Returns a page by running get page
    """
    return requests.get(url).text
