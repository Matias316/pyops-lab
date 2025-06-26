import pytest
from pathlib import Path
from .file_gap_checker import identify_gaps


def test_identify_missing_file(tmp_path: Path):
    filenames = [
        "upbcnv01_FO_EMAILREPORT_KPI_20250623_180000_last_30_minutes.csv",
        "upbcnv01_FO_EMAILREPORT_KPI_20250623_183000_last_30_minutes.csv",
        "upbcnv01_FO_EMAILREPORT_KPI_20250623_193000_last_30_minutes.csv",
    ]
    for name in filenames:
        (tmp_path / name).touch()

    missing = identify_gaps(
        str(tmp_path),
        example_filename="upbcnv01_FO_EMAILREPORT_KPI_20250612_223000_last_30_minutes.csv",
        step_in_mins=30,
    )
    assert missing == ["20250623_1900"]


def test_no_missing(tmp_path: Path):

    for hm in ["18:00", "18:30", "19:00", "19:30"]:
        hour, minute = hm.split(":")
        name = f"upbcnv01_FO_EMAILREPORT_KPI_20250623_{hour}{minute}00_last_30_minutes.csv"
        (tmp_path / name).touch()

    missing = identify_gaps(
        str(tmp_path),
        "upbcnv01_FO_EMAILREPORT_KPI_20250623_180000_last_30_minutes.csv",
        30,
    )
    assert missing == []


def test_invalid_step():
    with pytest.raises(ValueError) as valueErrorException:
        identify_gaps("/fake", "example_20250623_180000.csv", step_in_mins=10)
    assert str(valueErrorException.value) == "Only 15 and 30 minute steps are supported."


def test_no_matching_files(tmp_path: Path):
    filenames = [
        "upbcnv01_FO_EMAILREPORT_KPI_20250623_180000_last_30_minutes.csv",
        "upbcnv01_FO_EMAILREPORT_KPI_20250623_183000_last_30_minutes.csv",
        "upbcnv01_FO_EMAILREPORT_KPI_20250623_193000_last_30_minutes.csv",
    ]
    for name in filenames:
        (tmp_path / name).touch()

    with pytest.raises(ValueError) as valueErrorException:
        identify_gaps(str(tmp_path), "UNEXISTING_FILE_20250623_180000_last_30_minutes.csv", 30)
    assert str(valueErrorException.value) == "No files found matching example filename."