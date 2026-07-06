"""Utility for loading CSV/JSON test data files.

Provides load_test_data_csv() and load_test_data_json() functions
that search both erp_tests/test_data/ and the parent outputs/ directory.
"""
import csv
import json
from pathlib import Path
from typing import Any


def _find_data_file(filename: str) -> Path:
    """Find a test data file in known locations."""
    candidates = [
        Path(__file__).parent.parent / "test_data" / filename,
        Path(__file__).parent.parent.parent / filename,
    ]
    for p in candidates:
        if p.exists():
            return p
    raise FileNotFoundError(
        f"Test data file not found: {filename} (searched: {candidates})"
    )


def load_test_data_csv(filename: str) -> list[dict[str, str]]:
    """Load CSV test data as list of dicts.

    Args:
        filename: CSV filename (e.g., 'test_data.csv')

    Returns:
        List of dicts keyed by CSV column headers
    """
    filepath = _find_data_file(filename)
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def load_test_data_json(filename: str) -> Any:
    """Load JSON test data.

    Args:
        filename: JSON filename

    Returns:
        Parsed JSON data (dict or list)
    """
    filepath = _find_data_file(filename)
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def get_data_by_id(data: list[dict], data_id: str) -> dict | None:
    """Find a test data record by its data_id field."""
    for record in data:
        if record.get("data_id") == data_id:
            return record
    return None


def get_data_by_scenario(data: list[dict], scenario_filter: str) -> list[dict]:
    """Filter test data records by scenario field (partial match)."""
    return [r for r in data if scenario_filter in r.get("scenario", "")]
