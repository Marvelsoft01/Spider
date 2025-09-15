# ================================================================
# signals.py
#
# This module scans parsed documents to extract "signals" that
# might be useful for sales, SEO, and lead generation.
#
# Signals include:
#   - Email addresses
#   - Phone numbers
#   - Call-to-action (CTA) phrases like "contact us" or "get a quote"
#
# In short: this is the "business insights extractor" for Spider.
# ================================================================

# Import regular expressions (re) for pattern matching
import re

# Import typing for clarity: Dict (structured document) and List (lists of signals)
from typing import Dict, List


def extract_emails(text: str) -> List[str]:
    """
    Extract all email addresses from text using regex.
    """
    # Regex pattern to match emails (simple version)
    pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    return re.findall(pattern, text)


def extract_phone_numbers(text: str) -> List[str]:
    """
    Extract phone numbers (basic patterns like +123-456-7890 or 1234567890).
    """
    # Regex pattern for phone-like numbers
    pattern = r"(\+?\d[\d\-\s]{7,}\d)"
    return re.findall(pattern, text)


def extract_cta_phrases(text: str) -> List[str]:
    """
    Extract call-to-action (CTA) phrases commonly used on business websites.
    """
    # List of common CTAs (can be expanded)
    cta_list = [
        "contact us",
        "get a quote",
        "buy now",
        "sign up",
        "subscribe",
        "free trial",
        "request demo",
        "book a call",
    ]

    found_ctas = []
    # Lowercase the text so search is case-insensitive
    text_lower = text.lower()

    # Check if each CTA phrase appears in the text
    for cta in cta_list:
        if cta in text_lower:
            found_ctas.append(cta)

    return found_ctas


def extract_signals(doc: Dict) -> Dict:
    """
    Extract all signals (emails, phones, CTAs) from a parsed document.

    Args:
        doc (Dict): A parsed document dictionary with "url" and "text".

    Returns:
        Dict: A dictionary with extracted signals:
            {
                "url": <page url>,
                "emails": [...],
                "phones": [...],
                "ctas": [...]
            }
    """
    # Get the text content of the document (default empty if missing)
    text = doc.get("text", "")

    # Run all extraction functions
    emails = extract_emails(text)
    phones = extract_phone_numbers(text)
    ctas = extract_cta_phrases(text)

    # Return structured signals
    return {
        "url": doc.get("url", ""),
        "emails": emails,
        "phones": phones,
        "ctas": ctas,
    }
