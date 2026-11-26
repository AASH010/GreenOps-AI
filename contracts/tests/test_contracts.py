"""Contract tests: schemas are valid, fixtures behave, and the seven contracts agree with each other."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

CONTRACTS = Path(__file__).resolve().parents[1]
NAMES = [
    "telemetry_record",
    "asset",
    "research_case",
    "hypothesis",
    "experiment_spec",
    "experiment_result",
    "decision_certificate",
]
INVALID_TO_SCHEMA = {
    "telemetry_null_without_missing_quality": "telemetry_record",
    "telemetry_unknown_provenance": "telemetry_record",
    "asset_unknown_kind": "asset",
    "hypothesis_not_falsifiable": "hypothesis",
    "experiment_spec_not_sandboxed": "experiment_spec",
    "experiment_result_measured": "experiment_result",
    "certificate_execution_allowed": "decision_certificate",
    "certificate_not_advisory": "decision_certificate",
    "certificate_without_limitations": "decision_certificate",
    "case_without_trigger": "research_case",
}


def load(relative: str) -> dict:
    return json.loads((CONTRACTS / relative).read_text(encoding="utf-8"))


SCHEMAS = {name: load(f"schemas/{name}.schema.json") for name in NAMES}


def errors(name: str, document: dict) -> list:
    return list(Draft202012Validator(SCHEMAS[name]).iter_errors(document))


@pytest.mark.parametrize("name", NAMES)
def test_schemas_are_valid_and_versioned(name):
    Draft202012Validator.check_schema(SCHEMAS[name])
    assert SCHEMAS[name]["properties"]["schema_version"] == {"const": "0.1.0"}
    assert SCHEMAS[name]["additionalProperties"] is False


def test_schema_ids_are_unique():
    ids = [s["$id"] for s in SCHEMAS.values()]
    assert len(ids) == len(set(ids))


@pytest.mark.parametrize("name", NAMES)
def test_valid_fixtures_pass(name):
    assert errors(name, load(f"fixtures/valid_{name}.json")) == []


@pytest.mark.parametrize("fixture,name", sorted(INVALID_TO_SCHEMA.items()))
def test_invalid_fixtures_fail(fixture, name):
    assert errors(name, load(f"fixtures/invalid_{fixture}.json"))


def test_every_invalid_fixture_file_is_covered():
    files = {p.stem.removeprefix("invalid_") for p in (CONTRACTS / "fixtures").glob("invalid_*.json")}
    assert files == set(INVALID_TO_SCHEMA)


def test_timestamps_must_look_like_rfc3339():
    record = load("fixtures/valid_telemetry_record.json")
    record["timestamp"] = "yesterday"
    assert errors("telemetry_record", record)


def test_provenance_labels_match_across_contracts():
    expected = ["MEASURED", "REPLAYED", "ESTIMATED", "SIMULATED"]
    assert SCHEMAS["telemetry_record"]["properties"]["provenance"]["enum"] == expected
    assert SCHEMAS["asset"]["properties"]["provenance"]["enum"] == expected
    assert SCHEMAS["decision_certificate"]["properties"]["provenance_labels"]["items"]["enum"] == expected


def test_unknown_fields_are_rejected():
    record = load("fixtures/valid_telemetry_record.json")
    record["surprise"] = 1
    assert errors("telemetry_record", record)


def test_valid_fixtures_describe_one_coherent_case():
    case = load("fixtures/valid_research_case.json")
    hypothesis = load("fixtures/valid_hypothesis.json")
    spec = load("fixtures/valid_experiment_spec.json")
    certificate = load("fixtures/valid_decision_certificate.json")
    result = load("fixtures/valid_experiment_result.json")
    assert hypothesis["case_id"] == spec["case_id"] == certificate["case_id"] == case["case_id"]
    assert hypothesis["hypothesis_id"] in case["hypothesis_ids"]
    assert set(spec["hypothesis_ids"]) == set(case["hypothesis_ids"])
    assert result["experiment_id"] == spec["experiment_id"]
    assert spec["experiment_id"] in certificate["evidence_refs"]
