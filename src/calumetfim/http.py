# Copyright (c) 2026 Martial Systems LLC
"""Fetch the ScienceBase SIR 2020-5074 shapefile zip. Fetch-or-stop."""

from __future__ import annotations

import json
import urllib.request
from pathlib import Path
from zipfile import ZipFile

from calumetfim.config import (
    SCIENCEBASE_ITEM_URL,
    USGS_METADATA_NAME,
    USGS_METADATA_URL,
    USGS_ZIP_NAME,
    USGS_ZIP_URL,
    USER_AGENT,
)
from calumetfim.errors import FetchError, WrongStudyError
from calumetfim.study import prove_zip_name, refuse_substitute


def _get(url: str, dest: Path, *, min_bytes: int) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.is_file() and dest.stat().st_size >= min_bytes:
        return dest
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            dest.write_bytes(resp.read())
    except Exception as exc:  # noqa: BLE001
        raise FetchError(f"library download failed: {url}: {exc}") from exc
    if dest.stat().st_size < min_bytes:
        raise FetchError(f"download too small ({dest.stat().st_size} bytes): {url}")
    return dest


def fetch_item_json(dest_dir: Path) -> dict:
    dest = dest_dir / "sciencebase_item.json"
    _get(SCIENCEBASE_ITEM_URL + "?format=json", dest, min_bytes=500)
    item = json.loads(dest.read_text(encoding="utf-8"))
    refuse_substitute(json.dumps(item, default=str), source="sciencebase_live")
    return item


def fetch_fgdc(dest_dir: Path) -> Path:
    dest = dest_dir / USGS_METADATA_NAME
    return _get(USGS_METADATA_URL, dest, min_bytes=1000)


def fetch_zip(dest_dir: Path, *, url: str = USGS_ZIP_URL) -> Path:
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / USGS_ZIP_NAME
    prove_zip_name(dest if dest.is_file() else Path(USGS_ZIP_NAME))
    refuse_substitute(url, source="zip_url")
    return _get(url, dest, min_bytes=1_000_000)


def extract_zip(zip_path: Path, dest_dir: Path) -> Path:
    prove_zip_name(zip_path)
    dest_dir.mkdir(parents=True, exist_ok=True)
    with ZipFile(zip_path) as zf:
        names = zf.namelist()
        blob = " ".join(names)
        refuse_substitute(blob, source="zip_members")
        if "lcalumeil/lcalumeil.shp" not in names:
            raise WrongStudyError(
                f"{zip_path} is not lcalumeil/lcalumeil.shp ({names[:12]})"
            )
        zf.extractall(dest_dir)
    return dest_dir
