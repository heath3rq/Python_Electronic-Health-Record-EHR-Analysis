"""A module that analyzes EHR data."""
from datetime import datetime
import os
import sqlite3

# from dataclasses import dataclass

# COMPUTATIONAL COMPLEXITY DEFINITION
# N is the number of patients
# M is the number of lab records
# CP is the number of columns in the patient file
# CL is the number of columns in the lab file

# ASSUMPTIONS:
# 1. Input file always has a header in the first row position.
# 2. There is no duplicative records in the files.
# 3. File Names, database name and Patient IDs are provided in string format.
# 4. File must contain columns in the same order as the sample input files


class Lab:
    """A Class for Lab Information."""

    def __init__(
        self,
        database_name: str,
        patient_id: str,
        #  lab_name: str,
        #  lab_value: str,
        #  lab_date: str,
        #  lab_units: str,
    ) -> None:
        """Initialize Lab Class."""
        connection = sqlite3.connect(database_name)
        with connection as cursor:
            self.lab_name = cursor.execute(
                "SELECT lab_name FROM labs WHERE patient_id = ?", (patient_id,)
            ).fetchall()
            self.lab_value = cursor.execute(
                "SELECT lab_value FROM labs WHERE patient_id = ?",
                (patient_id,),
            ).fetchall()
            self.lab_date = cursor.execute(
                "SELECT lab_date FROM labs WHERE patient_id = ?", (patient_id,)
            ).fetchall()
            # self.lab_units = cursor.execute("SELECT lab_units FROM labs "
            # "WHERE patient_id = ?", (patient_id,)).fetchall()


class Patient:
    """A Class for Patient Information."""

    def __init__(
        self,
        patient_id: str,
        database_name: str,
        # dob: str,
        # labs: list[Lab],
        # gender: str,
        # race: str,
        # marital_status: str,
        # language: str,
    ) -> None:
        """Initialize Patient Class."""
        self.patient_id = patient_id
        connection = sqlite3.connect(database_name)
        with connection as cursor:
            self.dob = cursor.execute(
                "SELECT date_of_birth FROM patients WHERE id = ?",
                (self.patient_id,),
            ).fetchall()[0][0]
            self.labs = Lab(database_name, self.patient_id)

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
        # patient_labs = self.lab # O(1)
        lab_dates = []  # O(1)
        for record in self.labs.lab_date:  # O(M/N)
            lab_dates.append(date_type_conversion(record[0]))  # O(1)
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

        lab_values = []
        for _idx, _lab_name in enumerate(self.labs.lab_name):
            if _lab_name[0] == lab_name:
                lab_values.append(float(self.labs.lab_value[_idx][0]))

        if not lab_values:
            raise ValueError(
                f"""The patient has never done the test \
[{lab_name}]."""
            )  # O(1)

        if operator == ">" and (
            max(lab_values) > decision_threshold
        ):  # O(M/N)
            return True  # O(1)
        elif operator == "<" and (
            min(lab_values) < decision_threshold
        ):  # O(M/N)
            return True  # O(1)
        else:  # O(1)
            return False  # O(1)


def parse_data(
    patient_filename: str, lab_filename: str, database_name: str
) -> None:
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
    if os.path.exists(database_name):
        os.remove(database_name)
    if not os.path.exists(patient_filename):
        raise FileNotFoundError("Patient file not found")
    if not os.path.exists(lab_filename):
        raise FileNotFoundError("Lab file not found")

    connection = sqlite3.connect(database_name)
    with connection as cursor:
        cursor.execute("DROP TABLE IF EXISTS patients")
        cursor.execute("DROP TABLE IF EXISTS labs")
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS patients(
                id VARCHAR PRIMARY KEY,
                gender VARCHAR,
                date_of_birth VARCHAR,
                race VARCHAR,
                marital_status VARCHAR,
                language VARCHAR,
                population_percentage_below_povert VARCHAR
                )"""
        )
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS labs(
                lab_id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id VARCHAR,
                admission_id VARCHAR,
                lab_name VARCHAR,
                lab_value VARCHAR,
                lab_unit VARCHAR,
                lab_date VARCHAR
                )"""
        )

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

        for lab_line in lab_lines_lst[1:]:  # O(M*CL)
            cursor.execute(
                "INSERT INTO labs(patient_id, admission_id, lab_name, "
                "lab_value, lab_unit, lab_date) VALUES (?,?,?,?,?,?)",
                lab_line,
            )

        for patient_line in patient_lines_lst[1:]:  # O(N*CP)
            cursor.execute(
                "INSERT INTO patients VALUES (?,?,?,?,?,?,?)", patient_line
            )


def date_type_conversion(date_time: str) -> datetime:
    """Convert a string to a datetime object.

    O(1) total
    """
    return datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S.%f")  # O(1)


if __name__ == "__main__":
    parse_data(
        "PatientCorePopulatedTable.txt",
        "LabsCorePopulatedTable.txt",
        "SampleDB.db",
    )
    patient = Patient("1A8791E3-A61C-455A-8DEE-763EB90C9B2C", "SampleDB.db")
    print(patient.age)
    print(patient.age_at_first_admission)
    print(patient.is_sick("<", "URINALYSIS: RED BLOOD CELLS", 1.5))
