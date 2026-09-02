# Copyright (c) 2026 Martial Systems LLC

import json
from pathlib import Path

import pytest

from calumetfim.config import DATA_DOI, SIR, STUDY_TITLE_FRAGMENT, USGS_ZIP_NAME
from calumetfim.errors import SubstituteError, WrongStudyError
from calumetfim.study import (
    prove_fgdc_metadata,
    prove_sciencebase_item,
    prove_zip_name,
    refuse_substitute,
)

FX = Path(__file__).resolve().parent / "fixtures"


def test_sciencebase_and_fgdc_are_dunn_straub_manaster() -> None:
    item = json.loads((FX / "sciencebase_item.json").read_text(encoding="utf-8"))
    ident = prove_sciencebase_item(item)
    assert STUDY_TITLE_FRAGMENT in ident["title"]
    assert ident["zip_name"] == USGS_ZIP_NAME
    assert ident["sir"] == SIR
    assert ident["data_doi"] == DATA_DOI
    prove_fgdc_metadata((FX / "FIMI_shapefile_metadata_lcalumeil.xml").read_text())


def test_refuse_grand_cal_and_infip() -> None:
    with pytest.raises(SubstituteError):
        refuse_substitute("use Grand Calumet bathymetry instead", source="t")
    with pytest.raises(SubstituteError):
        refuse_substitute("fall through to INFIP polygons", source="t")
    bad = {
        "title": "Bathymetry of the Grand Calumet River, Indiana-Illinois, 2017",
        "citation": "not Dunn",
        "files": [{"name": "grandcal.zip"}],
    }
    with pytest.raises(SubstituteError):
        prove_sciencebase_item(bad)


def test_wrong_zip_name_stops() -> None:
    with pytest.raises(WrongStudyError):
        prove_zip_name(Path("nori3_shapefiles.zip"))
    prove_zip_name(Path(USGS_ZIP_NAME))
