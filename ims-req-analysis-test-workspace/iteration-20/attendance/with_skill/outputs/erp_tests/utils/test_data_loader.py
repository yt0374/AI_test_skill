# erp_tests/utils/test_data_loader.py
"""Utilities for loading CSV/JSON test data."""

import csv
import json
from pathlib import Path
from typing import Any

TEST_DATA_DIR = Path(__file__).parent.parent / "test_data"


def load_csv(filename: str) -> list[dict[str, str]]:
    """Load a CSV file as list of dicts."""
    path = TEST_DATA_DIR / filename
    if not path.exists():
        raise FileNotFoundError(f"Test data file not found: {path}")
    with open(path, "r", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def load_json(filename: str) -> Any:
    """Load a JSON file."""
    path = TEST_DATA_DIR / filename
    if not path.exists():
        raise FileNotFoundError(f"Test data file not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def filter_by(data: list[dict], **kwargs) -> list[dict]:
    """Filter list of dicts by key-value pairs."""
    result = data
    for k, v in kwargs.items():
        result = [d for d in result if str(d.get(k, "")) == str(v)]
    return result


def get_unique_values(data: list[dict], field: str) -> list[str]:
    """Get unique values for a field from data list."""
    return list({d[field] for d in data if field in d})
