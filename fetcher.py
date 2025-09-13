import urllib.request
import urllib.error
import time
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
    attempt = 0
    while attempt <= retries:
        try:
            req = urllib.request.Request(
                url,
                headers={
                    "User-Agent": "Spider/0.1 (https://github.com/marvelspft01/spider)"
                },
            )
            with urllib.request.urlopen(req, timeout=timeout) as response:
                if "text/html" in response.headers.get("Content-Type", ""):
                    return response.read().decode("utf-8", errors="ignore")
                else:
                    return None

        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as e:
            # Basic logging for now
            print(f"[FetchError] {url} ({e}) - attempt {attempt+1}/{retries+1}")
            time.sleep(delay)
            attempt += 1
        except Exception as e:
            print(f"[UnexpectedError] {url} ({e})")
            return None

    return None
