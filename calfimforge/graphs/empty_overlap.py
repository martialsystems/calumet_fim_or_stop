# Copyright (c) 2026 Martial Systems LLC
"""Refuse IoU paint when the Munster to South Holland window has no frozen HAND."""

from __future__ import annotations

from typing import Any

from calfimforge.graphs._common import binary_graph


def _evaluate(state: dict[str, Any]) -> dict[str, Any]:
    violations: list[str] = []
    empty = bool(state.get("overlap_empty"))
    paint = bool(state.get("paint_iou"))
    if empty and paint:
        violations.append("paint_iou_on_empty_overlap")
    return {
        "violations": violations,
        "events": [
            {"node": "evaluate", "ok": len(violations) == 0, "violations": list(violations)}
        ],
    }


def build_graph():
    # Fail closed: later agents who omit flags still try to paint an empty window.
    return binary_graph(
        name="calfim.empty_overlap",
        evaluate=_evaluate,
        extra=[("overlap_empty", True), ("paint_iou", True)],
    )
