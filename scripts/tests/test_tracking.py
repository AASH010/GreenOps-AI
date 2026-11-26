"""Tests for the tracking contract, metrics, README sync and SVG generation."""

from __future__ import annotations

import shutil
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from tracking.cli import main  # noqa: E402
from tracking.metrics import commit_activity, compute_metrics  # noqa: E402
from tracking.plan_parser import parse_plan, validate_plan  # noqa: E402
from tracking.readme_sync import replace_block  # noqa: E402
from tracking.svg_render import badges_svg, milestones_svg, progress_svg, taskmap_svg  # noqa: E402

MILESTONES = "\n".join(f"| M{i:02d} | Milestone {i} | Objective {i} | — |" for i in range(1, 12))
GATES = "\n".join(f"- [ ] M{i:02d}-G1 Gate {i}" for i in range(1, 12))


def make_plan(task_rows: str, gates: str = GATES) -> str:
    return f"""
| Owner | Accountability |
|---|---|
| Member 1 | Platform |
| Member 2 | Intelligence |
| Member 3 | Twin |

| Area | Name | Prefix |
|---|---|---|
| A01 | Platform | PLT |
| A02 | Data | DAT |

| ID | Name | Objective | Depends on |
|---|---|---|---|
{MILESTONES}

{gates}

| ID | Task | Pri | MS | Owner | Depends | Done when | Status |
|---|---|---|---|---|---|---|---|
{task_rows}
"""


def row(task_id: str, pri="P0", ms="M01", deps="—", status="todo", owner="Member 1") -> str:
    return f"| {task_id} | Task {task_id} | {pri} | {ms} | {owner} | {deps} | done when | {status} |"


def errors_for(rows: str) -> list[str]:
    return validate_plan(parse_plan(make_plan(rows)))


def test_real_tracking_file_satisfies_the_contract():
    plan = parse_plan((ROOT / "TRACKING.md").read_text(encoding="utf-8"))
    assert validate_plan(plan) == []
    assert len(plan.tasks) > 100
    assert len(plan.milestones) == 11
    assert {o.id for o in plan.owners} == {"Member 1", "Member 2", "Member 3"}


def test_valid_minimal_plan():
    assert errors_for(row("PLT-01") + "\n" + row("DAT-01", deps="PLT-01")) == []


@pytest.mark.parametrize(
    "rows,fragment",
    [
        (row("PLT-01") + "\n" + row("PLT-01"), "duplicate task id"),
        (row("PLT-01", deps="PLT-09"), "unknown task"),
        (row("PLT-01", status="finished"), "invalid status"),
        (row("PLT-01", pri="P9"), "invalid priority"),
        (row("PLT-01", ms="M12"), "invalid milestone"),
        (row("PLT-01", owner="Member 9"), "unknown owner"),
        (row("PLT-01", ms="M02") + "\n" + row("DAT-01", ms="M01", deps="PLT-01"), "later milestone"),
        (row("PLT-01", pri="P2") + "\n" + row("DAT-01", deps="PLT-01"), "optional task"),
        (row("PLT-01", deps="DAT-01") + "\n" + row("DAT-01", deps="PLT-01"), "cycle"),
        ("| PLT-01 | only | three |", "columns"),
    ],
)
def test_violations_are_reported(rows, fragment):
    assert any(fragment in e for e in errors_for(rows)), errors_for(rows)


def test_requirement_style_ids_are_not_tasks():
    assert parse_plan("| NFR-01 | text | more |").tasks == []


def test_progress_is_derived_from_statuses_only():
    rows = "\n".join(
        [
            row("PLT-01", status="done"),
            row("PLT-02", status="doing"),
            row("DAT-01", owner="Member 2"),
            row("DAT-02", pri="P2", status="done"),
        ]
    )
    metrics = compute_metrics(parse_plan(make_plan(rows)))
    assert (metrics["core_done"], metrics["core_total"], metrics["core_pct"]) == (1, 3, 33.3)
    assert (metrics["optional_done"], metrics["optional_total"]) == (1, 1)
    assert next(m for m in metrics["milestones"] if m["id"] == "M01")["status"] == "in progress"
    owner_1 = next(o for o in metrics["owners"] if o["id"] == "Member 1")
    assert (owner_1["total"], owner_1["done"]) == (3, 2)


def test_milestone_needs_both_tasks_and_gates():
    rows = row("PLT-01", status="done")
    unticked = compute_metrics(parse_plan(make_plan(rows)))
    assert next(m for m in unticked["milestones"] if m["id"] == "M01")["status"] != "complete"
    ticked = compute_metrics(parse_plan(make_plan(rows, GATES.replace("- [ ] M01-G1", "- [x] M01-G1"))))
    assert next(m for m in ticked["milestones"] if m["id"] == "M01")["status"] == "complete"
    assert ticked["milestones_done"] == 1 and ticked["milestones_total"] == 10


def test_blocked_task_blocks_the_milestone():
    metrics = compute_metrics(parse_plan(make_plan(row("PLT-01", status="blocked"))))
    assert next(m for m in metrics["milestones"] if m["id"] == "M01")["status"] == "blocked"


def test_optional_milestone_is_excluded_from_the_headline():
    rows = row("PLT-01", pri="P2", ms="M11", status="done")
    gates = GATES.replace("- [ ] M11-G1", "- [x] M11-G1")
    metrics = compute_metrics(parse_plan(make_plan(rows, gates)))
    m11 = next(m for m in metrics["milestones"] if m["id"] == "M11")
    assert m11["status"] == "complete" and m11["optional"]
    assert metrics["milestones_done"] == 0


def test_replace_block_is_idempotent_and_strict():
    text = "a\n<!-- X:START -->\nold\n<!-- X:END -->\nb\n"
    once = replace_block(text, "X", "new")
    assert once == "a\n<!-- X:START -->\nnew\n<!-- X:END -->\nb\n"
    assert replace_block(once, "X", "new") == once
    with pytest.raises(ValueError):
        replace_block("no markers", "X", "new")


def test_svgs_are_well_formed_and_reflect_the_tracking_file():
    plan = parse_plan((ROOT / "TRACKING.md").read_text(encoding="utf-8"))
    metrics = compute_metrics(plan)
    for svg in (
        badges_svg(metrics, None),
        badges_svg(metrics, {"last_7_days": 3, "total": 10}),
        progress_svg(metrics, None),
        taskmap_svg(plan),
        milestones_svg(metrics),
    ):
        ET.fromstring(svg)
    titles = ET.fromstring(taskmap_svg(plan)).findall(".//{http://www.w3.org/2000/svg}title")
    assert len(titles) == len(plan.tasks) + 1  # one per tile plus the document title


def test_commit_activity_is_none_outside_git(tmp_path):
    assert commit_activity(tmp_path) is None


def test_cli_write_is_idempotent(tmp_path):
    shutil.copy(ROOT / "TRACKING.md", tmp_path / "TRACKING.md")
    readme = (
        "<!-- PROGRESS:START -->\n<!-- PROGRESS:END -->\n<!-- MILESTONES:START -->\n<!-- MILESTONES:END -->\n"
    )
    (tmp_path / "README.md").write_text(readme, encoding="utf-8")
    assert main(["--write", "--root", str(tmp_path)]) == 0
    first = (tmp_path / "README.md").read_text(encoding="utf-8")
    assert "task-map.svg" in first and "Progress by owner" in first
    assert main(["--write", "--root", str(tmp_path)]) == 0
    assert (tmp_path / "README.md").read_text(encoding="utf-8") == first
    assert {p.name for p in (tmp_path / "assets" / "status").iterdir()} == {
        "badges.svg",
        "progress.svg",
        "task-map.svg",
        "milestones.svg",
    }


def test_cli_leaves_the_readme_untouched_on_an_invalid_file(tmp_path):
    (tmp_path / "TRACKING.md").write_text(make_plan(row("PLT-01", status="oops")), encoding="utf-8")
    original = "<!-- PROGRESS:START -->\nkeep\n<!-- PROGRESS:END -->\n<!-- MILESTONES:START -->\n<!-- MILESTONES:END -->\n"
    (tmp_path / "README.md").write_text(original, encoding="utf-8")
    assert main(["--write", "--root", str(tmp_path)]) == 1
    assert (tmp_path / "README.md").read_text(encoding="utf-8") == original
