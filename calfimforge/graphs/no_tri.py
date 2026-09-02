# Copyright (c) 2026 Martial Systems LLC
"""Refuse a TRI five-row overlay on this git."""

from __future__ import annotations

from typing import Any

from calfimforge.graphs._common import binary_graph


def _evaluate(state: dict[str, Any]) -> dict[str, Any]:
    violations = ["tri_five_row"] if state.get("tri_five_row") else []
    return {
        "violations": violations,
        "events": [
            {"node": "evaluate", "ok": len(violations) == 0, "violations": list(violations)}
        ],
    }


def build_graph():
    return binary_graph(
        name="calfim.no_tri",
        evaluate=_evaluate,
        extra=[("tri_five_row", False)],
    )
