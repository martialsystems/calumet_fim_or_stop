# Copyright (c) 2026 Martial Systems LLC
"""Call sites for the five refuse laws."""

from __future__ import annotations

from typing import Any

from calfimforge._bootstrap import ensure_paths

ensure_paths()

from graphforge.product_law import require_law

from calfimforge.graphs.empty_overlap import build_graph as build_overlap
from calfimforge.graphs.no_substitute import build_graph as build_substitute
from calfimforge.graphs.no_tri import build_graph as build_tri
from calfimforge.graphs.published_gridid import build_graph as build_gridid
from calfimforge.graphs.study_identity import build_graph as build_study


def _run(build, law_id: str, state: dict[str, Any], thread_id: str) -> None:
    require_law(
        build(),
        state,
        allow_decisions=["allow"],
        law_id=law_id,
        thread_id=thread_id,
        raise_error=True,
    )


def require_study(**flags: Any) -> None:
    thread_id = str(flags.pop("thread_id", "calfim_study"))
    state = {"dunn_straub_manaster": False, "zip_is_lcalumeil": False}
    state.update(flags)
    _run(build_study, "calfim.study_identity", state, thread_id)


def require_gridid(**flags: Any) -> None:
    thread_id = str(flags.pop("thread_id", "calfim_gridid"))
    state = {"published_gridid": False, "interpolated": True}
    state.update(flags)
    _run(build_gridid, "calfim.published_gridid", state, thread_id)


def require_substitute(**flags: Any) -> None:
    thread_id = str(flags.pop("thread_id", "calfim_sub"))
    state = {"grand_cal_bathy": False, "infip": False}
    state.update(flags)
    _run(build_substitute, "calfim.no_substitute", state, thread_id)


def require_tri(**flags: Any) -> None:
    thread_id = str(flags.pop("thread_id", "calfim_tri"))
    state = {"tri_five_row": False}
    state.update(flags)
    _run(build_tri, "calfim.no_tri", state, thread_id)


def require_overlap(**flags: Any) -> None:
    thread_id = str(flags.pop("thread_id", "calfim_overlap"))
    state = {"overlap_empty": True, "paint_iou": True}
    state.update(flags)
    _run(build_overlap, "calfim.empty_overlap", state, thread_id)
