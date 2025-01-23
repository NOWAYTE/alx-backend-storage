#!/usr/bin/env python3
""" expiring web cache module """

import redis
import requests
from typing import Callable
from functools import wraps

# Use a more explicit name for the Redis client to avoid shadowing the module
redis_client = redis.Redis()


def wrap_requests(fn: Callable) -> Callable:
    """ Decorator wrapper for caching web requests """

    @wraps(fn)
    def wrapper(url: str) -> str:
        """ Wrapper that implements caching and counting logic """
        try:
            # Increment the access counter for this URL
            redis_client.incr(f"count:{url}")

            # Try to get cached response
            cached_response = redis_client.get(f"cached:{url}")
            if cached_response:
                return cached_response.decode('utf-8')

            # If no cached response, make the request
            result = fn(url)

            # Cache the result with 10 seconds expiration
            redis_client.setex(f"cached:{url}", 10, result)

            return result

        except redis.RedisError as e:
            # If Redis fails, just make the request without caching
            return fn(url)

    return wrapper


@wrap_requests
def get_page(url: str) -> str:
    """Get page content from URL

    Args:
        url: URL to fetch

    Returns:
        str: Page content
    """
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for bad status codes
    return response.text
