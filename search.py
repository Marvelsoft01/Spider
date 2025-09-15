# ================================================================
# search.py
#
# This module provides a simple keyword search interface on top
# of Spider’s inverted index. It looks up documents containing
# search terms and ranks them by frequency.
#
# In short: this is the "retrieval layer" for Spider.
# ================================================================

from typing import Dict, List


def search(index: Dict[str, List[str]], query: str) -> List[str]:
    """
    Search the inverted index for documents matching the query.

    Args:
        index (Dict[str, List[str]]): The inverted index
            - Keys: words
            - Values: list of document URLs containing the word
        query (str): The user’s search query (e.g., "python crawler")

    Returns:
        List[str]: Ranked list of matching document URLs
    """
    # Split query string into individual terms (case-insensitive)
    terms = query.lower().split()

    # Dictionary to store scores per document
    scores: Dict[str, int] = {}

    # For each term in the query
    for term in terms:
        # If the term is not in the index, skip it
        if term not in index:
            continue

        # For each document containing this term
        for doc in index[term]:
            # Increase its score (frequency count)
            scores[doc] = scores.get(doc, 0) + 1

    # Sort documents by score (descending order)
    ranked_docs = sorted(scores, key=lambda d: scores[d], reverse=True)

    return ranked_docs


def pretty_print_results(results: List[str], query: str) -> None:
    """
    Print search results in a readable format.

    Args:
        results (List[str]): List of ranked document URLs
        query (str): The original search query
    """
    # Print the search query as a header
    print(f"\nSearch results for: '{query}'")

    # If no results, inform the user
    if not results:
        print("No documents found.")
        return

    # Print each result with ranking number
    for i, doc in enumerate(results, start=1):
        print(f"{i}. {doc}")
