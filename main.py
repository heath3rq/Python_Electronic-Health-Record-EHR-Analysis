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
) -> tuple[dict[str, dict[str, str]], dict[str, list[dict[str, str]]]]:
    """Parse EHR Data.

    Opening the file takes constant time, but reading lines takes O(N*CP) or
    O(M*CL) time for patient/lab record files. Stripping the lines
    of whitespace and splitting the lines into a list takes
    O(CP)*O(N) = O(CP*N) time for patient records, and O(CL)*O(M) = O(CL*M).
    The list comprehension that puts each line of patient record in the list
    into a dictionary takes O(1)*O(N) = O(N) time, and O(1)*O(M) = O(M) time
    for each lab record. Together, our big-O notation is therefore
    O(CL*M+CP*N) after dropping the constant factors.

    """
    with open(
        patient_filename, mode="r", encoding="utf-8-sig"
    ) as file:  # O(1)
        patient_lines_str = file.readlines()  # O(N*CP)
    patient_lines_lst = [
        i.strip().split("\t") for i in patient_lines_str  # O(N*CP)
    ]
    patient_records_dict = {}  # O(1)
    patient_header = patient_lines_lst[0]
    for record in patient_lines_lst[1:]:  # O(N)
        patient_records_dict[record[0]] = {
            patient_header[record_idx]: record[record_idx]
            for record_idx in range(1, len(record))
        }  # O(CP)

    with open(lab_filename, mode="r", encoding="utf-8-sig") as file:
        lab_lines_str = file.readlines()  # O(M*CL)
    lab_lines_lst = [i.strip().split("\t") for i in lab_lines_str]  # O(M*CL)
    lab_records_dict: dict[str, list[dict[str, str]]] = {}  # O(1)
    lab_header = lab_lines_lst[0]  # O(1)
    for line in lab_lines_lst[1:]:  # O(M)
        if line[0] in lab_records_dict:  # O(1)
            lab_records_dict[line[0]].append(
                {
                    lab_header[lab_indx]: line[lab_indx]
                    for lab_indx in range(1, len(line))
                }
            )  # O(CL)
        else:
            lab_records_dict[line[0]] = [
                {
                    lab_header[lab_indx]: line[lab_indx]
                    for lab_indx in range(1, len(line))
                }
            ]  # O(CL)
    return patient_records_dict, lab_records_dict  # O(1)


def date_type_conversion(date_time: str) -> datetime:
    """Convert a string to a datetime object.

    O(1) total
    """
    return datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S.%f")  # O(1)


def patient_age(
    patient_records_dict: dict[str, dict[str, str]], patient_id: str
) -> int:
    """Calculate Patient Age in Years.

    Retriving date index from a list of headers will take constant time O(1)
    Retriving values from a dictionary takes O(1) time. Converting date from
    string format to date format,retrieving current year, and
    calculating/returning patient age are all operations of O(1) time
    complexity. Our big-O notation is therefore constant time.

    """
    if patient_id not in patient_records_dict:  # O(1)
        raise ValueError(
            f"Patient ID: {patient_id} not found in patient data."
        )  # O(1)
    dob_string = patient_records_dict[patient_id]["PatientDateOfBirth"]  # O(1)
    dob_int = date_type_conversion(dob_string)  # O(1)
    today = datetime.now()  # O(1)
    age = today.year - dob_int.year  # O(1)
    return int(age)  # O(1)


def search_test_results(
    lab_records_dict: dict[str, list[dict[str, str]]],
    patient_id: str,
    test_name: str,
) -> list[float]:
    """Search Test Results by Patient ID.

    Creating an empty list and indexing the dictionary of lab records based on
    patient id takes constant time. For each patient, looping through their lab
    files on average takes O(M/N) time. Checking if the given test name is in
    patient lab record dictionary takes constatnt time, and appending the lab
    result to a list takes constant time. Checking if a list is empty and
    raise error if empty each take constant time. Returing lab results for a
    patient take constant time. Our big-O notation is therefore O(M/N) after
    dropping the constant factors.
    """
    patient_lab_results = []  # O(1)
    patient_labs = lab_records_dict[patient_id]  # O(1)
    for record in patient_labs:  # O(M/N)
        if record["LabName"] == test_name:  # O(1)
            patient_lab_results.append(float(record["LabValue"]))  # O(1)
    if not patient_lab_results:
        raise ValueError(
            f"The patient has never done the test: \
                {test_name.title().strip(':')}."
        )  # O(1)
    return patient_lab_results  # O(1)


def patient_is_sick(
    lab_records_dict: dict[str, list[dict[str, str]]],
    patient_id: str,
    lab_name: str,
    operator: str,
    value: float,
) -> bool:
    """Check if a patient was once sick.

    Checking the input operator and patient ID each takes O(1) time.
    Comparing whether the max/min lab value is greater than or smaller to the
    input value takes O(1) time. Assessing the max/min values from a list of
    patient lab results on average takes O(M/N) time. Our big-O notation is
    therefore O(M/N) after dropping the constant factors.

    """
    if operator not in ["<", ">"]:  # O(1)
        raise ValueError("Operator can only be '<' or '>'.")  # O(1)
    if patient_id not in lab_records:  # O(1)
        raise ValueError(
            f"Patient ID: {patient_id} not found in lab data."
        )  # O(1)

    if operator == ">" and (
        max(search_test_results(lab_records_dict, patient_id, lab_name))
        > value
    ):  # O(M/N)
        return True  # O(1)
    elif operator == "<" and (
        max(search_test_results(lab_records_dict, patient_id, lab_name))
        < value
    ):  # O(M/N)
        return True  # O(1)
    else:  # O(1)
        return False  # O(1)


if __name__ == "__main__":
    patient_records, lab_records = parse_data(
        "PatientCorePopulatedTable.txt", "LabsCorePopulatedTable.txt"
    )
    print(patient_age(patient_records, "1A8791E3-A61C-455A-8DEE-763EB90C9B2C"))
    print(
        patient_is_sick(
            lab_records,
            "1A8791E3-A61C-455A-8DEE-763EB90C9B2C",
            "URINALYSIS: RED BLOOD CELLS",
            "<",
            1.5,
        )
    )
