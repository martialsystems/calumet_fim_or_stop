# Copyright (c) 2026 Martial Systems LLC
"""Refuse unpublished GRIDIDs and interpolated stages (NWS 16.00 is not 16.32)."""

from __future__ import annotations

from typing import Any

from calfimforge.graphs._common import binary_graph


def _evaluate(state: dict[str, Any]) -> dict[str, Any]:
    violations: list[str] = []
    if not bool(state.get("published_gridid")):
        violations.append("unpublished_gridid")
    if bool(state.get("interpolated")):
        violations.append("interpolated_stage")
    return {
        "violations": violations,
        "events": [
            {"node": "evaluate", "ok": len(violations) == 0, "violations": list(violations)}
        ],
    }


def build_graph():
    return binary_graph(
        name="calfim.published_gridid",
        evaluate=_evaluate,
        extra=[("published_gridid", False), ("interpolated", True)],
    )
