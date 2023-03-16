"""A module that tests EHR data."""
import pytest
from fake_files import fake_files
from main import (
    parse_data,
)


def test_main() -> None:
    """Test parse data function."""
    table_lab = [
        [
            "PatientID",
            "AdmissionID",
            "LabName",
            "LabValue",
            "LabUnits",
            "LabDateTime",
        ],
        [
            "1A8791E3-A61C-455A-8DEE-763EB90C9B2C",
            "1",
            "URINALYSIS: RED BLOOD CELLS",
            "1.8",
            "rbc/hpf",
            "1992-07-01 01:36:17.910",
        ],
    ]
    table_patient = [
        [
            "PatientID",
            "PatientGender",
            "PatientDateOfBirth",
            "PatientRace",
            "PatientMaritalStatus",
            "PatientLanguage",
            "PatientPopulationPercentageBelowPoverty",
        ],
        [
            "1A8791E3-A61C-455A-8DEE-763EB90C9B2C",
            "Male",
            "1973-08-16 10:58:34.413",
            "Asian",
            "Single",
            "English",
            "13.97",
        ],
    ]
    with fake_files(table_lab) as labs, fake_files(table_patient) as patients:
        patient_records = parse_data(patients[0], labs[0])
    assert (
        patient_records["1A8791E3-A61C-455A-8DEE-763EB90C9B2C"].age == 50
    ), "Error calculating patient age."
    assert (
        patient_records[
            "1A8791E3-A61C-455A-8DEE-763EB90C9B2C"
        ].age_at_first_admission
        == 19
    ), "Error calculating age at first admission"
    assert (
        patient_records["1A8791E3-A61C-455A-8DEE-763EB90C9B2C"].is_sick(
            "<", "URINALYSIS: RED BLOOD CELLS", 1.5
        )
        is False
    ), "Error in determining whether patient is sick."
    with pytest.raises(ValueError):
        patient_records["1A8791E3-A61C-455A-8DEE-763EB90C9B2C"].is_sick(
            "=", "URINALYSIS: RED BLOOD CELLS", 1.5
        )
    with pytest.raises(ValueError):
        patient_records["1A8791E3-A61C-455A-8DEE-763EB90C9B2C"].is_sick(
            "<", "URINALYSIS: RED BLOOD CELLSS", 1.5
        )
