import requests
import redis
from functools import wraps
from typing import Callable
import time

# Initialize Redis connection
redis_client = redis.Redis(host='localhost', port=6379, db=0)

def cache_with_expiry(expiry_time: int = 10) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(url: str) -> str:
            # Create cache key for the URL
            cache_key = f"cache:{url}"
            count_key = f"count:{url}"
            
            # Increment the access counter for this URL
            redis_client.incr(count_key)
            
            # Try to get cached content
            cached_content = redis_client.get(cache_key)
            if cached_content:
                return cached_content.decode('utf-8')
            
            # If not cached, call the original function
            content = func(url)
            
            # Cache the result with expiration
            redis_client.setex(cache_key, expiry_time, content)
            
            return content
        return wrapper
    return decorator

@cache_with_expiry(10)
def get_page(url: str) -> str:
    """
    Fetches the HTML content of a given URL with caching and access tracking.
    
    Args:
        url (str): The URL to fetch content from
        
    Returns:
        str: The HTML content of the page
    """
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for bad status codes
    return response.text

# Example usage and testing
if __name__ == "__main__":
    # Test URL (slow response)
    test_url = "http://slowwly.robertomurray.co.uk/delay/3000/url/http://www.google.com"
    
    # Test the function
    try:
        # First request (should be slow)
        print("First request...")
        start_time = time.time()
        content = get_page(test_url)
        print(f"Time taken: {time.time() - start_time:.2f} seconds")
        
        # Second request (should be fast, from cache)
        print("\nSecond request...")
        start_time = time.time()
        content = get_page(test_url)
        print(f"Time taken: {time.time() - start_time:.2f} seconds")
        
        # Print access count
        count = redis_client.get(f"count:{test_url}")
        print(f"\nURL accessed {count.decode('utf-8')} times")
        
        # Wait for cache to expire
        print("\nWaiting for cache to expire (11 seconds)...")
        time.sleep(11)
        
        # Third request (should be slow again)
        print("\nThird request (after cache expiration)...")
        start_time = time.time()
        content = get_page(test_url)
        print(f"Time taken: {time.time() - start_time:.2f} seconds")
        
    except requests.RequestException as e:
        print(f"Error fetching URL: {e}")
    except redis.RedisError as e:
        print(f"Redis error: {e}")
