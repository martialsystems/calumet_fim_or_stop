# Copyright (c) 2026 Martial Systems LLC

from pathlib import Path

from calumetfim.config import FLOOD_GRIDID, GAGE_MUNSTER, QUESTION, SIR
from calumetfim.pipeline import stage0_fixture


def test_fixture_stage0(tmp_path: Path) -> None:
    report = stage0_fixture(tmp_path)
    assert report["gage_id"] == GAGE_MUNSTER
    assert report["sir"] == SIR
    assert report["question"] == QUESTION
    assert report["pairs"]["flood"]["grid_id"] == FLOOD_GRIDID
    assert report["huc8_library"] == "07120003"
    assert report["huc8_hand"] == "04040001"
    assert report["parent_hand_sha"] == "a7dcd81"
    assert report["parent_p_sha"] == "3a5dcfd"
    assert report["interpolated"] is False
    assert report["tri_five_row"] is False
    assert report["p_is_forecast"] is False
    assert (tmp_path / "four_wet.png").is_file()
    assert (tmp_path / "stage0_report.json").is_file()
