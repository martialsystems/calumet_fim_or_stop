# Operator checklist

1. Fixture Stage 0 green (`scripts/run_fixture.py`).
2. Calumet sibling rasters on disk; band sha matches `LOCKED_BAND_SHA256`.
3. ScienceBase zip is `lcalumeil_shapefile.zip`. DBF has 24 GRIDIDs. Authors Dunn/Straub/Manaster.
4. Live `scripts/run_live.py logs/live`. Exit 2 is empty HAND overlap.
5. README matches `logs/live/stage_a_report.json` (or the fixture JSON if live is not fetched).
6. Claim scan clean. No TRI five-row. No interpolated 16.00 ft.
7. Push public `martialsystems/calumet_fim_or_stop`.
8. Index gist `66b896b0` Maps / Calumet row: FIM library exists; window is the wrong HUC; stop.
9. `calfimforge/scripts/sanity_calfimforge.py`. Do not restamp Pages. Do not open `nwm_ana_2025_26`. Do not start a 07120003 HAND freeze here.
