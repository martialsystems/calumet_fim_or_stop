# Copyright (c) 2026 Martial Systems LLC

import numpy as np
import pytest

from calumetfim.errors import GateError
from calumetfim.physics import munster_delta_m, paint_wet
from calumetfim.usgs import pin_pairs


def test_delta_uses_wse_not_stage() -> None:
    pairs = pin_pairs()
    elev = float(pairs["flood"]["munster_elev_ft"])
    delta = munster_delta_m(munster_elev_ft=elev, h_channel_m=180.0)
    assert delta == pytest.approx(elev * 0.3048 - 180.0)
    with pytest.raises(GateError):
        paint_wet(
            np.zeros((4, 4)),
            delta_m=delta,
            drain_to_reach=np.ones((4, 4), dtype=bool),
            h_channel_locked=False,
        )
