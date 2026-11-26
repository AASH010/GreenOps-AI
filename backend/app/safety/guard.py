"""Deterministic action guard (first draft for task SAF-02).

Pure functions with no network access and no model calls: the guard works without cloud connectivity and
cannot be influenced by LLM output. Anything not explicitly allowed is denied.
"""

from __future__ import annotations

from dataclasses import dataclass

# Actions the MVP never performs, in any mode (see the safety boundary, task SAF-01).
HIGH_IMPACT_ACTIONS = frozenset(
    {
        "cooling_setpoint_change",
        "chiller_control",
        "crac_crah_control",
        "ups_control",
        "switchgear_control",
        "power_distribution_control",
        "server_shutdown",
        "server_reboot",
        "production_workload_migration",
    }
)

# Allowlist per execution mode. Everything else is refused.
ALLOWED_ACTIONS: dict[str, frozenset[str]] = {
    "sandbox": frozenset({"run_experiment", "simulate_placement", "simulate_capacity_change"}),
    "advisory": frozenset({"recommend_placement", "recommend_capacity_change", "advise_cooling_review"}),
}


@dataclass(frozen=True)
class GuardDecision:
    allowed: bool
    rule: str
    reason: str


def evaluate_action(action: str, mode: str) -> GuardDecision:
    """Decide whether an action may run in the given mode ('sandbox', 'advisory' or anything else)."""
    if mode == "production":
        return GuardDecision(False, "no-production-execution", "Production execution is disabled in the MVP.")
    if action in HIGH_IMPACT_ACTIONS:
        return GuardDecision(
            False, "high-impact-blocked", f"{action} is a high-impact action and is blocked."
        )
    if mode not in ALLOWED_ACTIONS:
        return GuardDecision(False, "unknown-mode", f"Unknown execution mode {mode!r}; denied by default.")
    if action not in ALLOWED_ACTIONS[mode]:
        return GuardDecision(False, "not-allowlisted", f"{action} is not allowlisted in {mode} mode.")
    return GuardDecision(True, "allowlisted", f"{action} is allowed in {mode} mode.")
