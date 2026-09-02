# Copyright (c) 2026 Martial Systems LLC

import pytest

from calumetfim.config import FLOOD_GRIDID, GAGE_MUNSTER, GAGE_SOUTH_HOLLAND, HIGH_GRIDID
from calumetfim.errors import UsgsStageError
from calumetfim.usgs import (
    pin_pairs,
    refuse_interpolated_stage,
    require_library_gages,
    require_published_gridid,
    require_published_south_holland_stage,
)


def test_published_profiles_only() -> None:
    assert require_published_gridid(FLOOD_GRIDID) == 11
    assert require_published_gridid(HIGH_GRIDID) == 24
    assert require_published_south_holland_stage(16.32) == 16.32
    with pytest.raises(UsgsStageError):
        require_published_south_holland_stage(16.0)
    with pytest.raises(UsgsStageError):
        require_published_gridid(25)
    with pytest.raises(UsgsStageError):
        refuse_interpolated_stage(16.0)
    pairs = pin_pairs()
    assert pairs["flood"]["grid_id"] == 11
    assert pairs["flood"]["south_holland_stage_ft"] == 16.32
    assert pairs["flood"]["gap_ft"] == 0.32
    assert pairs["high"]["grid_id"] == 24


def test_library_gages() -> None:
    assert require_library_gages((GAGE_SOUTH_HOLLAND, GAGE_MUNSTER))[1] == GAGE_MUNSTER
    with pytest.raises(UsgsStageError):
        require_library_gages(("03351000", GAGE_MUNSTER))
