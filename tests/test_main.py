"""A module that tests EHR data."""
import pytest
from fake_files import fake_files
from main import (
    parse_data,
    patient_age,
    patient_is_sick,
    patient_age_at_first_admission,
)


lab_records_dict = {
    "1A8791E3-A61C-455A-8DEE-763EB90C9B2C": [
        {
            "AdmissionID": "1",
            "LabName": "URINALYSIS: RED BLOOD CELLS",
            "LabValue": "1.8",
            "LabUnits": "rbc/hpf",
            "LabDateTime": "1992-07-01 01:36:17.910",
        },
    ],
    "1A8791E3-A61C-455A-8DEE-763EB90C9B2F": [
        {
            "AdmissionID": "1",
            "LabName": "URINALYSIS: RED BLOOD CELLS",
            "LabValue": "6.8",
            "LabUnits": "rbc/hpf",
            "LabDateTime": "1990-08-01 01:34:17.910",
        },
    ],
}

patient_records_dict = {
    "1A8791E3-A61C-455A-8DEE-763EB90C9B2C": {
        "PatientGender": "Male",
        "PatientDateOfBirth": "1973-08-16 10:58:34.413",
        "PatientRace": "Asian",
        "PatientMaritalStatus": "Single",
        "PatientLanguage": "English",
        "PatientPopulationPercentageBelowPoverty": "13.97",
    },
    "1A8791E3-A61C-455A-8DEE-763EB90C9B2O": {
        "PatientGender": "Male",
        "PatientDateOfBirth": "1970-07-20 11:08:25.413",
        "PatientRace": "White",
        "PatientMaritalStatus": "Divorced",
        "PatientLanguage": "American",
        "PatientPopulationPercentageBelowPoverty": "10.23",
    },
}


def test_parse_data() -> None:
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
        patient_records, lab_records = parse_data(patients[0], labs[0])
        assert patient_records == {
            "1A8791E3-A61C-455A-8DEE-763EB90C9B2C": {
                "PatientGender": "Male",
                "PatientDateOfBirth": "1973-08-16 10:58:34.413",
                "PatientRace": "Asian",
                "PatientMaritalStatus": "Single",
                "PatientLanguage": "English",
                "PatientPopulationPercentageBelowPoverty": "13.97",
            }
        }, "Error parsing patient file."

        assert lab_records == {
            "1A8791E3-A61C-455A-8DEE-763EB90C9B2C": [
                {
                    "AdmissionID": "1",
                    "LabName": "URINALYSIS: RED BLOOD CELLS",
                    "LabValue": "1.8",
                    "LabUnits": "rbc/hpf",
                    "LabDateTime": "1992-07-01 01:36:17.910",
                },
            ]
        }, "Error parsing lab file."


def test_patient_age() -> None:
    """Test patient age function."""
    patient_records = patient_records_dict
    patient_age_ = patient_age(
        patient_records, "1A8791E3-A61C-455A-8DEE-763EB90C9B2C"
    )
    assert patient_age_ == 50, "Error calculating patient age."
    with pytest.raises(ValueError):
        patient_age(
            patient_records_dict, "FB2ABB23-C9D0-4D09-8464-49BF0B982F0FBB"
        )


def test_patient_age_at_first_admission() -> None:
    """Test patient age at first admission function"""
    age_at_admin = patient_age_at_first_admission(
        patient_records_dict,
        lab_records_dict,
        "1A8791E3-A61C-455A-8DEE-763EB90C9B2C",
    )
    assert (
        age_at_admin == 19
    ), "Error in patient_age_at_first_admission function"
    with pytest.raises(ValueError):
        patient_age_at_first_admission(
            patient_records_dict,
            lab_records_dict,
            "1A8791E3-A61C-455A-8DEE-763EB90C9B2C123",
        )
    with pytest.raises(ValueError):
        patient_age_at_first_admission(
            patient_records_dict,
            lab_records_dict,
            "1A8791E3-A61C-455A-8DEE-763EB90C9B2O",
        )


def test_patient_is_sick() -> None:
    """Test patient_is_sick function."""
    sick = patient_is_sick(
        lab_records_dict,
        "1A8791E3-A61C-455A-8DEE-763EB90C9B2C",
        "URINALYSIS: RED BLOOD CELLS",
        "<",
        1.5,
    )
    assert sick is False, "Error in patient_is_sick method."
    with pytest.raises(ValueError):
        patient_is_sick(
            lab_records_dict,
            "1A8791E3-A61C-455A-8DEE-763EB90C9B2C",
            "URINALYSIS: RED BLOOD",
            "<",
            1.5,
        )
    with pytest.raises(ValueError):
        patient_is_sick(
            lab_records_dict,
            "1A8791E3-A61C-455A-8DEE-763EB90C9B2CA",
            "URINALYSIS: RED BLOOD CELLS",
            "<",
            1.5,
        )
    with pytest.raises(ValueError):
        patient_is_sick(
            lab_records_dict,
            "1A8791E3-A61C-455A-8DEE-763EB90C9B2C",
            "URINALYSIS: RED BLOOD CELLS",
            "=",
            1.5,
        )
