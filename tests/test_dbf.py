# Copyright (c) 2026 Martial Systems LLC

from pathlib import Path

from calumetfim.study import prove_shapefile_dbf


def test_dbf_matches_table_2(tmp_path: Path) -> None:
    shp_dir = tmp_path / "lcalumeil"
    shp_dir.mkdir()
    src = Path(__file__).resolve().parent / "fixtures" / "lcalumeil.dbf"
    (shp_dir / "lcalumeil.dbf").write_bytes(src.read_bytes())
    (shp_dir / "lcalumeil.shp").write_bytes(b"SHP")
    rows = prove_shapefile_dbf(tmp_path)
    assert len(rows) == 24
    assert {int(float(r["GRIDID"])) for r in rows} == set(range(1, 25))
