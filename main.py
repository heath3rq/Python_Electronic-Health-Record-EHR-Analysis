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
) -> tuple[dict[str, list[str]], list[dict[str, list[str]]]]:
    """Parse EHR Data.

    Opening the file takes constant time, but reading lines takes O(N*CP) or
    O(M*CL) time for patient/lab record files,respectively. Stripping the lines
    of whitespace and splitting the lines into a list takes
    O(CP)*O(N) = O(CP*N) time for patient records, and O(CL)*O(M) = O(CL*M).
    The list comprehension that puts each line of patient record in the list
    into a dictionary takes O(1)*O(N) = O(N) time, and O(1)*O(M) = O(M) time
    for each lab record. If we assume M > N, our big-O notation is therefore
    O(M) after dropping the constant factors.

    """
    with open(
        patient_filename, mode="r", encoding="utf-8-sig"
    ) as file:  # O(1)
        patient_lines_str = file.readlines()  # O(N*CP)
    patient_lines_lst = [
        i.strip().split("\t") for i in patient_lines_str  # O(N*CP)
    ]
    patient_dict = {}  # O(1)
    for record in patient_lines_lst:  # O(N)
        patient_dict[record[0]] = record[1:]  # O(1)
    with open(lab_filename, mode="r", encoding="utf-8-sig") as file:  # O(1)
        lab_lines_str = file.readlines()  # O(M*CL)
    lab_lines_lst = [i.strip().split("\t") for i in lab_lines_str]  # O(M*CL)
    lab_records = [{r[0]: r[1:]} for r in lab_lines_lst]  # O(M)
    return patient_dict, lab_records  # O(1)


def date_type_conversion(date_time: str) -> datetime:
    """Convert a string to a datetime object.

    O(1) total
    """
    return datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S.%f")  # O(1)


def patient_age(patient_records: dict[str, list[str]], patient_id: str) -> int:
    """Calculate Patient Age in Years.

    Retriving date index from a list of headers will take constant time O(1)
    Retriving values from a dictionary takes O(N) time. Converting date from
    string format to date format,retrieving current year, and
    calculating/returning patient age are all operations of O(1) time
    complexity. Our big-O notation is therefore O(N) after dropping
    the constant factors.

    """
    date_index = patient_records["PatientID"].index(
        "PatientDateOfBirth"
    )  # O(1)
    dob_string = patient_records[patient_id][date_index]  # O(N*CP)
    dob_int = date_type_conversion(dob_string)  # O(1)
    today = datetime.now()  # O(1)
    age = today.year - dob_int.year  # O(1)
    return int(age)  # O(1)


def search_test_results(
    lab_records: list[dict[str, list[str]]], patient_id: str, test_name: str
) -> list[float]:
    """Search Test Results by Patient ID.

    Retriving indexes from a list of headers takes O(1) constant time.
    Looping through the lab records to check if a patient has completed a
    specific test takes 0(M*CL) time. Then, retriving test results take O(1)
    constant time. Our big-O notation is therefore O(M*CL) after dropping the
    constant factors.

    """
    lab_record_header = lab_records[0]["PatientID"]  # O(CL)
    lab_name_index = lab_record_header.index("LabName")  # O(1)
    lab_value_index = lab_record_header.index("LabValue")  # O(1)
    return [
        float(lab_record[patient_id][lab_value_index])  # O(1)
        for lab_record in lab_records  # O(M)
        if (
            patient_id in lab_record
            and lab_record[patient_id][lab_name_index] == test_name
        )  # O(CL)
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
    print(patient_age(records[0], "1A8791E3-A61C-455A-8DEE-763EB90C9B2"))
    print(
        patient_is_sick(
            records[1],
            "1A8791E3-A61C-455A-8DEE-763EB90C9B2C",
            "URINALYSIS: RED BLOOD CELLS",
            ">",
            1.5,
        )
    )
