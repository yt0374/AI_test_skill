"""
Test data loading utilities for IMS ERP tests.

Supports CSV and JSON data formats.
"""
import csv
import json
from pathlib import Path
from typing import Any


def load_json_data(filename: str) -> dict:
    """Load test data from a JSON file."""
    data_path = Path(__file__).parent.parent / "test_data" / filename
    with open(data_path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_csv_data(filename: str) -> list[dict[str, str]]:
    """Load test data from a CSV file as list of dicts."""
    data_path = Path(__file__).parent.parent / "test_data" / filename
    with open(data_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def get_dataset(test_data: dict, dataset_name: str) -> dict:
    """Get a specific dataset from the test data dict."""
    return test_data.get("datasets", {}).get(dataset_name, {})


def get_records(test_data: dict, dataset_name: str) -> list[dict]:
    """Get records from a specific dataset."""
    dataset = get_dataset(test_data, dataset_name)
    return dataset.get("records", [])


def parametrize_from_json(dataset_name: str):
    """Create pytest parametrize decorator from JSON dataset.

    Usage:
        @parametrize_from_json("cpo_selection")
        def test_cpo(test_data, record): ...
    """
    import pytest
    data = load_json_data("test_data.json")
    records = get_records(data, dataset_name)
    ids = [r["id"] for r in records]
    return pytest.mark.parametrize("record", records, ids=ids)


def parametrize_from_csv(filename: str):
    """Create pytest parametrize decorator from CSV file.

    Usage:
        @parametrize_from_csv("test_data.csv")
        def test_data_driven(record): ...
    """
    import pytest
    rows = load_csv_data(filename)
    ids = [r.get("data_id", str(i)) for i, r in enumerate(rows)]
    return pytest.mark.parametrize("record", rows, ids=ids)
