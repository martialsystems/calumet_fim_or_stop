# Copyright (c) 2026 Martial Systems LLC
"""Read-only Calumet HAND and calibrated P. Freeze a7dcd81 / 3a5dcfd."""

from __future__ import annotations

import hashlib
from pathlib import Path

from calumetfim.config import (
    CALUMET_INTERIM,
    LOCKED_BAND_SHA256,
    LOCKED_TRANSFORM_SHA256,
    TEMPLATE_CRS,
    TEMPLATE_RES_M,
    TEMPLATE_SHAPE,
)
from calumetfim.errors import SiblingShaError


def transform_sha256_from_raster(path: Path) -> str:
    import rasterio

    with rasterio.open(path) as src:
        t = src.transform
        payload = (
            f"{int(src.crs.to_epsg() or 0)}|{src.width}|{src.height}|"
            f"{t.a},{t.b},{t.c},{t.d},{t.e},{t.f}"
        )
    return hashlib.sha256(payload.encode("ascii")).hexdigest()


def band_sha256_from_raster(path: Path) -> str:
    import rasterio

    with rasterio.open(path) as src:
        return hashlib.sha256(src.read(1).tobytes()).hexdigest()


def require_band_sha(path: Path, *, expected: str) -> str:
    if not path.is_file():
        raise SiblingShaError(f"sibling raster missing: {path}")
    got = band_sha256_from_raster(path)
    if got != expected:
        raise SiblingShaError(f"band {got} != locked {expected} ({path})")
    return got


def calumet_paths(root: Path | None = None) -> dict[str, Path]:
    if root is None:
        interim = CALUMET_INTERIM
    else:
        interim = Path(root) / "data" / "interim"
    return {
        "hand": interim / "hand.tif",
        "p_calibrated": interim / "p_sfha_calibrated.tif",
        "zone_class": interim / "zone_class.tif",
        "dem": interim / "dem.tif",
    }


def require_template(path: Path) -> str:
    import rasterio

    with rasterio.open(path) as src:
        if int(src.crs.to_epsg() or 0) != TEMPLATE_CRS:
            raise SiblingShaError(f"CRS {src.crs} is not EPSG:{TEMPLATE_CRS}")
        if abs(src.transform.a - TEMPLATE_RES_M) > 1e-6 or abs(src.transform.e + TEMPLATE_RES_M) > 1e-6:
            raise SiblingShaError(f"cell size is not {TEMPLATE_RES_M} m: {src.transform}")
        if (src.height, src.width) != TEMPLATE_SHAPE:
            raise SiblingShaError(
                f"shape {(src.height, src.width)} is not locked {TEMPLATE_SHAPE}"
            )
    got = transform_sha256_from_raster(path)
    if got != LOCKED_TRANSFORM_SHA256:
        raise SiblingShaError(f"transform {got} != locked {LOCKED_TRANSFORM_SHA256}")
    return got


def require_live_siblings(*, calumet_root: Path | None = None) -> dict[str, str]:
    paths = calumet_paths(calumet_root)
    out: dict[str, str] = {}
    for key, expected in LOCKED_BAND_SHA256.items():
        out[key] = require_band_sha(paths[key], expected=expected)
    out["transform"] = require_template(paths["hand"])
    return out
