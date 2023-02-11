"""A module that analyzes EHR data."""
from datetime import datetime

# COMPUTATIONAL COMPLEXITY DEFINITION
# N is the number of patients
# M is the number of lab records
# CP is the number of columns in the patient file
# CL is the number of columns in the lab file

# ASSUMPTIONS:
# 1. Input file always has a header in the first row position.
# 2. There is no duplicative records in the files.
# 3. File Names and Patient IDs are provided in string format.
# 4. The first column is always the patient ID.


def parse_data(
    patient_filename: str, lab_filename: str
) -> tuple[list[dict[str, list[str]]], list[dict[str, list[str]]]]:
    """Parse EHR Data.

    Opening the file takes constant time, but reading lines takes O(N)/O(M)
    time for patient/lab record files,respectively. The list comprehension that
    strips the lines of whitespace and splitting the lines into a list takes
    O(1)*O(N) = O(N) time for patient records, and O(1)*O(M) = O(M).
    The list comprehension that puts each line of patient record in the list
    into a dictionary takes O(1)*O(N) = O(N) time, and O(1)*O(M) = O(M) time
    for each lab record. If we assume M > N, our big-O notation is therefore
    O(M) after dropping the constant factors.

    """
    with open(
        patient_filename, mode="r", encoding="utf-8-sig"
    ) as file:  # O(1)
        patient_lines_str = file.readlines()  # O(N)
    patient_lines_lst = [
        i.strip().split("\t") for i in patient_lines_str  # O(1)  # O(N)
    ]
    patient_records = [
        {r[0]: r[1:]} for r in patient_lines_lst  # O(1)  # O(N)
    ]
    with open(lab_filename, mode="r", encoding="utf-8-sig") as file:  # O(1)
        lab_lines_str = file.readlines()  # O(M)
    lab_lines_lst = [
        i.strip().split("\t") for i in lab_lines_str  # O(1)  # O(M)
    ]
    lab_records = [{r[0]: r[1:]} for r in lab_lines_lst]  # O(1)  # O(M)
    return patient_records, lab_records  # O(1)


def date_type_conversion(date_time: str) -> datetime:
    """Convert a string to a datetime object.

    O(1) total
    """
    return datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S.%f")  # O(1)


def patient_age(
    patient_records: list[dict[str, list[str]]], patient_id: str
) -> int:
    """Calculate Patient Age in Years.

    Retriving date index from a list of headers will take time O(CP) where CP
    is the length of the patient file header. Getting the next item of a
    list takes O(1) time. Looping through the patient records to check if a
    patient ID exists takes 0(N**2) time. Then, retriving patient's date of
    birth takes O(1) time. Converting date from string format to date format,
    retrieving current year, and calculating/returning patient age are all
    operations of O(1) time complexity. Our big-O notation is therefore
    O(N**2) after dropping the constant factors.

    """
    date_index = patient_records[0]["PatientID"].index(
        "PatientDateOfBirth"
    )  # O(CP)
    dob_string = next(  # O(1)
        record[patient_id][date_index]  # O(1)
        for record in patient_records  # O(N)
        if patient_id in record  # O(N)
    )
    dob_int = date_type_conversion(dob_string)  # O(1)
    today = datetime.now()  # O(1)
    age = today.year - dob_int.year  # O(1)
    return int(age)  # O(1)


def search_test_results(
    lab_records: list[dict[str, list[str]]], patient_id: str, test_name: str
) -> list[float]:
    """Search Test Results by Patient ID.

    Retriving indexes from a list of headers takes time O(CL) each time where
    CL is the length of the lab file header. Looping through the lab records to
    check if a patient has completed a specific test takes 0(M**2) time. Then,
    retriving test results take O(1) constant time. Our big-O notation is
    therefore O(M**2) after dropping the constant factors.

    """
    lab_record_header = lab_records[0]["PatientID"]  # O(CL)
    lab_name_index = lab_record_header.index("LabName")  # O(CL)
    lab_value_index = lab_record_header.index("LabValue")  # O(CL)
    return [
        float(i[patient_id][lab_value_index])  # O(1)
        for i in lab_records  # O(M)
        if (
            patient_id in i and i[patient_id][lab_name_index] == test_name
        )  # O(M)
    ]


def patient_is_sick(
    lab_records: list[dict[str, list[str]]],
    patient_id: str,
    lab_name: str,
    operator: str,
    value: float,
) -> bool:
    """Check if a patient was once sick.

    Checking the input operator takes O(1) time. Comparing whether the max/min
    lab value is greater than or smaller to the input value takes O(1) time.
    Assessing the max/min values from a list of patient lab results on average
    takes O(M/N) time. Other scenarios (i.e., patient not sick) all takes O(1)
    time. Our big-O notation is therefore O(M/N) after dropping the constant
    factors.

    """
    if operator == ">":  # O(1)
        if (
            max(search_test_results(lab_records, patient_id, lab_name)) > value
        ):  # O(M/N)
            return True  # O(1)
    elif operator == "<":  # O(1)
        if (
            min(search_test_results(lab_records, patient_id, lab_name)) < value
        ):  # O(M/N)
            return True  # O(1)
    else:  # O(1)
        return False  # O(1)
    return False  # O(1)


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
