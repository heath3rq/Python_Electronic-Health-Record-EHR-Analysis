"""A module that tests EHR data."""
import pytest
from fake_files import fake_files
from main import (
    parse_data,
    patient_age,
    patient_is_sick,
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
    ]
}

patient_records_dict = {
    "FB2ABB23-C9D0-4D09-8464-49BF0B982F0F": {
        "PatientGender": "Male",
        "PatientDateOfBirth": "1947-12-28 02:45:40.547",
        "PatientRace": "Unknown",
        "PatientMaritalStatus": "Married",
        "PatientLanguage": "Icelandic",
        "PatientPopulationPercentageBelowPoverty": "18.08",
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
            "FB2ABB23-C9D0-4D09-8464-49BF0B982F0F",
            "Male",
            "1947-12-28 02:45:40.547",
            "Unknown",
            "Married",
            "Icelandic",
            "18.08",
        ],
    ]
    with fake_files(table_lab) as labs, fake_files(table_patient) as patients:
        patient_records, lab_records = parse_data(patients[0], labs[0])
        assert patient_records == {
            "FB2ABB23-C9D0-4D09-8464-49BF0B982F0F": {
                "PatientGender": "Male",
                "PatientDateOfBirth": "1947-12-28 02:45:40.547",
                "PatientRace": "Unknown",
                "PatientMaritalStatus": "Married",
                "PatientLanguage": "Icelandic",
                "PatientPopulationPercentageBelowPoverty": "18.08",
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
        patient_records, "FB2ABB23-C9D0-4D09-8464-49BF0B982F0F"
    )
    assert patient_age_ == 76, "Error calculating patient age."


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


def test_wrong_patient_id_pis() -> None:
    """Test patient_is_sick function when incorrect patient ID is given."""
    with pytest.raises(ValueError):
        patient_is_sick(
            lab_records_dict,
            "1A8791E3-A61C-455A-8DEE-763EB90C9B2CA",
            "URINALYSIS: RED BLOOD CELLS",
            "<",
            1.5,
        )


def test_wrong_operator_pis() -> None:
    """Test patient_is_sick function when incorrect operator is given."""
    with pytest.raises(ValueError):
        patient_is_sick(
            lab_records_dict,
            "1A8791E3-A61C-455A-8DEE-763EB90C9B2C",
            "URINALYSIS: RED BLOOD CELLS",
            "=",
            1.5,
        )


def test_wrong_test_name_pis() -> None:
    """Test patient_is_sick function when incorrect test name is given."""
    with pytest.raises(ValueError):
        patient_is_sick(
            lab_records_dict,
            "1A8791E3-A61C-455A-8DEE-763EB90C9B2C",
            "URINALYSIS: RED BLOOD",
            "<",
            1.5,
        )


def test_wrong_patient_id_pa() -> None:
    """Test patient_age function when incorrect patient ID is given."""
    with pytest.raises(ValueError):
        patient_age(
            patient_records_dict, "FB2ABB23-C9D0-4D09-8464-49BF0B982F0FBB"
        )
