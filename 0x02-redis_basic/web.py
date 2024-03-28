#!/usr/bin/env python3
"""
wep.py
"""
import requests
import redis
from functools import wraps


def cache_and_track(func):
    """
    A decorator that caches the HTML content of a URL and tracks the number of
    accesses for each URL.

    Args:
    func (callable): The function to be decorated.

    Returns:
    callable: The decorated function.
    """
    @wraps(func)
    def wrapper(url):
        """
        Wrapper function that handles caching and access counting for the
        provided function.

        Args:
        url (str): The URL whose HTML content is to be fetched.

        Returns:
        str: The HTML content of the URL.

        """
        # Initialize Redis connection
        r = redis.Redis()

        # Check if the URL content is already cached
        cached_content = r.get(url)
        if cached_content:
            return cached_content.decode('utf-8')

        # If not cached, fetch the content from the URL
        response = requests.get(url)
        content = response.text

        # Cache the content with expiration time of 10 seconds
        r.setex(url, 10, content)

        # Track the number of accesses for this URL
        r.incr(f"count:{url}")

        return content
    return wrapper


@cache_and_track
def get_page(url: str) -> str:
    """
    Fetches the HTML content of a URL.

    Args:
    url (str): The URL whose HTML content is to be fetched.

    Returns:
    str: The HTML content of the URL.

    """
    return requests.get(url).text


# Test the function
print(get_page('http://slowwly.robertomurray.co.uk'))
print(get_page('http://slowwly.robertomurray.co.uk'))
