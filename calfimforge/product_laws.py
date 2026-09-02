# Copyright (c) 2026 Martial Systems LLC
"""Five refuse laws. Verify-before-done is the finish gate. Science e11fce4."""

from __future__ import annotations

from typing import Any


def laws() -> list[dict[str, Any]]:
    from calfimforge.graphs.empty_overlap import build_graph as empty_overlap
    from calfimforge.graphs.no_substitute import build_graph as no_substitute
    from calfimforge.graphs.no_tri import build_graph as no_tri
    from calfimforge.graphs.published_gridid import build_graph as published_gridid
    from calfimforge.graphs.study_identity import build_graph as study_identity

    return [
        {
            "id": "calfim.study_identity",
            "build": study_identity,
            "state": {"dunn_straub_manaster": True, "zip_is_lcalumeil": True},
            "allow_decisions": ["allow"],
        },
        {
            "id": "calfim.published_gridid",
            "build": published_gridid,
            "state": {"published_gridid": True, "interpolated": False},
            "allow_decisions": ["allow"],
        },
        {
            "id": "calfim.no_substitute",
            "build": no_substitute,
            "state": {"grand_cal_bathy": False, "infip": False},
            "allow_decisions": ["allow"],
        },
        {
            "id": "calfim.no_tri",
            "build": no_tri,
            "state": {"tri_five_row": False},
            "allow_decisions": ["allow"],
        },
        {
            "id": "calfim.empty_overlap",
            "build": empty_overlap,
            "state": {"overlap_empty": True, "paint_iou": False},
            "allow_decisions": ["allow"],
        },
    ]
