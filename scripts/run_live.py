#!/usr/bin/env python3
# Copyright (c) 2026 Martial Systems LLC
"""Live identity + window overlap. Exit 2 if frozen HAND does not cover the library."""

from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(REPO), str(REPO / "src")]

from calumetfim.errors import EmptyOverlapError  # noqa: E402
from calumetfim.pipeline import run_live  # noqa: E402


def main() -> int:
    log_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else REPO / "logs" / "live"
    raw = REPO / "data" / "raw"
    try:
        report = run_live(log_dir, raw_dir=raw)
    except EmptyOverlapError as exc:
        print(str(exc))
        return 2
    print(report["leftover"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
