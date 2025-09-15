# ============================================================
# cli.py
# ------------------------------------------------------------
# This file is the command-line interface (CLI) entrypoint for Spider.
#
# Responsibilities:
#   - Read configuration from config.py
#   - Load seed URLs (from examples/seed_urls.txt or user-provided file)
#   - Construct and run the Crawler
#   - Collect parsed documents
#   - Pass results to the Indexer and Signals modules
#   - Save final outputs using the Store module
#
# This file "ties everything together" so that Spider can be
# run as a standalone tool directly from the terminal.
# ============================================================

import argparse  # built-in module for parsing command-line arguments
import os        # used for file path handling
import sys       # used for exiting the program if errors occur

# Import local modules from the Spider package
from . import config                # load configuration defaults
from .crawler import Crawler        # main crawling engine
from .indexer import Indexer        # build inverted index
from .signals import extract_signals  # detect sales/lead signals
from .store import save_results     # save data to JSON or CSV


def load_seed_urls(seed_file: str) -> list:
    """
    Load seed URLs from a given text file.
    Each line in the file is expected to contain one URL.
    """
    # Check if file exists before reading
    if not os.path.exists(seed_file):
        print(f"[Error] Seed file not found: {seed_file}")
        sys.exit(1)  # exit program with error code

    # Open file and read all lines, stripping whitespace
    with open(seed_file, "r", encoding="utf-8") as f:
        urls = [line.strip() for line in f if line.strip()]

    return urls  # return list of URLs


def main():
    """
    Main function for running Spider from the command line.
    """
    # Set up argument parser to allow user overrides
    parser = argparse.ArgumentParser(
        description="Spider - Sales-driven web crawler")
    parser.add_argument("--seeds", default="examples/seed_urls.txt",
                        help="Path to seed URLs file (default: examples/seed_urls.txt)")
    parser.add_argument("--max-pages", type=int, default=config.MAX_PAGES,
                        help="Maximum number of pages to crawl")
    parser.add_argument("--threads", type=int, default=config.NUM_THREADS,
                        help="Number of concurrent threads")
    parser.add_argument("--format", choices=["json", "csv"], default=config.OUTPUT_FORMAT,
                        help="Output format for results (json or csv)")
    parser.add_argument("--output-dir", default=config.OUTPUT_DIR,
                        help="Directory where results will be saved")
    args = parser.parse_args()

    # Load the seed URLs (starting points for the crawler)
    seed_urls = load_seed_urls(args.seeds)

    # Construct the crawler with user-specified or default settings
    crawler = Crawler(seed_urls=seed_urls,
                      max_pages=args.max_pages,
                      num_threads=args.threads)

    # Run the crawler and collect documents
    print("[Spider] Starting crawl...")
    documents = crawler.run()
    print(f"[Spider] Crawling complete. {len(documents)} documents collected.")

    # Build the inverted index for keyword search
    indexer = Indexer()
    indexer.build_index(documents)
    print(f"[Spider] Index built with {len(indexer.index)} unique terms.")

    # Extract sales/lead signals from the crawled documents
    signals = []
    for doc in documents:
        found = extract_signals(doc.get("text", ""))
        if found:
            signals.append({"url": doc["url"], "signals": found})
    print(f"[Spider] Signals extracted from {len(signals)} documents.")

    # Save results (documents, index, and signals)
    save_results(documents, signals, args.format, args.output_dir)
    print(
        f"[Spider] Results saved to {args.output_dir}/ in {args.format} format.")


# Standard Python entrypoint check
if __name__ == "__main__":
    main()
