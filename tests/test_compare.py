# Copyright (c) 2026 Martial Systems LLC

import numpy as np
import pytest

from calumetfim.compare import leftover_sentence, overlap_table
from calumetfim.errors import EmptyOverlapError, GateError
from calumetfim.fixture import arrays, empty_overlap_arrays
from calumetfim.window import overlap_counts


def test_overlap_counts_and_refuses_huc_wide() -> None:
    blobs = arrays()
    t = overlap_table(
        wet=blobs["wet"],
        usgs=blobs["usgs"],
        zone=blobs["zone"],
        p_cal=blobs["p"],
        drain_to_reach=blobs["drain"],
    )
    assert t["p_is_forecast"] is False
    assert t["usgs_is_firm"] is False
    assert t["iou_universe"] == "munster_south_holland_window"
    assert int(t["n_hand_wet"]) > 0
    assert int(t["n_usgs_wet"]) > 0
    s = leftover_sentence(t)
    assert "USGS wet cells are HAND-wet" in s
    assert s.index("USGS wet cells are HAND-wet") < s.index("Leftover SFHA")
    with pytest.raises(GateError):
        overlap_table(
            wet=blobs["wet"],
            usgs=blobs["usgs"],
            zone=blobs["zone"],
            p_cal=blobs["p"],
            drain_to_reach=np.ones(blobs["wet"].shape, dtype=bool),
        )


def test_empty_window_is_a_stop() -> None:
    blobs = empty_overlap_arrays()
    counts = overlap_counts(np.full((16, 16), -9999.0), blobs["zone"], blobs["p"])
    assert counts["overlap_empty"] is True
    assert counts["n_hand_finite"] == 0
    with pytest.raises(EmptyOverlapError):
        overlap_table(
            wet=blobs["wet"],
            usgs=blobs["usgs"],
            zone=blobs["zone"],
            p_cal=blobs["p"],
            drain_to_reach=blobs["drain"],
        )
