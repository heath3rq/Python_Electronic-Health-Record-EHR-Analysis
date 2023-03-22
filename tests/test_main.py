"""A module that tests EHR data."""
import sqlite3
import pytest
from fake_files import fake_files
from main import parse_data, Patient


DATABASE_TEST = "SampleDB_Test.db"

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


def test_parse_data() -> None:
    """Test parse data function."""
    with fake_files(table_lab) as _labs, fake_files(
        table_patient
    ) as _patients:
        parse_data(_patients[0], _labs[0], "test.db")
        # Check if the expected data was inserted into the database
        con = sqlite3.connect("test.db")
        with con as cursor:
            patient_db = cursor.execute(
                "SELECT id, date_of_birth FROM patients"
            ).fetchall()
            assert (
                patient_db[0][0] == "1A8791E3-A61C-455A-8DEE-763EB90C9B2C"
            ), "Error parsing the patient file, patient id did not insert \
                correctly."
            assert (
                patient_db[0][1] == "1973-08-16 10:58:34.413"
            ), "Error parsing the patient file, patient date of birth did not \
                insert correctly."
            labs_db = cursor.execute(
                "SELECT patient_id, lab_name, lab_value, lab_date FROM labs"
            ).fetchall()
            assert (
                labs_db[0][0] == "1A8791E3-A61C-455A-8DEE-763EB90C9B2C"
            ), "Error parsing the lab file, patient id did not insert \
                correctly."
            assert (
                labs_db[0][1] == "URINALYSIS: RED BLOOD CELLS"
            ), "Error parsing the lab file, lab value did not insert \
                correctly."
            assert (
                labs_db[0][2] == "1.8"
            ), "Error parsing the lab file, lab value did not insert \
                correctly."
            assert (
                labs_db[0][3] == "1992-07-01 01:36:17.910"
            ), "Error parsing the lab file, lab date did not insert correctly."

        with pytest.raises(FileNotFoundError):
            parse_data("patients[0].txt", _labs[0], "test.db")
        with pytest.raises(FileNotFoundError):
            parse_data(_patients[0], "labs[0].txt", "test.db")


with fake_files(table_lab) as labs, fake_files(table_patient) as patients:
    parse_data(patients[0], labs[0], DATABASE_TEST)


patient = Patient("1A8791E3-A61C-455A-8DEE-763EB90C9B2C", DATABASE_TEST)


def test_age() -> None:
    """Test age property in Patient class."""
    assert patient.age == 50, "Error calculating patient age."


def test_age_at_first_admission() -> None:
    """Test age at first admission property in Patient class."""
    assert (
        patient.age_at_first_admission == 19
    ), "Error calculating age at first admission"


def test_is_sick() -> None:
    """Test is sick method in Patient class"""
    assert (
        patient.is_sick("<", "URINALYSIS: RED BLOOD CELLS", 1.5) is True
    ), "Error in determining whether patient is sick."
    with pytest.raises(ValueError):
        patient.is_sick("=", "URINALYSIS: RED BLOOD CELLS", 1.5)
    with pytest.raises(ValueError):
        patient.is_sick("<", "URINALYSIS: RED BLOOD CELLSS", 1.5)
