"""Tests for telemetry record validation."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from app.ingestion.validation import METRIC_UNITS, validate_record

FIXTURES = Path(__file__).resolve().parents[2] / "contracts" / "fixtures"


def valid() -> dict:
    return json.loads((FIXTURES / "valid_telemetry_record.json").read_text(encoding="utf-8"))


def test_the_contract_fixture_is_accepted():
    assert validate_record(valid()) == []


def test_every_metric_in_the_draft_dictionary_has_a_unit():
    assert all(METRIC_UNITS.values())


@pytest.mark.parametrize(
    "field", ["entity_id", "metric", "value", "unit", "timestamp", "source", "provenance"]
)
def test_missing_fields_are_reported(field):
    record = valid()
    del record[field]
    assert validate_record(record) == [f"missing field: {field}"]


@pytest.mark.parametrize(
    "changes,fragment",
    [
        ({"provenance": "GUESSED"}, "unknown provenance"),
        ({"timestamp": "yesterday"}, "timestamp"),
        ({"timestamp": "2026-11-25T10:00:00"}, "timezone"),
        ({"metric": "mystery"}, "unknown metric"),
        ({"unit": "fahrenheit"}, "unit for cpu_utilization"),
        ({"value": 140}, "between 0 and 100"),
        ({"value": "high"}, "number or null"),
        ({"value": True}, "number or null"),
    ],
)
def test_bad_records_are_rejected_with_a_reason(changes, fragment):
    problems = validate_record({**valid(), **changes})
    assert any(fragment in p for p in problems), problems


def test_null_values_must_be_marked_missing():
    record = {**valid(), "value": None}
    record.pop("quality")
    assert any("quality=missing" in p for p in validate_record(record))
    assert validate_record({**record, "quality": "missing"}) == []
