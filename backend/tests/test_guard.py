"""Tests for the deterministic action guard."""

from __future__ import annotations

import pytest
from app.safety.guard import ALLOWED_ACTIONS, HIGH_IMPACT_ACTIONS, evaluate_action


@pytest.mark.parametrize("action", sorted(HIGH_IMPACT_ACTIONS))
@pytest.mark.parametrize("mode", ["sandbox", "advisory", "production", "anything"])
def test_high_impact_actions_are_never_allowed(action, mode):
    decision = evaluate_action(action, mode)
    assert decision.allowed is False


def test_production_mode_blocks_everything():
    for actions in ALLOWED_ACTIONS.values():
        for action in actions:
            assert evaluate_action(action, "production").rule == "no-production-execution"


def test_allowlisted_actions_pass_in_their_own_mode_only():
    assert evaluate_action("run_experiment", "sandbox").allowed
    assert evaluate_action("recommend_placement", "advisory").allowed
    assert evaluate_action("recommend_placement", "sandbox").rule == "not-allowlisted"
    assert evaluate_action("run_experiment", "advisory").rule == "not-allowlisted"


def test_unknown_actions_and_modes_are_denied_by_default():
    assert evaluate_action("do_something_new", "sandbox").allowed is False
    assert evaluate_action("run_experiment", "staging").rule == "unknown-mode"


def test_every_decision_explains_itself():
    for action, mode in [("run_experiment", "sandbox"), ("server_reboot", "advisory"), ("x", "y")]:
        decision = evaluate_action(action, mode)
        assert decision.rule and decision.reason


def test_the_allowlists_never_overlap_with_the_blocked_actions():
    for actions in ALLOWED_ACTIONS.values():
        assert not actions & HIGH_IMPACT_ACTIONS
