# Copyright (c) 2026 Martial Systems LLC


class GateError(RuntimeError):
    """Stage hard gate failed."""


class ClaimBanError(GateError):
    """Report text hit a banned claim."""


class SiblingShaError(GateError):
    """Frozen Calumet raster sha drifted."""


class UsgsStageError(GateError):
    """Requested library profile is interpolated, off-list, or the wrong gage."""


class FetchError(GateError):
    """ScienceBase library download failed."""


class WrongStudyError(GateError):
    """Zip or metadata is not Dunn/Straub/Manaster 2020 SIR 2020-5074."""


class SubstituteError(GateError):
    """Grand Calumet bathymetry, INFIP, or another study was offered as a fallback."""


class EmptyOverlapError(GateError):
    """Munster to South Holland window has no finite frozen HAND cells."""
