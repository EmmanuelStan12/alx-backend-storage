#!/usr/bin/env python3
"""Writing strings to Redis
"""
import redis
from typing import Union, Callable, Any
import uuid
from functools import wraps


def replay(fn: Callable) -> None:
    """Displays the call history of the cache class
    """
    if fn is None or not hasattr(fn, '__self__'):
        return
    store = getattr(fn.__self__, '_redis', None)
    if not isinstance(store, redis.Redis):
        return
    fn_name = fn.__qualname__
    inputs = "{}:inputs".format(fn_name)
    outputs = "{}:outputs".format(fn_name)
    count = 0
    if store.exists(fn_name) != 0:
        count = int(store.get(fn_name))

    print('{} was called {} times:'.format(fn_name, count))
    fn_inputs = store.lrange(inputs, 0, -1)
    fn_outputs = store.lrange(outputs, 0, -1)
    for input, output in zip(fn_inputs, fn_outputs):
        print('{}(*{}) -> {}'.format(
            fn_name,
            input.decode('utf-8'),
            output.decode('utf-8')))


def call_history(method: Callable) -> Callable:
    """Store the inputs and outputs of each function call
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        """Wrapper function that tracks the inputs and outputs of the method
        """
        inputs = "{}:inputs".format(method.__qualname__)
        outputs = "{}:outputs".format(method.__qualname__)

        self._redis.rpush(inputs, str(args))
        result = method(self, *args, **kwargs)
        self._redis.rpush(outputs, result)

        return result

    return wrapper


def count_calls(method: Callable) -> Callable:
    """Count the number of calls on a method
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        """Wrapper function that increments call count and calls the method
        """
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


class Cache:
    """Cache class for all redis utils
    """
    def __init__(self) -> None:
        """Initialize redis client
        """
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Generates a random key and saves the data
        """
        key: str = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(
            self,
            key: str,
            fn: Callable = None
    ) -> Union[str, bytes, int, float]:
        """Reading data from redis
        """
        data = self._redis.get(key)
        return fn(data) if fn is not None else data

    def get_int(self, key: str) -> int:
        """Retrieves an integer from redis store
        """
        return self.get(key, lambda x: int(x))

    def get_str(self, key: str) -> str:
        """Retrieves a string from redis store
        """
        return self.get(key, lambda x: x.decode('utf-8'))
