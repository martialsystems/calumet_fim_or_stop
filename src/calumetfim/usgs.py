# Copyright (c) 2026 Martial Systems LLC
"""Pin SIR 2020-5074 published profiles. No interpolation."""

from __future__ import annotations

from calumetfim.config import (
    FLOOD_GRIDID,
    FLOOD_STAGE_GAP_FT,
    GAGE_MUNSTER,
    GAGE_SOUTH_HOLLAND,
    HIGH_GRIDID,
    NWS_MINOR_STAGE_FT,
    PUBLISHED_PROFILES,
)
from calumetfim.errors import UsgsStageError

_BY_ID = {int(row[0]): row for row in PUBLISHED_PROFILES}


def profile_by_gridid(grid_id: int) -> tuple[int, float, float, float, float, str]:
    row = _BY_ID.get(int(grid_id))
    if row is None:
        raise UsgsStageError(
            f"GRIDID {grid_id} is not a published SIR 2020-5074 profile "
            f"{tuple(_BY_ID)}. Do not interpolate."
        )
    return row


def require_published_gridid(grid_id: int) -> int:
    return int(profile_by_gridid(grid_id)[0])


def require_published_south_holland_stage(stage_ft: float) -> float:
    target = float(stage_ft)
    for row in PUBLISHED_PROFILES:
        if abs(row[1] - target) < 1e-9:
            return row[1]
    raise UsgsStageError(
        f"South Holland stage {target} ft is not a published SIR 2020-5074 "
        "surface. Do not interpolate."
    )


def refuse_interpolated_stage(stage_ft: float) -> None:
    """NWS minor 16.00 is not a paint surface. GRIDID 11 is 16.32."""
    if abs(float(stage_ft) - NWS_MINOR_STAGE_FT) < 1e-9:
        raise UsgsStageError(
            f"stage {stage_ft} ft is NWS SHLI2 minor flood, not a published "
            f"library surface. Pin GRIDID {FLOOD_GRIDID} (16.32 ft, gap "
            f"{FLOOD_STAGE_GAP_FT} ft). Do not interpolate."
        )


def require_library_gages(gage_ids: tuple[str, str]) -> tuple[str, str]:
    a, b = str(gage_ids[0]), str(gage_ids[1])
    if {a, b} != {GAGE_SOUTH_HOLLAND, GAGE_MUNSTER}:
        raise UsgsStageError(
            f"gages {gage_ids} are not {GAGE_SOUTH_HOLLAND} and {GAGE_MUNSTER}"
        )
    return GAGE_SOUTH_HOLLAND, GAGE_MUNSTER


def pin_pairs() -> dict[str, dict[str, object]]:
    flood = profile_by_gridid(FLOOD_GRIDID)
    high = profile_by_gridid(HIGH_GRIDID)
    return {
        "flood": {
            "grid_id": flood[0],
            "south_holland_stage_ft": flood[1],
            "south_holland_elev_ft": flood[2],
            "munster_stage_ft": flood[3],
            "munster_elev_ft": flood[4],
            "profile": flood[5],
            "nws_minor_ft": NWS_MINOR_STAGE_FT,
            "gap_ft": FLOOD_STAGE_GAP_FT,
        },
        "high": {
            "grid_id": high[0],
            "south_holland_stage_ft": high[1],
            "south_holland_elev_ft": high[2],
            "munster_stage_ft": high[3],
            "munster_elev_ft": high[4],
            "profile": high[5],
        },
    }
