"""IMS Attendance — Test Data Loader

Utilities for loading CSV and JSON test data files.
"""

import csv
import json
from pathlib import Path
from typing import Any


def load_json(path: str) -> Any:
    """Load a JSON file."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_csv(path: str) -> list[dict]:
    """Load a CSV file as list of dicts."""
    with open(path, "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def load_dataset(name: str, data_dir: Path = None) -> dict:
    """Load a named dataset from test_data/test_data.json."""
    if data_dir is None:
        data_dir = Path(__file__).parent.parent / "test_data"
    full_data = load_json(str(data_dir / "test_data.json"))
    return full_data.get(name, {})


def get_parametrize_args(dataset_name: str) -> tuple:
    """Convert a dataset to pytest parametrize arguments.

    Returns (argnames, argvalues) tuple.
    """
    dataset = load_dataset(dataset_name)
    records = dataset.get("dataset", [])
    if not records:
        return ("empty", [])
    # Use all keys from first record as param names
    keys = list(records[0].keys())
    values = [[r.get(k) for k in keys] for r in records]
    return (",".join(keys), values)
