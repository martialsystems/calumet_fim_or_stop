# Calumet FIM or stop

Does the Calumet HAND bathtub, or P(sfha | hydro) >= t, sit in the same neighborhood as USGS SIR 2020-5074 on a Munster to South Holland window?

SIR 2020-5074 is Dunn/Straub/Manaster 2020, 24 published profiles, gages 05536195 and 05536290. Those gages are HUC 07120003. Frozen HAND a7dcd81 is HUC 04040001. Finite HAND cells on the Munster to South Holland window: 0. Stop. Stage A `e11fce4`.

Stage 0 proved the GIS (`lcalumeil_shapefile.zip`, data DOI 10.5066/P99L14DN). NWS SHLI2 minor flood 16.00 ft is not a paint surface: GRIDID 11 is 16.32 ft. Frozen calibrated P is `3a5dcfd`. The 8-mile library runs from 0.4 mile downstream of Munster toward South Holland.

Little Calumet in the SIR title is the Lansing to South Holland reach in HUC 07120003, not the Galien HUC 04040001 that was trained. USS Gary is east of that clip, on 04040001. Live WBD at the two gages is Chicago 07120003 (1,590.16 km²). Do not restamp Calumet D. Do not freeze a 07120003 HAND just to finish this IoU.

P(sfha | hydro) is map-completion, not water at 16.32 ft. The HAND mask is a 30 m bathtub. The USGS polygon is not a FIRM.

[![Calumet floodplain completion](https://img.shields.io/badge/Calumet_floodplain_completion-2e7d32?style=for-the-badge)](https://github.com/martialsystems/calumet_flood_completion) (`a7dcd81` HAND, `3a5dcfd` calibrated P). [![Open the research console](https://img.shields.io/badge/Open_the_research_console-2e7d32?style=for-the-badge)](https://martialsystems.github.io/indiana_wx_pages/)

| Quantity | Value |
|----------|------:|
| SIR | 2020-5074 |
| Published profiles | 24 |
| Pinned flood GRIDID | 11 (South Holland 16.32 ft / Munster 14.66 ft) |
| Pinned high GRIDID | 24 (South Holland 24.32 ft / Munster 19.66 ft) |
| NWS minor vs GRIDID 11 | 0.32 ft |
| Library HUC-8 | 07120003 |
| HAND HUC-8 | 04040001 |
| Finite HAND cells on window | 0 |

## Stage 0

Identity is ScienceBase item `5ec58ae882ce476925ebbbf5` plus the shapefile DBF. Fetch-or-stop if the zip is not `lcalumeil_shapefile.zip`. Stage A clips the frozen 04040001 template to the ScienceBase bbox and counts finite HAND. Empty overlap is the stop.

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=src:. python3 scripts/run_fixture.py logs/stage0_fixture
.venv/bin/python -m pytest tests -q
PYTHONPATH=src:. python3 scripts/run_live.py logs/live
```

Live exit 2 is the empty-overlap stop. Do not use stock `/usr/bin/python3 -m pytest`.

| File | Role |
|------|------|
| [METHODOLOGY.md](METHODOLOGY.md) | Locked contract |
| [AGENTS.md](AGENTS.md) | Agent rules |
| [CHECKLIST.md](CHECKLIST.md) | Operator list |
| `src/calumetfim/` | Study pin, published profiles, window clip, claims |
| `calfimforge/` | GraphForge pin: five refuse laws |

MIT. Martial Systems LLC.
