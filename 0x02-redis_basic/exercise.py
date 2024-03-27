#!/usr/bin/env python3
"""
exercise.py
"""
import redis
import uuid
from typing import Union, Callable
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    Decorator to count method calls
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ increments the count """
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Decorator to store input and output history of a function
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Create input and output list keys
        """
        input_key = "{}:inputs".format(method.__qualname__)
        output_key = "{}:outputs".format(method.__qualname__)
        self._redis.rpush(input_key, str(args))
        result = method(self, *args, **kwargs)
        self._redis.rpush(output_key, str(result))

        return result

    return wrapper


def replay(method: Callable) -> None:
    """
    Display the history of calls of a particular function.
    Retrieve input and output list keys
    """
    cache_instance = getattr(method.__self__, '_redis', None)

    input_key = "{}:inputs".format(method.__qualname__)
    output_key = "{}:outputs".format(method.__qualname__)

    inputs = cache_instance.lrange(input_key, 0, -1)
    outputs = cache_instance.lrange(output_key, 0, -1)

    print(f"{method.__qualname__} was called {len(inputs)} times:")
    for input_args, output in zip(inputs, outputs):
        print(f"{method.__qualname__}(*{eval(input_args)}) -> {output}")


class Cache:
    """
    Create a Cache class
    """
    def __init__(self) -> None:
        """
        Initialize Redis client and flush the database
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Generate a random key using uuid
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(
            self,
            key: str,
            fn: Callable = None
            ) -> Union[str, bytes, int, float]:
        """
        Get data from Redis
        """
        data = self._redis.get(key)

        if data is None:
            return None

        return fn(data) if fn else data

    def get_str(self, key: str) -> Union[str, None]:
        """
        Helper method for getting a string from cache
        """
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Union[int, None]:
        """
        Helper method for getting a integer from cache
        """
        return self.get(key, fn=int)
