"""
Spider
----------

A lightweight multithreaded web crawler and search indexer in pure Python.
Designed as a sales-driven insights engine for SEO, lead generation, and market research.

Modules:
    crawler.py   - orchestrates crawling loop and thread pool
    fetcher.py   - handles HTTP requests, retries, rate limiting
    parser.py    - HTML parsing, text + link extraction
    indexer.py   - inverted index and tokenization
    signals.py   - sales/lead signal extraction (keywords, contacts, CTAs)
    store.py     - save results to JSON/CSV
    config.py    - crawler and parsing configuration
    cli.py       - command line interface
"""

__version__ = "0.1.0"
__author__ = "A.Rahman Dayo"


# Import the Crawler class from crawler.py so users can access it directly
from .crawler import Crawler

# Import the fetch_url function from fetcher.py for direct URL fetching
from .fetcher import fetch_url

# Import the parse_html function from parser.py for HTML parsing
from .parser import parse_html

# Import the Indexer class (or functions) from indexer.py for search indexing
from .indexer import Indexer

# Import the signals module, which extracts sales/lead signals
from . import signals

# Import the store module, which handles saving results to JSON/CSV
from . import store

# Define the list of items that are exposed when "from mini_spider import *" is used
__all__ = ["Crawler", "fetch_url", "parse_html", "Indexer", "signals", "store"]
