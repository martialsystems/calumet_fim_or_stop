# Copyright (c) 2026 Martial Systems LLC
"""WBD HUC-8 at the library gages. Record 07120003; do not relabel as 04040001."""

from __future__ import annotations

import json
import urllib.request
from typing import Any

from calumetfim.config import (
    GAGE_MUNSTER,
    GAGE_MUNSTER_LONLAT,
    GAGE_SOUTH_HOLLAND,
    GAGE_SOUTH_HOLLAND_LONLAT,
    HUC8_HAND,
    HUC8_LIBRARY,
    USER_AGENT,
    WBD_LAYER_URL,
)
from calumetfim.errors import FetchError, GateError


def query_huc8(lon: float, lat: float) -> dict[str, Any]:
    url = (
        f"{WBD_LAYER_URL}/query?geometry={lon},{lat}"
        "&geometryType=esriGeometryPoint&inSR=4269"
        "&spatialRel=esriSpatialRelIntersects"
        "&outFields=huc8,name,states,areasqkm&returnGeometry=false&f=json"
    )
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=45) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except Exception as exc:  # noqa: BLE001
        raise FetchError(f"WBD query failed: {url}: {exc}") from exc
    feats = payload.get("features") or []
    if not feats:
        raise FetchError(f"WBD returned no HUC-8 at {lon},{lat}")
    attrs = feats[0]["attributes"]
    return {
        "huc8": str(attrs.get("huc8") or ""),
        "name": str(attrs.get("name") or ""),
        "states": str(attrs.get("states") or ""),
        "areasqkm": attrs.get("areasqkm"),
    }


def require_library_huc(*, live: bool) -> dict[str, dict[str, Any]]:
    """Munster and South Holland are Chicago 07120003, not Calumet HAND HUC."""
    if not live:
        return {
            GAGE_MUNSTER: {
                "huc8": HUC8_LIBRARY,
                "name": "Chicago",
                "lonlat": GAGE_MUNSTER_LONLAT,
                "live": False,
            },
            GAGE_SOUTH_HOLLAND: {
                "huc8": HUC8_LIBRARY,
                "name": "Chicago",
                "lonlat": GAGE_SOUTH_HOLLAND_LONLAT,
                "live": False,
            },
        }
    out: dict[str, dict[str, Any]] = {}
    for gage, lonlat in (
        (GAGE_MUNSTER, GAGE_MUNSTER_LONLAT),
        (GAGE_SOUTH_HOLLAND, GAGE_SOUTH_HOLLAND_LONLAT),
    ):
        hit = query_huc8(lonlat[0], lonlat[1])
        if hit["huc8"] == HUC8_HAND:
            raise GateError(
                f"{gage} WBD is {HUC8_HAND}; the locked pin is {HUC8_LIBRARY}"
            )
        if hit["huc8"] != HUC8_LIBRARY:
            raise GateError(
                f"{gage} WBD HUC {hit['huc8']} is not locked {HUC8_LIBRARY}"
            )
        hit["lonlat"] = lonlat
        hit["live"] = True
        out[gage] = hit
    return out
