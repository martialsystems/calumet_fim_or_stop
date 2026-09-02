# Copyright (c) 2026 Martial Systems LLC
"""HAND bathtub: wet iff HAND < (WSE - h_channel). Lock h_channel first."""

from __future__ import annotations

import numpy as np

from calumetfim.config import FT_TO_M, HYDRO_NODATA, WET_DRY, WET_NODATA, WET_WET
from calumetfim.errors import GateError


def wse_ft_navd88(*, stage_ft: float, datum_ft_navd88: float) -> float:
    if not np.isfinite(stage_ft) or not np.isfinite(datum_ft_navd88):
        raise GateError("stage and datum must be finite")
    return float(datum_ft_navd88) + float(stage_ft)


def relative_height_m(*, wse_navd88_m: float, h_channel_m: float) -> float:
    if not np.isfinite(wse_navd88_m) or not np.isfinite(h_channel_m):
        raise GateError("WSE and h_channel must be finite")
    return float(wse_navd88_m) - float(h_channel_m)


def paint_wet(
    hand: np.ndarray,
    *,
    delta_m: float,
    drain_to_reach: np.ndarray,
    h_channel_locked: bool,
) -> np.ndarray:
    if not h_channel_locked:
        raise GateError("lock h_channel before painting the wet mask")
    if not np.isfinite(delta_m):
        raise GateError("delta_m is not finite")
    hand_a = np.asarray(hand, dtype=np.float64)
    drain = np.asarray(drain_to_reach, dtype=bool)
    if hand_a.shape != drain.shape:
        raise GateError("HAND and drain-to-reach shapes differ")
    finite = np.isfinite(hand_a) & (hand_a != HYDRO_NODATA)
    out = np.full(hand_a.shape, WET_NODATA, dtype=np.uint8)
    on_reach = drain & finite
    out[on_reach] = np.where(hand_a[on_reach] < float(delta_m), WET_WET, WET_DRY)
    return out


def munster_delta_m(*, munster_elev_ft: float, h_channel_m: float) -> float:
    return relative_height_m(
        wse_navd88_m=float(munster_elev_ft) * FT_TO_M,
        h_channel_m=float(h_channel_m),
    )
