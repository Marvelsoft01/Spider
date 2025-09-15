# ============================================================
# config.py
# ------------------------------------------------------------
# This file defines the configuration settings for Spider.
# It allows users (and the CLI) to adjust runtime behavior
# such as number of threads, maximum crawl depth, timeouts,
# retries, storage format, and the User-Agent string.
#
# By centralizing settings here, we avoid hardcoding values
# in multiple files, making Spider easier to configure and
# extend in the future.
# ============================================================

# Default number of worker threads for concurrent crawling
NUM_THREADS = 5  # controls how many pages are fetched in parallel

# Maximum number of pages to crawl before stopping
MAX_PAGES = 100  # ensures the crawler does not run indefinitely

# Maximum crawl depth (distance from seed URLs)
MAX_DEPTH = 2  # prevents crawling from going too deep into the web

# Timeout (in seconds) for each HTTP request
REQUEST_TIMEOUT = 5  # ensures fetcher does not hang forever

# Number of retry attempts for failed HTTP requests
REQUEST_RETRIES = 2  # retries help recover from temporary errors

# Delay (in seconds) between retries after a failure
RETRY_DELAY = 1.0  # avoids hammering the same server repeatedly

# User-Agent string to identify the crawler to web servers
USER_AGENT = "Spider/0.1 (https://github.com/marvelspft01/spider)"

# Storage format for output data
OUTPUT_FORMAT = "json"  # can be "json" or "csv"

# Output directory for storing results
OUTPUT_DIR = "output"  # all saved files will be written here
