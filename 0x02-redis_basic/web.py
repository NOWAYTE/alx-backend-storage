import requests
import time
from functools import wraps

# Cache dictionary to store the HTML content and timestamps for URLs
cache = {}
# Dictionary to track the count of accesses per URL
access_count = {}

# Cache decorator to handle caching and count tracking
def cache_decorator(func):
    """
    A decorator function that wraps around the core `get_page` function.
    Handles the caching of results and tracks the number of accesses for each URL.
    
    Parameters:
    func (function): The function being decorated, in this case, `get_page`.

    Returns:
    function: The wrapped version of `get_page` that handles caching and access counting.
    """
    @wraps(func)
    def wrapper(url: str):
        """
        This wrapper function manages caching and access counting.
        
        Parameters:
        url (str): The URL to be fetched.

        Returns:
        str: The HTML content of the URL.
        """
        # Check if URL is already cached and if cache is still valid (10 seconds expiration)
        if url in cache and (time.time() - cache[url]['timestamp'] < 10):
            # Increment access count for the URL
            access_count[url] += 1
            return cache[url]['content']
        
        # If not cached or expired, call the function to fetch the page
        content = func(url)
        
        # Cache the result with timestamp
        cache[url] = {'content': content, 'timestamp': time.time()}
        
        # Set the count to 1 if it's the first access
        if url not in access_count:
            access_count[url] = 1
        
        return content
    return wrapper

# The actual get_page function wrapped with the cache decorator
@cache_decorator
def get_page(url: str) -> str:
    """
    Fetches the HTML content of the specified URL.
    
    Parameters:
    url (str): The URL of the page to fetch.

    Returns:
    str: The HTML content of the page.
    """
    # Use requests to fetch the page content
    response = requests.get(url)
    return response.text

# Function to get the access count for a URL
def get_access_count(url: str) -> int:
    """
    Returns the number of times a URL has been accessed.
    
    Parameters:
    url (str): The URL whose access count is to be retrieved.

    Returns:
    int: The number of times the URL was accessed.
    """
    return access_count.get(url, 0)

# Testing with a slow URL to simulate caching
if __name__ == "__main__":
    url = "http://slowwly.robertomurray.co.uk/delay/5000/url/http://example.com"
    
    # Fetch the page twice with caching
    print(get_page(url))  # This will take time the first time
    time.sleep(1)
    print(get_page(url))  # This will return the cached result
    
    # Check how many times the URL was accessed
    print(f"Access count for {url}: {get_access_count(url)}")

