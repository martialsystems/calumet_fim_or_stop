# Copyright (c) 2026 Martial Systems LLC
"""Clip to the Munster to South Holland library bbox. Refuse a whole-HUC mask."""

from __future__ import annotations

from typing import Any

import numpy as np

from calumetfim.config import (
    HYDRO_NODATA,
    TEMPLATE_SHAPE,
    WINDOW_LONLAT,
    ZONE_NODATA,
)
from calumetfim.errors import EmptyOverlapError, GateError


def window_from_bounds(dataset, lonlat: tuple[float, float, float, float] = WINDOW_LONLAT):
    from rasterio.warp import transform_bounds
    from rasterio.windows import from_bounds

    minx, miny, maxx, maxy = lonlat
    west, south, east, north = transform_bounds(
        "EPSG:4269", dataset.crs, minx, miny, maxx, maxy, densify_pts=21
    )
    win = from_bounds(west, south, east, north, transform=dataset.transform)
    return win.round_offsets().round_lengths()


def read_window(path, lonlat: tuple[float, float, float, float] = WINDOW_LONLAT):
    import rasterio

    with rasterio.open(path) as src:
        win = window_from_bounds(src, lonlat)
        arr = src.read(1, window=win)
        transform = src.window_transform(win)
        profile = src.profile.copy()
        profile.update(
            height=int(win.height),
            width=int(win.width),
            transform=transform,
        )
        return arr, profile, win


def finite_hydro(arr: np.ndarray, *, nodata: float = HYDRO_NODATA) -> np.ndarray:
    a = np.asarray(arr)
    return np.isfinite(a) & (a != nodata)


def require_not_huc_wide(mask: np.ndarray) -> np.ndarray:
    m = np.asarray(mask, dtype=bool)
    if not m.any():
        raise EmptyOverlapError(
            "Munster to South Holland window has no finite frozen HAND cells"
        )
    if int(m.sum()) == m.size:
        raise GateError("C refuses a HUC-wide wet/reach mask")
    if m.shape == TEMPLATE_SHAPE:
        raise GateError("window clip returned the full 04040001 template")
    return m


def overlap_counts(
    hand: np.ndarray,
    zone: np.ndarray,
    p_cal: np.ndarray,
    *,
    hand_nodata: float = HYDRO_NODATA,
    zone_nodata: int = ZONE_NODATA,
) -> dict[str, Any]:
    hf = finite_hydro(hand, nodata=hand_nodata)
    z = np.asarray(zone)
    z_ok = z != zone_nodata
    p = np.asarray(p_cal, dtype=np.float64)
    p_ok = np.isfinite(p) & (p >= 0.0)
    n = int(hand.size)
    n_hand = int(hf.sum())
    return {
        "n_window_cells": n,
        "n_hand_finite": n_hand,
        "n_zone_mapped": int(z_ok.sum()),
        "n_p_finite": int(p_ok.sum()),
        "window_is_huc": tuple(hand.shape) == TEMPLATE_SHAPE,
        "overlap_empty": n_hand == 0,
    }
