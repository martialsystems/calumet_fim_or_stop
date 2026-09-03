# Copyright (c) 2026 Martial Systems LLC

from pathlib import Path

from calumetfim.claims import scan_text
from calumetfim.config import PARENT_HAND_SHA, PARENT_P_SHA, QUESTION, SIR

REPO = Path(__file__).resolve().parents[1]


def test_readme_opens_with_the_question() -> None:
    text = (REPO / "README.md").read_text(encoding="utf-8")
    body = "\n".join(text.splitlines()[1:]).lstrip()
    assert body.startswith(QUESTION)
    assert SIR in text
    assert "Dunn" in text and "Straub" in text and "Manaster" in text
    assert "05536195" in text
    assert "05536290" in text
    assert "07120003" in text
    assert "04040001" in text
    assert PARENT_HAND_SHA in text
    assert PARENT_P_SHA in text
    assert "lcalumeil_shapefile.zip" in text
    assert "16.32" in text
    assert "Research index: https://gist.github.com/martialsystems/66b896b0a4a0b8cba2b478aef64312f3" in text
    assert "Open_the_research_console" not in text
    assert "66b896b0a4a0b8cba2b478aef64312f3" in text
    assert "Calumet floodplain completion" in text
    assert "calumet__flood__completion" not in text
    assert "Parent: [![" not in text
    assert "nwm_ana_2025_26" not in text
    assert scan_text(text) == []
    assert "\u2014" not in text
    assert "What it is not" not in text
    for name in ("METHODOLOGY.md", "AGENTS.md", "CHECKLIST.md"):
        other = (REPO / name).read_text(encoding="utf-8")
        assert "\u2014" not in other
        assert "What it is not" not in other
