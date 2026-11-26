"""Parse and validate TRACKING.md (the tracking source). Standard library only."""

from __future__ import annotations

import re
from dataclasses import dataclass, field

PREFIXES = (
    "PLT",
    "DAT",
    "COK",
    "DET",
    "FOR",
    "RES",
    "TWN",
    "OPT",
    "DEC",
    "SAF",
    "EVL",
    "CLD",
    "DEV",
    "SEC",
    "OPS",
    "UXV",
)
TASK_ID = re.compile(rf"^({'|'.join(PREFIXES)})-\d{{2}}$")
AREA_ID = re.compile(r"^A\d{2}$")
MILESTONE_ID = re.compile(r"^M(0[1-9]|1[01])$")
OWNER_ID = re.compile(r"^Member [1-3]$")
GATE_LINE = re.compile(r"^- \[( |x|X)\] (M(?:0[1-9]|1[01]))-G(\d+) (.+)$")
PRIORITIES = ("P0", "P1", "P2")
STATUSES = ("todo", "doing", "blocked", "done")


@dataclass
class Task:
    id: str
    title: str
    pri: str
    ms: str
    owner: str
    deps: list[str]
    status: str
    line: int

    @property
    def prefix(self) -> str:
        return self.id.split("-")[0]

    @property
    def core(self) -> bool:
        return self.pri in ("P0", "P1")


@dataclass
class Concept:
    cid: str
    name: str
    prefix: str


@dataclass
class Owner:
    id: str
    role: str


@dataclass
class Milestone:
    id: str
    name: str
    objective: str


@dataclass
class Gate:
    ms: str
    num: int
    text: str
    checked: bool
    line: int


@dataclass
class Plan:
    tasks: list[Task] = field(default_factory=list)
    concepts: list[Concept] = field(default_factory=list)
    owners: list[Owner] = field(default_factory=list)
    milestones: list[Milestone] = field(default_factory=list)
    gates: list[Gate] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


def _cells(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def parse_plan(text: str) -> Plan:
    """Extract tasks, areas, owners, milestones and gates from the tracking text."""
    plan = Plan()
    for number, line in enumerate(text.split("\n"), start=1):
        gate = GATE_LINE.match(line)
        if gate:
            plan.gates.append(
                Gate(gate.group(2), int(gate.group(3)), gate.group(4), gate.group(1) != " ", number)
            )
            continue
        if not line.startswith("|"):
            continue
        cells = _cells(line)
        first = cells[0]
        if TASK_ID.match(first):
            if len(cells) != 8:
                plan.errors.append(f"line {number}: task row {first} has {len(cells)} columns, expected 8")
                continue
            deps = [] if cells[5] in ("—", "-", "") else [d.strip() for d in cells[5].split(",")]
            plan.tasks.append(Task(first, cells[1], cells[2], cells[3], cells[4], deps, cells[7], number))
        elif AREA_ID.match(first) and len(cells) == 3:
            plan.concepts.append(Concept(first, cells[1], cells[2]))
        elif OWNER_ID.match(first) and len(cells) == 2:
            plan.owners.append(Owner(first, cells[1]))
        elif MILESTONE_ID.match(first) and len(cells) == 4:
            plan.milestones.append(Milestone(first, cells[1], cells[2]))
    return plan


def validate_plan(plan: Plan) -> list[str]:
    """Return a list of problems; an empty list means the tracking contract is satisfied."""
    errors = list(plan.errors)
    if not plan.tasks:
        errors.append("no task rows found")
    owner_ids = {o.id for o in plan.owners}
    by_id: dict[str, Task] = {}
    for task in plan.tasks:
        if task.id in by_id:
            errors.append(f"line {task.line}: duplicate task id {task.id}")
        by_id[task.id] = task
        if task.pri not in PRIORITIES:
            errors.append(f"line {task.line}: {task.id} has invalid priority {task.pri!r}")
        if not MILESTONE_ID.match(task.ms):
            errors.append(f"line {task.line}: {task.id} has invalid milestone {task.ms!r}")
        if task.status not in STATUSES:
            errors.append(f"line {task.line}: {task.id} has invalid status {task.status!r}")
        if task.owner not in owner_ids:
            errors.append(f"line {task.line}: {task.id} has unknown owner {task.owner!r}")
    concept_prefixes = {c.prefix for c in plan.concepts}
    for task in plan.tasks:
        if task.prefix not in concept_prefixes:
            errors.append(f"line {task.line}: {task.id} prefix is not in the work-area table")
    milestone_ids = {m.id for m in plan.milestones}
    for expected in (f"M{i:02d}" for i in range(1, 12)):
        if expected not in milestone_ids:
            errors.append(f"milestone {expected} missing from the milestone table")
    for gate in plan.gates:
        if gate.ms not in milestone_ids:
            errors.append(f"line {gate.line}: gate refers to unknown milestone {gate.ms}")
    for task in plan.tasks:
        for dep in task.deps:
            other = by_id.get(dep)
            if other is None:
                errors.append(f"line {task.line}: {task.id} depends on unknown task {dep}")
                continue
            if MILESTONE_ID.match(other.ms) and MILESTONE_ID.match(task.ms) and other.ms > task.ms:
                errors.append(
                    f"line {task.line}: {task.id} ({task.ms}) depends on {dep} in later milestone {other.ms}"
                )
            if other.pri == "P2" and task.pri != "P2":
                errors.append(f"line {task.line}: core task {task.id} depends on optional task {dep}")
    errors.extend(_cycles(by_id))
    return errors


def _cycles(by_id: dict[str, Task]) -> list[str]:
    found: list[str] = []
    state: dict[str, int] = {}

    def visit(node: str, path: list[str]) -> None:
        state[node] = 1
        for dep in by_id[node].deps:
            if dep not in by_id:
                continue
            if state.get(dep) == 1:
                found.append("dependency cycle: " + " -> ".join(path + [node, dep]))
            elif dep not in state:
                visit(dep, path + [node])
        state[node] = 2

    for node in by_id:
        if node not in state:
            visit(node, [])
    return found
