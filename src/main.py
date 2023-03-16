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


class Lab:
    """A Class for Lab Information."""

    def __init__(
        self,
        patient_id: str,
        lab_name: str,
        lab_value: str,
        lab_date: str
        #  lab_units: str,
    ) -> None:
        """Initialize Lab Class."""
        self.patient_id = patient_id
        self.lab_name = lab_name
        self.lab_value = lab_value
        self.lab_date = lab_date
        # self.lab_units = lab_units


class Patient:
    """A Class for Patient Information."""

    def __init__(
        self,
        patient_id: str,
        dob: str,
        labs: list[Lab],
        # gender: str,
        # race: str,
        # marital_status: str,
        # language: str,
    ) -> None:
        """Initialize Patient Class."""
        self.patient_id = patient_id
        self.dob = dob
        self.labs = labs
        # self.gender = gender
        # self.race = race
        # self.marital_status = marital_status
        # self.language = language

    @property
    def age(self) -> int:
        """Calculate Patient Age in Years.

        O(1) time complexity total.

        """
        dob_int = date_type_conversion(self.dob)  # O(1)
        today = datetime.now()  # O(1)
        age = today.year - dob_int.year  # O(1)
        return int(age)  # O(1)

    @property
    def age_at_first_admission(self) -> int:
        """Compute age of a given patient when their earliest lab was recorded.

        Initializing an empty list take O(1). For each patient, looping
        through their lab files on average takes O(M/N) time. Find the earliest
        date from a list with the same length as the number of labs for a given
        patient is O(M/N) time. The rest of the operations takes constant time.
        Our big-O notation is therefore O(M/N) time.

        """
        patient_labs = self.labs  # O(1)
        lab_dates = []  # O(1)
        for record in patient_labs:  # O(M/N)
            lab_dates.append(date_type_conversion(record.lab_date))  # O(1)
        earliest_admission_date = min(
            lab_dates
        )  # O(M/N) because the length of the lab dates is the same
        #    as the number of labs a patient has
        dob_int = date_type_conversion(self.dob)  # O(1)
        age_at_first_admission = (
            earliest_admission_date.year - dob_int.year
        )  # O(1)
        return age_at_first_admission  # O(1)

    def is_sick(
        self,
        operator: str,
        lab_name: str,
        decision_threshold: float,
    ) -> bool:
        """Check if a patient was once sick.

        Checking whether the input operator is valid takes O(1) time.
        Comparing whether the max/min lab value is greater than or smaller to
        the input value takes O(1) time. Assessing the max/min values from a
        list of patient lab results on average takes O(M/N) time. Our big-O
        notation is therefore O(M/N) after dropping the constant factors.

        """
        if operator not in ["<", ">"]:  # O(1)
            raise ValueError("Operator can only be '<' or '>'.")  # O(1)

        if operator == ">" and (
            max(search_test_results(self.labs, lab_name)) > decision_threshold
        ):  # O(M/N)
            return True  # O(1)
        elif operator == "<" and (
            min(search_test_results(self.labs, lab_name)) < decision_threshold
        ):  # O(M/N)
            return True  # O(1)
        else:  # O(1)
            return False  # O(1)


def parse_data(patient_filename: str, lab_filename: str) -> dict[str, Patient]:
    """Parse EHR Data.

    Opening the file takes constant time, but reading lines takes O(N*CP) or
    O(M*CL) time for patient/lab record files. Stripping the lines
    of whitespace and splitting the lines into a list takes
    O(CP)*O(N) = O(CP*N) time for patient records, and O(CL)*O(M) = O(CL*M).
    Initializing empty dictionaries takes constant time. Indexing into
    dictionaries and retrieving index values take constant time.
    Together, our big-O notation is therefore
    O(CL*M+CP*N) after dropping the constant factors.

    """
    lab_lines_str = open(
        lab_filename, mode="r", encoding="utf-8-sig"
    ).readlines()  # O(M*CL)
    patient_lines_str = open(
        patient_filename, mode="r", encoding="utf-8-sig"
    ).readlines()  # O(N*CP)

    lab_lines_lst = [
        line.strip().split("\t") for line in lab_lines_str
    ]  # O(M*CL)
    patient_lines_lst = [
        line.strip().split("\t") for line in patient_lines_str
    ]  # O(N*CP)

    patient_records_dict = {}  # O(1)
    lab_records_dict: dict[str, list[Lab]] = {}  # O(1)

    lab_header = lab_lines_lst[0]  # O(1)
    lab_patient_id_idx = lab_header.index("PatientID")
    patient_header = patient_lines_lst[0]
    patient_id_idx = patient_header.index("PatientID")

    for lab_line in lab_lines_lst[1:]:  # O(M*CL)
        lab_obj = Lab(
            patient_id=lab_line[lab_patient_id_idx],  # O(CL)
            lab_name=lab_line[lab_header.index("LabName")],  # O(CL)
            lab_value=lab_line[lab_header.index("LabValue")],  # O(CL)
            lab_date=lab_line[lab_header.index("LabDateTime")],  # O(CL)
            #   lab_units=lab_line[lab_header.index("LabUnits")], # O(CL)
        )
        if lab_line[lab_patient_id_idx] in lab_records_dict:  # O(1)
            lab_records_dict[lab_line[lab_patient_id_idx]].append(
                lab_obj
            )  # O(1)
        else:  # O(1)
            lab_records_dict[lab_line[lab_patient_id_idx]] = [lab_obj]  # O(1)

    for patient_line in patient_lines_lst[1:]:  # O(N*CP)
        patient_obj = Patient(
            patient_id=patient_line[patient_id_idx],  # O(CP)
            dob=patient_line[
                patient_header.index("PatientDateOfBirth")
            ],  # O(CP)
            labs=lab_records_dict[patient_line[patient_id_idx]],  # O(CP)
        )
        patient_records_dict[
            patient_line[patient_id_idx]
        ] = patient_obj  # O(1)
    return patient_records_dict  # O(1)


def date_type_conversion(date_time: str) -> datetime:
    """Convert a string to a datetime object.

    O(1) total
    """
    return datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S.%f")  # O(1)


def search_test_results(
    lab_records_obj: list[Lab],
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
    for record in lab_records_obj:  # O(M/N)
        if record.lab_name == test_name:  # O(1)
            patient_lab_results.append(float(record.lab_value))  # O(1)
    if not patient_lab_results:
        raise ValueError(
            f"""The patient has never done the test \
[{test_name}]."""
        )  # O(1)
    return patient_lab_results  # O(1)


if __name__ == "__main__":
    patient_records = parse_data(
        "PatientCorePopulatedTable.txt", "LabsCorePopulatedTable.txt"
    )
    print(patient_records["1A8791E3-A61C-455A-8DEE-763EB90C9B2C"].age)
    print(
        patient_records[
            "1A8791E3-A61C-455A-8DEE-763EB90C9B2C"
        ].age_at_first_admission
    )
    print(
        patient_records["1A8791E3-A61C-455A-8DEE-763EB90C9B2C"].is_sick(
            "<", "URINALYSIS: RED BLOOD CELLS", 1.5
        )
    )
