# Agent notes: calumet_fim_or_stop

Public GitHub. MIT. Question: Does the Calumet HAND bathtub, or P(sfha | hydro) >= t, sit in the same neighborhood as USGS SIR 2020-5074 on a Munster to South Holland window?

Stage 0 must prove Dunn/Straub/Manaster 2020. Fetch-or-stop if the zip is the wrong study. Pin published GRIDIDs only. Do not interpolate NWS 16.00 ft. Clip to the Munster to South Holland library bbox, not the whole HUC. Freeze Calumet HAND `a7dcd81` and calibrated P `3a5dcfd`. No TRI five-row. No Grand Calumet bathymetry. No INFIP. Do not restamp `calumet_flood_completion` Stage D. Do not open `nwm_ana_2025_26` in the same sitting. Do not restamp Pages.

Empty HAND overlap on that window is a stop, not a substitute study.

## Verify

`python3 ~/agent_laws_verify_before_done/vbd_gate.py check --app-root . --claim-done`

`vbd.runtime.json` runs `.venv/bin/python -m pytest` and `scripts/run_fixture.py`. Do not use stock `/usr/bin/python3 -m pytest`.
