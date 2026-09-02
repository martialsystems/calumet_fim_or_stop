# Copyright (c) 2026 Martial Systems LLC
"""Refuse Grand Calumet bathymetry or INFIP as a fallback library."""

from __future__ import annotations

from typing import Any

from calfimforge.graphs._common import binary_graph


def _evaluate(state: dict[str, Any]) -> dict[str, Any]:
    violations: list[str] = []
    if bool(state.get("grand_cal_bathy")):
        violations.append("grand_calumet_bathymetry")
    if bool(state.get("infip")):
        violations.append("infip_fallback")
    return {
        "violations": violations,
        "events": [
            {"node": "evaluate", "ok": len(violations) == 0, "violations": list(violations)}
        ],
    }


def build_graph():
    return binary_graph(
        name="calfim.no_substitute",
        evaluate=_evaluate,
        extra=[("grand_cal_bathy", False), ("infip", False)],
    )
