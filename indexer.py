# ================================================================
# indexer.py
#
# This module is responsible for indexing parsed documents.
# It builds an "inverted index", which is a data structure
# that maps each word (token) to the list of documents
# in which that word appears.
#
# Example:
#   documents = [
#       {"url": "http://a.com", "text": "hello world"},
#       {"url": "http://b.com", "text": "hello spider"}
#   ]
#
#   inverted_index = {
#       "hello": ["http://a.com", "http://b.com"],
#       "world": ["http://a.com"],
#       "spider": ["http://b.com"]
#   }
#
# In short: this is the "search engine brain" of Spider.
# ================================================================

# Import re for text tokenization (splitting into words)
import re

# Import typing helpers for clarity
from typing import Dict, List


class Indexer:
    """
    Build and manage an inverted index for quick keyword-based search.
    """

    def __init__(self):
        # Store the inverted index as a dictionary:
        # key = token (word), value = list of document URLs
        self.index: Dict[str, List[str]] = {}

    def tokenize(self, text: str) -> List[str]:
        """
        Convert raw text into a list of lowercase word tokens.

        Args:
            text (str): The raw text from a document.

        Returns:
            List[str]: A list of clean, lowercase tokens.
        """
        # Use regex to split text into words (a-z characters only)
        tokens = re.findall(r"[a-zA-Z]+", text.lower())
        return tokens

    def add_document(self, doc: Dict):
        """
        Add a parsed document into the inverted index.

        Args:
            doc (Dict): A document dictionary with "url" and "text".
        """
        # Get the document's URL
        url = doc.get("url", "")
        # Get the document's text
        text = doc.get("text", "")

        # Break the text into tokens (words)
        tokens = self.tokenize(text)

        # For each token, add the document's URL to the index
        for token in tokens:
            if token not in self.index:
                # Create a new entry if token not seen before
                self.index[token] = []
            if url not in self.index[token]:
                # Append URL if not already listed for this token
                self.index[token].append(url)

    def search(self, query: str) -> List[str]:
        """
        Search the index for documents containing a given query word.

        Args:
            query (str): A single word to search for.

        Returns:
            List[str]: List of document URLs where the word appears.
        """
        # Normalize query by lowering case
        query_token = query.lower()

        # Return the URLs for this word, or empty list if not found
        return self.index.get(query_token, [])
