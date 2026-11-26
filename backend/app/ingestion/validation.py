"""Validation of one telemetry record before it is accepted (first draft for tasks DAT-03 and DAT-05).

The metric/unit table is a draft data dictionary; it is finalised by task DAT-01.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from ..provenance import Provenance

# metric -> expected unit (draft data dictionary)
METRIC_UNITS: dict[str, str] = {
    "cpu_utilization": "percent",
    "memory_utilization": "percent",
    "power": "watt",
    "energy": "kilowatt_hour",
    "inlet_temperature": "celsius",
    "rack_temperature": "celsius",
    "latency": "millisecond",
}
REQUIRED_FIELDS = (
    "schema_version",
    "entity_id",
    "metric",
    "value",
    "unit",
    "timestamp",
    "source",
    "provenance",
)


def _parse_timestamp(value: Any) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo is not None else None


def validate_record(record: dict[str, Any]) -> list[str]:
    """Return the reasons a record is rejected; an empty list means it is acceptable."""
    problems = [f"missing field: {name}" for name in REQUIRED_FIELDS if name not in record]
    if problems:
        return problems

    if record["provenance"] not in {label.value for label in Provenance}:
        problems.append(f"unknown provenance: {record['provenance']!r}")
    if _parse_timestamp(record["timestamp"]) is None:
        problems.append("timestamp must be an ISO 8601 date-time with a timezone")

    metric, unit, value = record["metric"], record["unit"], record["value"]
    if metric not in METRIC_UNITS:
        problems.append(f"unknown metric: {metric!r}")
    elif unit != METRIC_UNITS[metric]:
        problems.append(f"unit for {metric} must be {METRIC_UNITS[metric]!r}, got {unit!r}")

    if value is None:
        if record.get("quality") != "missing":
            problems.append("a null value must be marked quality=missing")
    elif isinstance(value, bool) or not isinstance(value, int | float):
        problems.append("value must be a number or null")
    elif unit == "percent" and not 0 <= value <= 100:
        problems.append("percent values must be between 0 and 100")
    return problems
