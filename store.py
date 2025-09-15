# ================================================================
# store.py
#
# This module handles saving Spider’s outputs to storage formats
# (JSON or CSV). Parsed docs and extracted signals can be persisted
# for later analysis.
#
# In short: this is the "data persistence layer" for Spider.
# ================================================================

# Import required modules
import json
import csv
from typing import List, Dict


def save_as_json(data: List[Dict], filename: str) -> None:
    """
    Save a list of dictionaries to a JSON file.

    Args:
        data (List[Dict]): List of structured data (docs or signals).
        filename (str): File path to save JSON.
    """
    # Open the file in write mode with UTF-8 encoding
    with open(filename, "w", encoding="utf-8") as f:
        # Dump the data into JSON with indentation for readability
        json.dump(data, f, ensure_ascii=False, indent=2)


def save_as_csv(data: List[Dict], filename: str) -> None:
    """
    Save a list of dictionaries to a CSV file.

    Args:
        data (List[Dict]): List of structured data (docs or signals).
        filename (str): File path to save CSV.
    """
    if not data:
        return  # Nothing to save

    # Extract field names from the first dictionary
    fieldnames = list(data[0].keys())

    # Open the file in write mode with newline='' to prevent blank lines
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        # Write header row
        writer.writeheader()

        # Write all rows of data
        for row in data:
            writer.writerow(row)


def store_results(results: List[Dict], base_filename: str) -> None:
    """
    Store results in both JSON and CSV formats for convenience.

    Args:
        results (List[Dict]): List of structured signals or docs.
        base_filename (str): Base name for the files (without extension).
    """
    # Save as JSON
    save_as_json(results, f"{base_filename}.json")

    # Save as CSV
    save_as_csv(results, f"{base_filename}.csv")
