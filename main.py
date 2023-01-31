"""A module that analyzes EHR data."""
from datetime import datetime

# ASSUMPTIONS:
# 1. Input file always has a header in the first row position.
# 2. There is no duplicative records in the files.
# 3. File Names and Patient IDs are provided in string format.
# 4. The first column is always the patient ID.


def parse_data(
    patient_filename: str, lab_filename: str
) -> tuple[list[dict[str, list[str]]], list[dict[str, list[str]]]]:
    """Parse EHR Data."""
    with open(patient_filename, mode="r", encoding="utf-8-sig") as file:
        patient_lines_str = file.readlines()
        patient_lines_lst = [i.strip().split("\t") for i in patient_lines_str]
        patient_records = [{r[0]: r[1:]} for r in patient_lines_lst]
    with open(lab_filename, mode="r", encoding="utf-8-sig") as file:
        lab_lines_str = file.readlines()
        lab_lines_lst = [i.strip().split("\t") for i in lab_lines_str]
        lab_records = [{r[0]: r[1:]} for r in lab_lines_lst]
        return patient_records, lab_records


def date_type_conversion(date_time: str) -> datetime:
    """Convert a string to a datetime object."""
    return datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S.%f")


def patient_age(
    patient_records: list[dict[str, list[str]]], patient_id: str
) -> int:
    """Calculate Patient Age in Years."""
    date_index = patient_records[0]["PatientID"].index("PatientDateOfBirth")
    dob_string = [
        record[patient_id][date_index]
        for record in patient_records
        if patient_id in record
    ][0]
    dob_int = date_type_conversion(dob_string)
    today = datetime.now()
    age = today.year - dob_int.year
    return int(age)


def search_test_results(
    lab_records: list[dict[str, list[str]]], patient_id: str, test_name: str
) -> list[float]:
    """Search Test Results by Patient ID."""
    lab_record_header = lab_records[0]["PatientID"]
    lab_name_index = lab_record_header.index("LabName")
    lab_value_index = lab_record_header.index("LabValue")
    return [
        float(i[patient_id][lab_value_index])
        for i in lab_records
        if (patient_id in i and i[patient_id][lab_name_index] == test_name)
    ]


def patient_is_sick(
    lab_records: list[dict[str, list[str]]],
    patient_id: str,
    lab_name: str,
    operator: str,
    value: float,
) -> bool:
    """Check if a patient was once sick."""
    if operator == ">":
        if max(search_test_results(lab_records, patient_id, lab_name)) > value:
            return True
    elif operator == "<":
        if min(search_test_results(lab_records, patient_id, lab_name)) < value:
            return True
    else:
        return False
    return False


if __name__ == "__main__":
    records = parse_data(
        "PatientCorePopulatedTable.txt", "LabsCorePopulatedTable.txt"
    )
    print(
        patient_is_sick(
            records[1],
            "1A8791E3-A61C-455A-8DEE-763EB90C9B2C",
            "URINALYSIS: RED BLOOD CELLS",
            ">",
            1.5,
        )
    )
