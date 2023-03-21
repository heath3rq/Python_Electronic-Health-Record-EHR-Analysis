"""A module that tests EHR data."""
import pytest
from fake_files import fake_files
from main import parse_data, Patient, Lab

lab_records = [
    Lab(
        "1A8791E3-A61C-455A-8DEE-763EB90C9B2C",
        "URINALYSIS: RED BLOOD CELLS",
        "1.8",
        "1992-07-01 01:36:17.910",
    ),
]

patient_records = {
    "1A8791E3-A61C-455A-8DEE-763EB90C9B2C": Patient(
        "1A8791E3-A61C-455A-8DEE-763EB90C9B2C",
        "1973-08-16 10:58:34.413",
        lab_records,
    )
}


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
        records = parse_data(patients[0], labs[0])
    assert records == patient_records, "Error parsing data."


def test_age() -> None:
    """Test age property in Patient class."""
    assert (
        patient_records["1A8791E3-A61C-455A-8DEE-763EB90C9B2C"].age == 50
    ), "Error calculating patient age."


def test_age_at_first_admission() -> None:
    """Test age at first admission property in Patient class."""
    assert (
        patient_records[
            "1A8791E3-A61C-455A-8DEE-763EB90C9B2C"
        ].age_at_first_admission
        == 19
    ), "Error calculating age at first admission"


def test_is_sick() -> None:
    """Test is sick method in Patient class"""
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
