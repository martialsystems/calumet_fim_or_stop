# Copyright (c) 2026 Martial Systems LLC

import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from calfimforge._bootstrap import ensure_paths

ensure_paths()

from graphforge.product_law import LawBlockedError

from calfimforge.gate import (
    require_gridid,
    require_overlap,
    require_study,
    require_substitute,
    require_tri,
)
from calfimforge.product_laws import laws


def test_study_identity() -> None:
    require_study(dunn_straub_manaster=True, zip_is_lcalumeil=True, thread_id="t.st.ok")
    with pytest.raises(LawBlockedError):
        require_study(thread_id="t.st.default")
    with pytest.raises(LawBlockedError):
        require_study(dunn_straub_manaster=True, zip_is_lcalumeil=False, thread_id="t.st.zip")


def test_unpublished_gridid_and_16ft() -> None:
    require_gridid(published_gridid=True, interpolated=False, thread_id="t.g.ok")
    with pytest.raises(LawBlockedError):
        require_gridid(thread_id="t.g.default")
    with pytest.raises(LawBlockedError):
        require_gridid(published_gridid=True, interpolated=True, thread_id="t.g.16")


def test_substitutes_and_tri() -> None:
    require_substitute(thread_id="t.sub.ok")
    with pytest.raises(LawBlockedError):
        require_substitute(grand_cal_bathy=True, thread_id="t.sub.gc")
    with pytest.raises(LawBlockedError):
        require_substitute(infip=True, thread_id="t.sub.infip")
    require_tri(thread_id="t.tri.ok")
    with pytest.raises(LawBlockedError):
        require_tri(tri_five_row=True, thread_id="t.tri.row")


def test_empty_overlap_blocks_paint() -> None:
    require_overlap(overlap_empty=True, paint_iou=False, thread_id="t.o.stop")
    require_overlap(overlap_empty=False, paint_iou=True, thread_id="t.o.paint")
    with pytest.raises(LawBlockedError):
        require_overlap(thread_id="t.o.default")
    with pytest.raises(LawBlockedError):
        require_overlap(overlap_empty=True, paint_iou=True, thread_id="t.o.fake")


def test_five_laws_registry() -> None:
    ids = {row["id"] for row in laws()}
    assert ids == {
        "calfim.study_identity",
        "calfim.published_gridid",
        "calfim.no_substitute",
        "calfim.no_tri",
        "calfim.empty_overlap",
    }
