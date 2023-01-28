"""A module that analyzes EHR data."""
from datetime import datetime

# ASSUMPTIONS:
# 1. Input file always has a header in the first row position.
# 2. There is no duplicative records in the files.
# 3. The order of the record details is the same as the sample file.
# 4. File name is provided in string format.
# 4. Every record has a patient ID and they are provided in string format.
# 5. Birthday is always listed in the 4th index position of the file.
# 6. Lab Name is always listed in the 3rd index postition of the file.


def parse_data(filename: str) -> list[dict[str, list[str]]]:
    """Parse EHR Data."""
    with open(filename, mode="r", encoding="utf-8-sig") as file:
        lines_str = file.readlines()[1:]  # skips header
        lines_lst = [x.strip().split("\t") for x in lines_str]
        records = [{r[0]: r[1:]} for r in lines_lst]
        return records


def date_type_conversion(date_time: str) -> datetime:
    """Convert a string to a datetime object."""
    return datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S.%f")


def patient_age(
    records: list[dict[str, list[str]]], patient_id: str
) -> int | str:
    """Calculate Patient Age in Years."""
    dob_string = [z[patient_id][1] for z in records if patient_id in z][0]
    dob_int = date_type_conversion(dob_string)
    today = datetime.now()
    age = today.year - dob_int.year
    return int(age)


def search(
    records: list[dict[str, list[str]]], patient_id: str, test_name: str
) -> list[float]:
    """Search Test Results by Patient ID."""
    return [
        float(i)
        for i in [
            j[patient_id][2]
            for j in records
            if (patient_id in j and j[patient_id][1] == test_name)
        ]
    ]


def patient_is_sick(
    records: list[dict[str, list[str]]],
    patient_id: str,
    lab_name: str,
    operator: str,
    value: float,
) -> bool:
    """Check if a patient was once sick."""
    if operator == ">":
        if max(search(records, patient_id, lab_name)) > value:
            return True
    elif operator == "<":
        if min(search(records, patient_id, lab_name)) < value:
            return True
    else:
        return False
    return False


if __name__ == "__main__":
    patient_records = parse_data("PatientCorePopulatedTable.txt")
    lab_records = parse_data("LabsCorePopulatedTable.txt")
    print(
        patient_is_sick(
            lab_records,
            "1A8791E3-A61C-455A-8DEE-763EB90C9B2C",
            "URINALYSIS: RED BLOOD CELLS",
            ">",
            1.5,
        )
    )
