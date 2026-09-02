# Copyright (c) 2026 Martial Systems LLC
"""Stage 0 identity: GIS must be Dunn/Straub/Manaster 2020. No substitute study."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from calumetfim.config import (
    AUTHOR_SURNAMES,
    DATA_DOI,
    GAGE_MUNSTER,
    GAGE_SOUTH_HOLLAND,
    GAGE_THORN,
    N_PUBLISHED_PROFILES,
    PUBLISHED_PROFILES,
    REFUSED_SUBSTITUTES,
    SIR,
    STUDY_TITLE_FRAGMENT,
    USGS_BREACH_REL,
    USGS_SHP_REL,
    USGS_ZIP_NAME,
    YEAR,
)
from calumetfim.errors import SubstituteError, WrongStudyError
from calumetfim.usgs import profile_by_gridid

_DBF_HEADER = 32
_FIELD_WIDTH = 32


def refuse_substitute(text: str, *, source: str) -> None:
    blob = text or ""
    lower = blob.lower()
    for marker in REFUSED_SUBSTITUTES:
        if marker.lower() in lower:
            raise SubstituteError(
                f"{source}: {marker} is not SIR {SIR}. Do not fall through "
                "to Grand Calumet bathymetry or INFIP."
            )


def _require_surnames(blob: str, *, source: str) -> None:
    for name in AUTHOR_SURNAMES:
        if name not in blob:
            raise WrongStudyError(f"{source}: missing author {name}")


def prove_sciencebase_item(item: dict[str, Any]) -> dict[str, str]:
    title = str(item.get("title") or "")
    citation = str(item.get("citation") or "")
    summary = str(item.get("summary") or "")
    links = " ".join(
        f"{x.get('uri') or ''} {x.get('title') or ''}"
        for x in (item.get("webLinks") or [])
    )
    blob = "\n".join([title, citation, summary, links, json.dumps(item, default=str)])
    refuse_substitute(blob, source="sciencebase")
    if STUDY_TITLE_FRAGMENT not in title:
        raise WrongStudyError(f"ScienceBase title is not {STUDY_TITLE_FRAGMENT}: {title}")
    _require_surnames(blob, source="sciencebase")
    if str(YEAR) not in citation and str(YEAR) not in title:
        raise WrongStudyError("ScienceBase citation is not 2020")
    if DATA_DOI not in blob:
        raise WrongStudyError(f"ScienceBase missing data DOI {DATA_DOI}")
    if SIR not in blob and "sir20205074" not in blob.lower():
        raise WrongStudyError(f"ScienceBase missing SIR {SIR}")
    for gage in (GAGE_MUNSTER, GAGE_SOUTH_HOLLAND, GAGE_THORN):
        if gage not in blob:
            raise WrongStudyError(f"ScienceBase missing gage {gage}")
    names = [str(f.get("name") or "") for f in (item.get("files") or [])]
    if USGS_ZIP_NAME not in names:
        raise WrongStudyError(f"ScienceBase files {names} missing {USGS_ZIP_NAME}")
    return {
        "title": title,
        "citation": citation,
        "zip_name": USGS_ZIP_NAME,
        "sir": SIR,
        "data_doi": DATA_DOI,
    }


def prove_fgdc_metadata(xml_text: str) -> None:
    blob = xml_text or ""
    refuse_substitute(blob, source="fgdc")
    if STUDY_TITLE_FRAGMENT not in blob:
        raise WrongStudyError("FGDC metadata is not the Lansing to South Holland study")
    _require_surnames(blob, source="fgdc")
    if SIR not in blob:
        raise WrongStudyError(f"FGDC metadata missing SIR {SIR}")
    if DATA_DOI not in blob:
        raise WrongStudyError(f"FGDC metadata missing {DATA_DOI}")
    for gage in (GAGE_MUNSTER, GAGE_SOUTH_HOLLAND, GAGE_THORN):
        if gage not in blob:
            raise WrongStudyError(f"FGDC metadata missing gage {gage}")


def _read_dbf_records(dbf_path: Path) -> list[dict[str, str]]:
    data = dbf_path.read_bytes()
    if len(data) < 32:
        raise WrongStudyError(f"DBF too small: {dbf_path}")
    n = int.from_bytes(data[4:8], "little")
    hlen = int.from_bytes(data[8:10], "little")
    rlen = int.from_bytes(data[10:12], "little")
    fields: list[tuple[str, int]] = []
    off = _DBF_HEADER
    while off < hlen - 1:
        raw = data[off : off + _FIELD_WIDTH]
        if raw[0] == 0x0D:
            break
        name = raw[0:11].split(b"\x00", 1)[0].decode("latin1")
        length = raw[16]
        fields.append((name, length))
        off += _FIELD_WIDTH
    rows: list[dict[str, str]] = []
    pos = hlen
    for _ in range(n):
        rec = data[pos : pos + rlen]
        pos += rlen
        cur = 1
        vals: dict[str, str] = {}
        for name, length in fields:
            vals[name] = rec[cur : cur + length].decode("latin1", errors="replace").strip()
            cur += length
        rows.append(vals)
    return rows


def prove_shapefile_dbf(extract_root: Path) -> list[dict[str, str]]:
    shp = extract_root / USGS_SHP_REL
    dbf = shp.with_suffix(".dbf")
    if not dbf.is_file():
        raise WrongStudyError(f"library shapefile missing: {shp}")
    breach = extract_root / USGS_BREACH_REL
    if not shp.is_file():
        raise WrongStudyError(f"library polygon missing: {shp}")
    rows = _read_dbf_records(dbf)
    if len(rows) != N_PUBLISHED_PROFILES:
        raise WrongStudyError(
            f"{dbf} has {len(rows)} records, not {N_PUBLISHED_PROFILES}"
        )
    gids: set[int] = set()
    for rec in rows:
        if rec.get("USGSID_1") != GAGE_SOUTH_HOLLAND:
            raise WrongStudyError(
                f"USGSID_1 {rec.get('USGSID_1')} is not {GAGE_SOUTH_HOLLAND}"
            )
        if rec.get("USGSID_2") != GAGE_MUNSTER:
            raise WrongStudyError(f"USGSID_2 {rec.get('USGSID_2')} is not {GAGE_MUNSTER}")
        gid = int(float(rec["GRIDID"]))
        gids.add(gid)
        pinned = profile_by_gridid(gid)
        stage1 = float(rec["STAGE_1"])
        stage2 = float(rec["STAGE_2"])
        if abs(stage1 - pinned[1]) > 0.01 or abs(stage2 - pinned[3]) > 0.01:
            raise WrongStudyError(
                f"GRIDID {gid} stages {stage1}/{stage2} do not match Table 2 "
                f"{pinned[1]}/{pinned[3]}"
            )
    if gids != set(range(1, N_PUBLISHED_PROFILES + 1)):
        raise WrongStudyError(f"GRIDID set {sorted(gids)} is not 1..24")
    if not breach.is_file():
        # Breach file is extra uncertainty, not required for identity, but the
        # compare must not silently use it as the library polygon.
        pass
    return rows


def prove_zip_name(zip_path: Path) -> None:
    if zip_path.name != USGS_ZIP_NAME:
        raise WrongStudyError(
            f"zip {zip_path.name} is not {USGS_ZIP_NAME}. Fetch-or-stop."
        )
    refuse_substitute(zip_path.name, source="zip_name")
