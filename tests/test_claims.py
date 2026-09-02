# Copyright (c) 2026 Martial Systems LLC

import pytest

from calumetfim.claims import require_clean, scan_text
from calumetfim.errors import ClaimBanError


def test_allowed_and_banned() -> None:
    assert scan_text(
        "HAND bathtub vs USGS SIR 2020-5074 on the Munster to South Holland window"
    ) == []
    assert "p_as_forecast" in scan_text("P(sfha | hydro) is a forecast")
    assert "hand_as_firm" in scan_text("HAND bathtub is a FIRM")
    assert "usgs_as_firm" in scan_text("USGS library polygon is a FIRM")
    assert "wrong_sir" in scan_text("compare to SIR 2011-5138")
    assert "nora_gage" in scan_text("gage 03351000")
    assert "infip_substitute" in scan_text("use INFIP as the library")
    assert "grand_cal_bathy" in scan_text("Grand Calumet bathymetry grids")
    assert "tri_five_row" in scan_text("Hammond Group window-max")
    assert "indy_plant_copy" in scan_text("THURSDAY POOLS on this overlay")
    with pytest.raises(ClaimBanError):
        require_clean("site-level flood risk", source="t")
