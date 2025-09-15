# ================================================================
# fetcher.py
#
# This module handles the low-level task of fetching web pages.
# It sends HTTP requests to URLs, applies headers like User-Agent,
# retries failed requests, respects timeouts, and only returns HTML
# pages (ignores non-HTML responses like images or PDFs).
#
# In short: this is the "downloader" part of the web crawler.
# ================================================================

# Import the urllib.request module for making HTTP requests
import urllib.request

# Import urllib.error to handle specific errors like HTTPError or URLError
import urllib.error

# Import time so we can pause (sleep) between retry attempts
import time

# Import Optional for type hinting: function may return a string or None
from typing import Optional


def fetch_url(url: str, timeout: int = 5, retries: int = 2, delay: float = 1.0) -> Optional[str]:
    """
    Fetch the content of a URL using urllib from Python's standard library.

    Args:
        url (str): The target URL to fetch.
        timeout (int): Timeout in seconds for the request.
        retries (int): Number of retry attempts on failure.
        delay (float): Delay (in seconds) between retries.

    Returns:
        Optional[str]: The HTML content of the page, or None if fetching failed.
    """
    # Keep track of how many attempts we've made
    attempt = 0

    # Keep trying until we've reached the allowed number of retries
    while attempt <= retries:
        try:
            # Create a request object with a custom User-Agent
            # This makes our crawler look "polite" and identifiable to servers
            req = urllib.request.Request(
                url,
                headers={
                    "User-Agent": "Spider/0.1 (https://github.com/marvelspft01/spider)"
                },
            )

            # Open the URL with the specified timeout
            with urllib.request.urlopen(req, timeout=timeout) as response:

                # Check the "Content-Type" header to ensure it's HTML
                if "text/html" in response.headers.get("Content-Type", ""):
                    # If it's HTML, decode the bytes into a string (UTF-8)
                    return response.read().decode("utf-8", errors="ignore")
                else:
                    # If it's not HTML (e.g., image, PDF), ignore and return None
                    return None

        # Handle common network errors like 404, 500, or connection issues
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as e:
            # Print a simple error message with retry attempt info
            print(
                f"[FetchError] {url} ({e}) - attempt {attempt+1}/{retries+1}")
            # Wait before retrying
            time.sleep(delay)
            # Increase attempt counter
            attempt += 1

        # Handle any other unexpected errors
        except Exception as e:
            # Print the unexpected error and stop retrying
            print(f"[UnexpectedError] {url} ({e})")
            return None

    # If all retries fail, return None (signal that fetch failed)
    return None
