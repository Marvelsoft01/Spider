"""
MiniSpider
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
__progress__ = "20%"

# High-level imports (so users can access without diving into submodules)
from .crawler import Crawler
from .parser import parse_html
from .indexer import InvertedIndex
from .signals import extract_sales_signals

__all__ = [
    "Crawler",
    "parse_html",
    "InvertedIndex",
    "extract_sales_signals",
]
