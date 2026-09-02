# Copyright (c) 2026 Martial Systems LLC
"""Stages 0 and A. Stop if the window has no frozen HAND. Do not skip."""

from __future__ import annotations

import json
from pathlib import Path

from calumetfim.claims import require_clean, require_paths_clean
from calumetfim.compare import leftover_sentence, overlap_table
from calumetfim.config import (
    FLOOD_GRIDID,
    GAGE_MUNSTER,
    HUC8_HAND,
    HUC8_LIBRARY,
    PARENT_HAND_SHA,
    PARENT_P_SHA,
    QUESTION,
    SIR,
    USGS_METADATA_NAME,
)
from calumetfim.errors import EmptyOverlapError
from calumetfim.figure import flood_copy, write_four_panel
from calumetfim.fixture import arrays
from calumetfim.http import extract_zip, fetch_fgdc, fetch_item_json, fetch_zip
from calumetfim.sibling import calumet_paths, require_live_siblings
from calumetfim.study import prove_fgdc_metadata, prove_sciencebase_item, prove_shapefile_dbf
from calumetfim.usgs import pin_pairs, require_published_gridid
from calumetfim.wbd import require_library_huc
from calumetfim.window import overlap_counts, read_window


def _write_json(path: Path, obj: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2) + "\n", encoding="utf-8")
    require_paths_clean([path])


def stage0_fixture(log_dir: Path, *, fixtures: Path | None = None) -> dict:
    require_published_gridid(FLOOD_GRIDID)
    pin = pin_pairs()
    hucs = require_library_huc(live=False)
    fx = fixtures or Path(__file__).resolve().parents[2] / "tests" / "fixtures"
    item = json.loads((fx / "sciencebase_item.json").read_text(encoding="utf-8"))
    identity = prove_sciencebase_item(item)
    prove_fgdc_metadata((fx / USGS_METADATA_NAME).read_text(encoding="utf-8"))
    blobs = arrays()
    table = overlap_table(
        wet=blobs["wet"],
        usgs=blobs["usgs"],
        zone=blobs["zone"],
        p_cal=blobs["p"],
        drain_to_reach=blobs["drain"],
    )
    sentence = leftover_sentence(table)
    require_clean(sentence, source="fixture_sentence")
    require_clean(QUESTION, source="question")
    log_dir.mkdir(parents=True, exist_ok=True)
    report = {
        "stage": "0",
        "question": QUESTION,
        "fixture": True,
        "gage_id": GAGE_MUNSTER,
        "sir": SIR,
        "authors": ["Dunn", "Straub", "Manaster"],
        "year": 2020,
        "huc8_hand": HUC8_HAND,
        "huc8_library": HUC8_LIBRARY,
        "parent_hand_sha": PARENT_HAND_SHA,
        "parent_p_sha": PARENT_P_SHA,
        "p_is_forecast": False,
        "hand_is_firm": False,
        "usgs_is_firm": False,
        "interpolated": False,
        "tri_five_row": False,
        "identity": identity,
        "wbd": hucs,
        "pairs": pin,
        "table": table,
        "leftover": sentence,
        "overlap_empty": False,
    }
    _write_json(log_dir / "stage0_report.json", report)
    title, sub, footer, hand_c, usgs_c = flood_copy(
        iou=float(table["iou_hand_usgs"]), leftover=sentence
    )
    write_four_panel(
        log_dir / "four_wet.png",
        wet=blobs["wet"],
        usgs=blobs["usgs"],
        zone=blobs["zone"],
        p_cal=blobs["p"],
        drain_to_reach=blobs["drain"],
        title=title,
        subtitle=sub,
        footer=footer,
        hand_caption=hand_c,
        usgs_caption=usgs_c,
    )
    return report


def run_live(
    log_dir: Path,
    *,
    raw_dir: Path,
    calumet_root: Path | None = None,
    fetch: bool = True,
) -> dict:
    require_published_gridid(FLOOD_GRIDID)
    pin = pin_pairs()
    log_dir.mkdir(parents=True, exist_ok=True)
    if fetch:
        item = fetch_item_json(raw_dir)
        identity = prove_sciencebase_item(item)
        zip_path = fetch_zip(raw_dir)
        extract_root = raw_dir / "extracted"
        extract_zip(zip_path, extract_root)
        meta = fetch_fgdc(raw_dir)
        prove_fgdc_metadata(meta.read_text(encoding="utf-8"))
        prove_shapefile_dbf(extract_root)
        wbd = require_library_huc(live=True)
    else:
        identity = {"title": "fixture-bypass"}
        wbd = require_library_huc(live=False)
        extract_root = raw_dir / "extracted"
        if (extract_root / "lcalumeil" / "lcalumeil.dbf").is_file():
            prove_shapefile_dbf(extract_root)

    bands = require_live_siblings(calumet_root=calumet_root)
    paths = calumet_paths(calumet_root)
    hand, profile, _win = read_window(paths["hand"])
    zone, _, _ = read_window(paths["zone_class"])
    p_cal, _, _ = read_window(paths["p_calibrated"])
    counts = overlap_counts(hand, zone, p_cal)
    stop_sentence = (
        f"SIR {SIR} is Dunn/Straub/Manaster 2020, 24 published profiles, "
        f"gages {GAGE_MUNSTER} and 05536290. Those gages are HUC "
        f"{HUC8_LIBRARY}. Frozen HAND {PARENT_HAND_SHA} is HUC {HUC8_HAND}. "
        f"Finite HAND cells on the Munster to South Holland window: "
        f"{counts['n_hand_finite']}. Stop."
    )
    require_clean(stop_sentence, source="stop_sentence")
    report = {
        "stage": "A",
        "question": QUESTION,
        "fixture": False,
        "gage_id": GAGE_MUNSTER,
        "sir": SIR,
        "authors": ["Dunn", "Straub", "Manaster"],
        "year": 2020,
        "huc8_hand": HUC8_HAND,
        "huc8_library": HUC8_LIBRARY,
        "parent_hand_sha": PARENT_HAND_SHA,
        "parent_p_sha": PARENT_P_SHA,
        "p_is_forecast": False,
        "hand_is_firm": False,
        "usgs_is_firm": False,
        "interpolated": False,
        "tri_five_row": False,
        "identity": identity,
        "wbd": wbd,
        "pairs": pin,
        "sibling_sha": bands,
        "window": counts,
        "overlap_empty": bool(counts["overlap_empty"]),
        "leftover": stop_sentence,
        "stopped": bool(counts["overlap_empty"]),
    }
    _write_json(log_dir / "stage_a_report.json", report)
    if counts["overlap_empty"]:
        raise EmptyOverlapError(stop_sentence)
    return report
