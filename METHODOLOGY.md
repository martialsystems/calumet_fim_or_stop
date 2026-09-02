# Methodology: Calumet HAND vs USGS SIR 2020-5074

Locked contract for `calumet_fim_or_stop`. Freeze Calumet HAND and calibrated P. Do not recompute HAND. Do not train. Do not paint a HUC. Science `e11fce4`. GraphForge pin `calfimforge/` holds five refuse laws.

## Reach and window

USGS 05536195 Little Calumet River at Munster, IN and 05536290 Little Calumet River at South Holland, IL. SIR 2020-5074 (Dunn, Straub, and Manaster 2020) maps about 8 miles from 0.4 mile downstream of Munster to 0.5 mile downstream of South Holland. Thorn Creek 05536275 is in the same study. The clip is the ScienceBase bounding box of that library (lon -87.6128 to -87.5204, lat 41.5621 to 41.6244), not USS Gary and not whole HUC 04040001.

Live WBD at both gages is HUC-8 07120003 Chicago. Frozen HAND is HUC-8 04040001 Little Calumet-Galien (`a7dcd81`). Scores are that clip only.

## Library

GIS source: ScienceBase item `5ec58ae882ce476925ebbbf5`, zip `lcalumeil_shapefile.zip`, data DOI 10.5066/P99L14DN. FGDC metadata must name Dunn, Straub, Manaster, SIR 2020-5074, and the three gages. The shapefile DBF has 24 records, USGSID_1 05536290, USGSID_2 05536195, GRIDID 1 to 24 matching Table 2 of the SIR. The breach shapefile is levee-uncertainty, not the library polygon.

Published profiles only. NWS SHLI2 minor flood is 16.00 ft. Nearest published South Holland stage is GRIDID 11 at 16.32 ft (gap 0.32 ft). GRIDID 24 is the high surface. Do not interpolate 16.00.

## Four layers (when the window has HAND)

| Layer | Rule |
|-------|------|
| FEMA SFHA | Calumet `zone_class.tif` floodway ∪ SFHA |
| Map-completion P | Calumet `p_sfha_calibrated.tif` >= 0.75 (`3a5dcfd`) |
| HAND wet | Frozen `hand.tif` (`a7dcd81`), `HAND < Δ`, `Δ = WSE - h_channel` at Munster |
| USGS library | GRIDID 11 and GRIDID 24 polygons from `lcalumeil.shp` |

Headline is containment: N of M USGS-wet cells that are also HAND-wet, plus the miss count, plus IoU on the window. P >= t is the same sentence. Empty P >= 0.75 is data on this lake-plain.

If finite HAND cells on the window are 0, stop. Do not fall through to Grand Calumet bathymetry or INFIP.

## Stages

0: study identity, published GRIDID pin, fixture path.
A: fetch zip, prove DBF, clip window, count frozen HAND.

A refuses a missing or wrong zip. Empty overlap is exit 2.

## Claims

Allowed: HAND bathtub vs USGS SIR 2020-5074 on the Munster to South Holland window; nearest published GRIDID 11 / 24; mapped SFHA; calibrated P as a map layer; containment N of M plus miss; leftover-SFHA / extra unshaded X; IoU on that window; empty-overlap stop with the two HUCs named.

Banned: 100-year exceedance; P as a forecast; HAND as a FIRM; USGS library as a FIRM; site-level flood risk; casualty / climate / population-at-risk; TRI five-row; Indy plant names; interpolated stages; Grand Calumet bathymetry; INFIP; SIR 2011-5138 as this library; whole-HUC paint.

## Freeze

Calumet band sha256 for `hand`, `p_calibrated`, and `zone_class` as `LOCKED_BAND_SHA256`. Transform sha256 `81748d41…`. Do not rewrite Calumet Stage D.
