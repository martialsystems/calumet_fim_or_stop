# Copyright (c) 2026 Martial Systems LLC
"""Fail closed: P is map-completion, HAND is not a FIRM, no TRI five-row."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable

from calumetfim.config import INDY_PLANT_NAMES, TRI_FIVE_MARKERS
from calumetfim.errors import ClaimBanError

_BANS: tuple[tuple[str, re.Pattern[str]], ...] = (
    (
        "casualty_count",
        re.compile(r"\b(deaths?|fatalit(?:y|ies)|casualt(?:y|ies)|killed)\b", re.I),
    ),
    (
        "climate_attribution",
        re.compile(r"\b(cmip\d*|downscal(?:e|ed|ing)|gcm)\b", re.I),
    ),
    (
        "population_at_risk",
        re.compile(r"\b(lives|people|population)\s+at\s+risk\b", re.I),
    ),
    (
        "p_as_100yr",
        re.compile(r"\b100-year\s+exceedance\b", re.I),
    ),
    (
        "p_as_forecast",
        re.compile(
            r"\bP\(sfha\s*\|\s*hydro\)\s+is\s+(?:a\s+)?(?:flood\s+)?forecast\b|"
            r"\bcalibrated P predicts\b",
            re.I,
        ),
    ),
    (
        "hand_as_firm",
        re.compile(r"\bHAND (?:mask|wet(?: area)?|bathtub) is (?:a |the )?FIRM\b", re.I),
    ),
    (
        "usgs_as_firm",
        re.compile(
            r"\b(?:USGS library|SIR 2020(?:–|-)?5074) (?:map|polygon|library) is (?:a |the )?FIRM\b",
            re.I,
        ),
    ),
    (
        "site_level_flood_risk",
        re.compile(r"\bsite-level flood risk\b", re.I),
    ),
    (
        "wrong_sir",
        re.compile(r"\bSIR 2011(?:–|-)?5138\b", re.I),
    ),
    (
        "nora_gage",
        re.compile(r"\b03351000\b"),
    ),
    (
        "infip_substitute",
        re.compile(r"\bINFIP\b|\bIndiana Floodplain Information Portal\b", re.I),
    ),
    (
        "grand_cal_bathy",
        re.compile(r"\bGrand Calumet bathymetr", re.I),
    ),
    (
        "interpolated_stage",
        re.compile(r"\binterpolat(?:e|ed|ing) (?:a |the )?(?:USGS |library )?stage\b", re.I),
    ),
)


def scan_text(text: str) -> list[str]:
    hits: list[str] = []
    blob = text or ""
    for name, pat in _BANS:
        if pat.search(blob):
            hits.append(name)
    lower = blob.lower()
    for plant in INDY_PLANT_NAMES:
        if plant.lower() in lower:
            hits.append("indy_plant_copy")
            break
    for marker in TRI_FIVE_MARKERS:
        if marker.lower() in lower:
            hits.append("tri_five_row")
            break
    if "\u2014" in blob:
        hits.append("em_dash")
    return hits


def require_clean(text: str, *, source: str) -> None:
    hits = scan_text(text)
    if hits:
        raise ClaimBanError(f"{source}: banned claims {hits}")


def require_paths_clean(paths: Iterable[Path]) -> None:
    for path in paths:
        if path.is_file():
            require_clean(path.read_text(encoding="utf-8"), source=str(path))
