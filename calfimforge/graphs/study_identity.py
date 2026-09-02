# Copyright (c) 2026 Martial Systems LLC
"""Refuse if the GIS is not Dunn/Straub/Manaster 2020 lcalumeil."""

from __future__ import annotations

from typing import Any

from calfimforge.graphs._common import binary_graph


def _evaluate(state: dict[str, Any]) -> dict[str, Any]:
    violations: list[str] = []
    if not bool(state.get("dunn_straub_manaster")):
        violations.append("study_not_dunn_straub_manaster_2020")
    if not bool(state.get("zip_is_lcalumeil")):
        violations.append("zip_not_lcalumeil")
    return {
        "violations": violations,
        "events": [
            {"node": "evaluate", "ok": len(violations) == 0, "violations": list(violations)}
        ],
    }


def build_graph():
    return binary_graph(
        name="calfim.study_identity",
        evaluate=_evaluate,
        extra=[("dunn_straub_manaster", False), ("zip_is_lcalumeil", False)],
    )
