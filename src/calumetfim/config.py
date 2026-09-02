# Copyright (c) 2026 Martial Systems LLC
"""Locked Munster to South Holland compare. Do not expand to the whole HUC."""

from __future__ import annotations

from pathlib import Path

QUESTION = (
    "Does the Calumet HAND bathtub, or P(sfha | hydro) >= t, sit in the same "
    "neighborhood as USGS SIR 2020-5074 on a Munster to South Holland window?"
)
HUC8_HAND = "04040001"
HUC_NAME_HAND = "Little Calumet-Galien"
# Live WBD at the two library gages (2026-09-02).
HUC8_LIBRARY = "07120003"
HUC_NAME_LIBRARY = "Chicago"
PARENT_HUC8 = "05120201"

GAGE_MUNSTER = "05536195"
GAGE_SOUTH_HOLLAND = "05536290"
GAGE_THORN = "05536275"
GAGE_MUNSTER_NAME = "Little Calumet River at Munster, IN"
GAGE_SOUTH_HOLLAND_NAME = "Little Calumet River at South Holland, IL"
GAGE_MUNSTER_LONLAT = (-87.5222222, 41.5775)
GAGE_SOUTH_HOLLAND_LONLAT = (-87.5975833, 41.60702778)
# Table 1, SIR 2020-5074: NAVD88 gage datums.
DATUM_SOUTH_HOLLAND_FT = 574.68
DATUM_MUNSTER_FT = 580.34
DATUM_THORN_FT = 586.11

SIR = "2020-5074"
SIR_URL = "https://doi.org/10.3133/sir20205074"
DATA_DOI = "10.5066/P99L14DN"
DATA_DOI_URL = "https://doi.org/10.5066/P99L14DN"
AUTHORS = ("Dunn, A.P.", "Straub, T.D.", "Manaster, A.E.")
AUTHOR_SURNAMES = ("Dunn", "Straub", "Manaster")
YEAR = 2020
STUDY_TITLE_FRAGMENT = "Little Calumet River from Lansing to South Holland"
SCIENCEBASE_ITEM = "5ec58ae882ce476925ebbbf5"
SCIENCEBASE_ITEM_URL = (
    "https://www.sciencebase.gov/catalog/item/5ec58ae882ce476925ebbbf5"
)
USGS_ZIP_NAME = "lcalumeil_shapefile.zip"
USGS_ZIP_URL = (
    "https://www.sciencebase.gov/catalog/file/get/5ec58ae882ce476925ebbbf5"
    "?f=__disk__90%2F46%2F7a%2F90467a38732a336e114f5e00e6bbabd004c68e67"
)
USGS_METADATA_NAME = "FIMI_shapefile_metadata_lcalumeil.xml"
USGS_METADATA_URL = (
    "https://www.sciencebase.gov/catalog/file/get/5ec58ae882ce476925ebbbf5"
    "?f=__disk__93%2Fd8%2F31%2F93d8318d2967d6fa3e9b28f7a83d10ee6ce20e79"
)
USGS_SHP_REL = Path("lcalumeil") / "lcalumeil.shp"
USGS_BREACH_REL = Path("lcalumeil_breach") / "lcalumeil_breach.shp"
# ScienceBase bounding box of the 8-mile library. Not USS Gary.
WINDOW_LONLAT = (-87.6128, 41.5621, -87.5204, 41.6244)
N_PUBLISHED_PROFILES = 24
# grid_id, SH stage ft, SH elev ft, Munster stage ft, Munster elev ft, PROFILE
PUBLISHED_PROFILES: tuple[tuple[int, float, float, float, float, str], ...] = (
    (1, 10.32, 585.0, 8.66, 589.0, "2p01_il"),
    (2, 11.32, 586.0, 9.66, 590.0, "5p01_il"),
    (3, 12.32, 587.0, 10.66, 591.0, "5p02_il"),
    (4, 12.32, 587.0, 11.66, 592.0, "2p04_il"),
    (5, 13.32, 588.0, 11.66, 592.0, "2p02_il"),
    (6, 14.32, 589.0, 11.66, 592.0, "2p03_il"),
    (7, 14.32, 589.0, 12.66, 593.0, "5p03_il"),
    (8, 14.32, 589.0, 13.66, 594.0, "10p01_il"),
    (9, 15.32, 590.0, 13.66, 594.0, "10p02_il"),
    (10, 15.32, 590.0, 14.66, 595.0, "100p01_il"),
    (11, 16.32, 591.0, 14.66, 595.0, "25p01_il"),
    (12, 16.32, 591.0, 15.66, 596.0, "50p01_il"),
    (13, 17.32, 592.0, 14.66, 595.0, "50p04_il"),
    (14, 17.32, 592.0, 15.66, 596.0, "50p02_il"),
    (15, 17.32, 592.0, 16.66, 597.0, "500p03_il"),
    (16, 18.32, 593.0, 15.66, 596.0, "50p03_il"),
    (17, 18.32, 593.0, 16.66, 597.0, "100p02_il"),
    (18, 19.32, 594.0, 17.66, 598.0, "500p04_il"),
    (19, 20.32, 595.0, 16.66, 597.0, "100p03_il"),
    (20, 20.32, 595.0, 17.66, 598.0, "500p05_il"),
    (21, 21.32, 596.0, 17.66, 598.0, "500p09_il"),
    (22, 22.32, 597.0, 18.66, 599.0, "500p10_il"),
    (23, 23.32, 598.0, 18.66, 599.0, "500p11_il"),
    (24, 24.32, 599.0, 19.66, 600.0, "500p12_il"),
)
# NWS SHLI2 minor flood is 16.00 ft. Nearest published South Holland stage is 16.32.
# Do not interpolate 16.00. Pin GRIDID 11 (and GRIDID 24 as the high surface).
FLOOD_GRIDID = 11
HIGH_GRIDID = 24
NWS_MINOR_STAGE_FT = 16.0
FLOOD_STAGE_GAP_FT = 0.32

PARENT_HAND_SHA = "a7dcd81"
PARENT_P_SHA = "3a5dcfd"
PARENT_HAND_SHA_FULL = "a7dcd819a4ab38e5c4cb727d84ae9db28aa546cc"
PARENT_P_SHA_FULL = "3a5dcfdca42a9ff7750d56635b4a9231728689b8"
CALUMET_DEFAULT = Path.home() / "calumet_flood_completion"
CALUMET_INTERIM = CALUMET_DEFAULT / "data" / "interim"

TEMPLATE_CRS = 5070
TEMPLATE_RES_M = 30.0
TEMPLATE_KIND = "nlcd_2021"
TEMPLATE_SHAPE = (3008, 3298)
HYDRO_NODATA = -9999.0
ZONE_NODATA = 255
WET_NODATA = 255
WET_DRY = 0
WET_WET = 1
FT_TO_M = 0.3048
P_HEADLINE_T = 0.75
P_DEFINITION = "P(sfha | hydro)"
P_SFHA_NODATA = -1.0

LOCKED_TRANSFORM_SHA256 = (
    "81748d4137cb2e161f4e875699d62a5b594a4141b5b6dc73eacd2af136d7e808"
)
LOCKED_BAND_SHA256 = {
    "hand": "8e70530e68589892c9779e505ced1cc249ccced91938fbfc8883b26f6607d3dc",
    "p_calibrated": "ee14fa6c47f0f5a475650430de87d261f45deac51540017c6927b99cf1dd9f55",
    "zone_class": "36f293d85250b651672f91b5472a3c98769af1541a49765d8dd235aa45086584",
}

ZONE_UNMAPPED = 0
ZONE_SFHA = 1
ZONE_FLOODWAY = 2
ZONE_SHADED_X = 3
ZONE_UNSHADED_X = 4
SFHA_CODES = frozenset({ZONE_SFHA, ZONE_FLOODWAY})

USER_AGENT = "MartialSystemsResearch/calumet_fim_or_stop"
INDEX_GIST = "https://gist.github.com/martialsystems/66b896b0a4a0b8cba2b478aef64312f3"
MAPS_GIST = "https://gist.github.com/martialsystems/16584e78d079666f7e8994b4cc6158be"
PARENT_REPO = "https://github.com/martialsystems/calumet_flood_completion"
WBD_LAYER_URL = "https://hydro.nationalmap.gov/arcgis/rest/services/wbd/MapServer/4"

REFUSED_SIR = "2011-5138"
REFUSED_GAGE_NORA = "03351000"
REFUSED_SUBSTITUTES = (
    "INFIP",
    "Indiana Floodplain Information Portal",
    "Grand Calumet bathymetry",
    "grandcal",
    "nori3_shapefiles",
    "SIR 2011-5138",
    "2011-5138",
)
INDY_PLANT_NAMES = (
    "THURSDAY POOLS",
    "FGF LLC",
    "ROYAL SPA CORP",
    "LINDE GAS & EQUIPMENT",
    "MAGNA POWERTRAIN EAST",
)
TRI_FIVE_MARKERS = (
    "Hammond Group",
    "expected pounds",
    "d1.csv",
    "five Zone X",
)

FIXTURE_WEST = 694_000.0
FIXTURE_NORTH = 2_098_000.0
FIXTURE_ROWS = 16
FIXTURE_COLS = 16

REPO_ROOT = Path(__file__).resolve().parents[2]
