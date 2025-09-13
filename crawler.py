import threading
import queue
from typing import List, Dict
from .fetcher import fetch_url
from .parser import parse_html


class Crawler:
    """
    Multithreaded web crawler.
    
    Responsibilities:
        - Manage crawl queue
        - Dispatch worker threads
        - Fetch pages using fetcher
        - Parse HTML using parser
        - Collect crawled documents for indexing
    """

    def __init__(self, seed_urls: List[str], max_pages: int = 100, num_threads: int = 5):
        self.seed_urls = seed_urls
        self.max_pages = max_pages
        self.num_threads = num_threads

        self.queue = queue.Queue()
        self.visited = set()
        self.results: List[Dict] = []

        # seed the queue
        for url in seed_urls:
            self.queue.put(url)

    def worker(self):
        """Worker thread: fetch and parse pages from the queue."""
        while not self.queue.empty() and len(self.results) < self.max_pages:
            try:
                url = self.queue.get_nowait()
            except queue.Empty:
                break

            if url in self.visited:
                continue

            self.visited.add(url)

            html = fetch_url(url)
            if not html:
                continue

            doc = parse_html(url, html)
            self.results.append(doc)

            # enqueue new links if we have space
            for link in doc.get("outbound_links", []):
                if len(self.results) < self.max_pages and link not in self.visited:
                    self.queue.put(link)

            self.queue.task_done()

    def run(self) -> List[Dict]:
        """Start the crawl and return parsed documents."""
        threads = []

        for _ in range(self.num_threads):
            t = threading.Thread(target=self.worker, daemon=True)
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        return self.results
