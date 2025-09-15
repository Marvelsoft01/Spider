# ================================================================
# parser.py
#
# This module is responsible for parsing HTML content.
# It takes a raw HTML string, extracts useful information,
# and returns a structured dictionary that contains:
#   - the URL
#   - the page title (if available)
#   - the visible text content
#   - a list of outbound links (hrefs found in <a> tags)
#
# In short: this is the "interpreter" of web pages for Spider.
# ================================================================

# Import the built-in HTML parser library
from html.parser import HTMLParser

# Import typing tools for clarity: Dict for structured return, List for link lists
from typing import Dict, List


class SimpleHTMLParser(HTMLParser):
    """
    A simple subclass of HTMLParser that:
      - Captures text data between tags
      - Extracts href links from <a> tags
      - Detects the <title> of the page
    """

    def __init__(self):
        # Initialize the parent HTMLParser
        super().__init__()
        # Store all text content found in the HTML
        self.text_parts: List[str] = []
        # Store all outbound links (href values from <a> tags)
        self.links: List[str] = []
        # Store the title of the page (if <title> tag is found)
        self.title: str = ""
        # Boolean flag to check if we are inside a <title> tag
        self.in_title: bool = False

    def handle_starttag(self, tag: str, attrs: List[tuple]):
        """
        Called when the parser encounters an opening tag like <a> or <title>.
        """
        # If the tag is <a>, look for its href attribute
        if tag == "a":
            for (attr, value) in attrs:
                if attr == "href":
                    # Save the link if it exists
                    self.links.append(value)

        # If the tag is <title>, set flag to True so text inside is captured
        if tag == "title":
            self.in_title = True

    def handle_endtag(self, tag: str):
        """
        Called when the parser encounters a closing tag like </title>.
        """
        # When </title> is reached, stop recording title text
        if tag == "title":
            self.in_title = False

    def handle_data(self, data: str):
        """
        Called for text content found inside tags.
        """
        # Clean up the text by stripping whitespace
        clean_data = data.strip()

        # If we're inside <title>, save this text as the page title
        if self.in_title:
            self.title += clean_data

        # If it's non-empty text (like paragraph text), store it in text_parts
        if clean_data:
            self.text_parts.append(clean_data)


def parse_html(url: str, html: str) -> Dict:
    """
    Parse raw HTML into a structured document dictionary.

    Args:
        url (str): The URL of the page.
        html (str): The raw HTML content.

    Returns:
        Dict: A structured dictionary with:
            - "url": the page's URL
            - "title": the <title> text (or empty if not found)
            - "text": combined visible text content
            - "outbound_links": list of href links
    """
    # Create a parser instance
    parser = SimpleHTMLParser()
    # Feed the raw HTML into the parser
    parser.feed(html)

    # Combine all text parts into one big string, separated by spaces
    text_content = " ".join(parser.text_parts)

    # Return the structured document dictionary
    return {
        "url": url,
        "title": parser.title,
        "text": text_content,
        "outbound_links": parser.links,
    }
