#!/usr/bin/env python3
""" Redis Module """

from functools import wraps
import redis
import requests
from typing import Callable

redis_ = redis.Redis()


def count_requests(method: Callable) -> Callable:
    """Decorator for counting requests and caching the result"""
    @wraps(method)
    def wrapper(url):  # sourcery skip: use-named-expression
        """Wrapper for decorator"""
        # Check if cached HTML exists
        cached_html = redis_.get(f"cached:{url}")
        if cached_html:
            redis_.incr(f"count:{url}")  # Increment request count when serving from cache
            return cached_html.decode('utf-8')
        
        # Fetch the page if not cached
        html = method(url)
        
        # Cache the result and set expiry time
        redis_.setex(f"cached:{url}", 10, html)
        
        # Increment the count for this URL
        redis_.incr(f"count:{url}")
        
        return html

    return wrapper


@count_requests
def get_page(url: str) -> str:
    """ Obtain the HTML content of a URL """
    req = requests.get(url)
    return req.text

