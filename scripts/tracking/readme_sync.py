"""Render the generated README blocks and replace them between marker comments."""

from __future__ import annotations


def replace_block(text: str, name: str, content: str) -> str:
    """Replace the content between <!-- NAME:START --> and <!-- NAME:END -->."""
    start, end = f"<!-- {name}:START -->", f"<!-- {name}:END -->"
    if start not in text or end not in text:
        raise ValueError(f"README markers for {name} not found")
    head, rest = text.split(start, 1)
    _, tail = rest.split(end, 1)
    return f"{head}{start}\n{content.strip()}\n{end}{tail}"


def _activity_line(activity: dict | None) -> str:
    if activity is None:
        return "**Commit activity** (separate metric): n/a — computed on GitHub."
    return (
        f"**Commit activity** (separate metric): {activity['last_7_days']} commits in the last 7 days, "
        f"{activity['total']} in total. A commit never completes a task."
    )


def _percent(done: int, total: int) -> str:
    return f"{(100 * done / total) if total else 0:.0f}%"


def progress_block(metrics: dict, activity: dict | None) -> str:
    areas = "\n".join(
        f"| {c['prefix']} · {c['name']} | {c['done']} | {c['total']} | {_percent(c['core_done'], c['core_total'])} |"
        for c in metrics["concepts"]
    )
    owners = "\n".join(
        f"| {o['id']} — {o['role']} | {o['done']} | {o['total']} | {_percent(o['core_done'], o['core_total'])} |"
        for o in metrics["owners"]
    )
    return f"""<p align="center"><img src="assets/status/badges.svg" alt="Status badges"></p>

<p align="center"><img src="assets/status/progress.svg" alt="Project progress bars" width="900"></p>

<p align="center"><img src="assets/status/task-map.svg" alt="Task map: one tile per tracked task" width="900"></p>

**Actual progress:** {metrics["core_done"]} of {metrics["core_total"]} core tasks done ({metrics["core_pct"]:.1f}%). \
Optional tasks: {metrics["optional_done"]} of {metrics["optional_total"]}.

{_activity_line(activity)}

<details>
<summary>Progress by work area</summary>

| Work area | Done | Total | Core done |
|---|---:|---:|---:|
{areas}

</details>

<details>
<summary>Progress by owner</summary>

| Owner | Done | Total | Core done |
|---|---:|---:|---:|
{owners}

</details>"""


def milestones_block(metrics: dict) -> str:
    rows = "\n".join(
        f"| {m['id']} | {m['name']} | {m['status']}{' (optional)' if m['optional'] else ''} | "
        f"{m['tasks_done']}/{m['tasks_total']} | {m['gates_done']}/{m['gates_total']} |"
        for m in metrics["milestones"]
    )
    return f"""<p align="center"><img src="assets/status/milestones.svg" alt="Milestone cards" width="900"></p>

A milestone is complete only when all of its core tasks are done **and** every exit gate is ticked. The ten gates are indicative checkpoints, not promised dates.

| Milestone | Name | Status | Tasks | Gates |
|---|---|---|---:|---:|
{rows}"""
