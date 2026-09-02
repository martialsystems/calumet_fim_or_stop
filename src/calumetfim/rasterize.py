# Copyright (c) 2026 Martial Systems LLC
"""Rasterize one published GRIDID polygon onto the window."""

from __future__ import annotations

from pathlib import Path

import numpy as np

from calumetfim.config import TEMPLATE_CRS, USGS_SHP_REL, WET_NODATA
from calumetfim.errors import GateError, UsgsStageError
from calumetfim.usgs import require_published_gridid


def shapefile_path(extract_root: Path) -> Path:
    path = extract_root / USGS_SHP_REL
    if not path.is_file():
        raise UsgsStageError(f"library polygon missing: {path}")
    return path


def rasterize_gridid(
    extract_root: Path,
    grid_id: int,
    *,
    transform,
    height: int,
    width: int,
    drain: np.ndarray,
) -> np.ndarray:
    import fiona
    from rasterio.features import rasterize
    from rasterio.warp import transform_geom

    gid = require_published_gridid(grid_id)
    shp = shapefile_path(extract_root)
    geoms: list = []
    with fiona.open(shp) as src:
        src_crs = src.crs or "EPSG:4269"
        for feat in src:
            props = feat.get("properties") or {}
            try:
                rec_id = int(float(props.get("GRIDID")))
            except (TypeError, ValueError):
                continue
            if rec_id != gid:
                continue
            geom = feat.get("geometry")
            if not geom:
                continue
            geoms.append(
                transform_geom(src_crs, f"EPSG:{TEMPLATE_CRS}", geom, precision=6)
            )
    if not geoms:
        raise UsgsStageError(f"GRIDID {gid} missing from {shp}")
    arr = rasterize(
        ((g, 1) for g in geoms),
        out_shape=(int(height), int(width)),
        transform=transform,
        fill=0,
        dtype="uint8",
        all_touched=False,
    )
    mask = np.asarray(drain, dtype=bool)
    if arr.shape != mask.shape:
        raise GateError(f"rasterize shape {arr.shape} != drain {mask.shape}")
    return np.where(mask, arr, WET_NODATA).astype(np.uint8)
