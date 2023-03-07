"""A module that tests EHR data."""
import pytest
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


def test_parse_data() -> tuple[
    dict[str, dict[str, str]], dict[str, list[dict[str, str]]]
]:
    """Test parse data function."""
    patient_records, lab_records = parse_data(
        "patient_file_sample.txt", "labs_file_sample.txt"
    )
    assert patient_records == {
        "FB2ABB23-C9D0-4D09-8464-49BF0B982F0F": {
            "PatientGender": "Male",
            "PatientDateOfBirth": "1947-12-28 02:45:40.547",
            "PatientRace": "Unknown",
            "PatientMaritalStatus": "Married",
            "PatientLanguage": "Icelandic",
            "PatientPopulationPercentageBelowPoverty": "18.08",
        },
        "64182B95-EB72-4E2B-BE77-8050B71498CE": {
            "PatientGender": "Male",
            "PatientDateOfBirth": "1952-01-18 19:51:12.917",
            "PatientRace": "African American",
            "PatientMaritalStatus": "Separated",
            "PatientLanguage": "English",
            "PatientPopulationPercentageBelowPoverty": "13.03",
        },
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
            {
                "AdmissionID": "1",
                "LabName": "METABOLIC: GLUCOSE",
                "LabValue": "103.3",
                "LabUnits": "mg/dL",
                "LabDateTime": "1992-06-30 09:35:52.383",
            },
        ]
    }, "Error parsing lab file."

    # If I don't have a return statement here, mypy is upset. If I do, pytest
    # gives me a warning. What would you recommend here?

    return patient_records, lab_records


def test_patient_age() -> int:
    """Test patient age function."""
    patient_records = patient_records_dict
    patient_age_ = patient_age(
        patient_records, "FB2ABB23-C9D0-4D09-8464-49BF0B982F0F"
    )
    assert patient_age_ == 76, "Error calculating patient age."
    return patient_age_


def test_patient_is_sick() -> bool:
    """Test patient_is_sick function."""
    sick = patient_is_sick(
        lab_records_dict,
        "1A8791E3-A61C-455A-8DEE-763EB90C9B2C",
        "URINALYSIS: RED BLOOD CELLS",
        "<",
        1.5,
    )
    assert sick is False, "Error in patient_is_sick method."
    return sick


# Tests for when incorrect input were given
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

with pytest.raises(ValueError):
    patient_is_sick(
        lab_records_dict,
        "1A8791E3-A61C-455A-8DEE-763EB90C9B2C",
        "URINALYSIS: RED BLOOD",
        "<",
        1.5,
    )


with pytest.raises(ValueError):
    patient_age(patient_records_dict, "FB2ABB23-C9D0-4D09-8464-49BF0B982F0FBB")
