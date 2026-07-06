"""
Test data loading utilities for IMS API tests.
Supports CSV and JSON data files from test_data/ directory.
"""
import csv
import json
from pathlib import Path


TEST_DATA_DIR = Path(__file__).parent.parent / "test_data"


def load_csv(filename):
    """Load test data from CSV file. Returns list of dicts."""
    path = TEST_DATA_DIR / filename
    rows = []
    with open(path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


def load_json(filename):
    """Load test data from JSON file."""
    path = TEST_DATA_DIR / filename
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_api_payloads():
    """Load API test payloads."""
    return load_json("api_payloads.json")
