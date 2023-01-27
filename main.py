"""A module that analyzes EHR data."""
from datetime import datetime

# ASSUMPTIONS
# 1. Input file always has a header
# 2. There is no duplicative records in the file
# 3. The order of the record details is the same as the sample file
# 4. File name is provided in string format
# 4. Every record has a patient ID and they are provided in string format
# 5. Birthday is always listed in the index 4th position


def parse_data(filename: str) -> dict[str, list[str]]:
    """Parse EHR Data."""
    with open(filename, mode="r", encoding="utf-8-sig") as patient_file:
        lines_lst = patient_file.readlines()[1:]  # skips header
        records_lst = [x.strip().split("\t") for x in lines_lst]
        records_dict = {r[0]: r[1:] for r in records_lst}
        return records_dict

    # with open(lab_filename, mode="r", encoding="utf-8-sig") as lab_file:
    #     line_lab = lab_file.readlines()[1:]  # skips header
    #     records_lab = [x.strip().split("\t") for x in line_lab]
    #     idv_lab_record_dict = {r[0]: r[1:] for r in records_lab}
    #     print(idv_lab_record_dict)


def date_type_conversion(date_time: str) -> datetime:
    """Convert a string to a datetime object."""
    return datetime.strptime(date_time[0][0], "%Y-%m-%d %H:%M:%S.%f")


def patient_age(
    idv_patient_record_dict: dict[str, list[str]], patient_id: str
) -> int | str:
    """Calculate Patient Age in Years."""
    if patient_id in idv_patient_record_dict.keys():
        birth_year = date_type_conversion(
            idv_patient_record_dict[patient_id][4]
        ).year
        today = datetime.now()
        age = today.year - birth_year
        return int(age)
    else:
        return "Something went wrong."


if __name__ == "__main__":
    records = parse_data("PatientCorePopulatedTable.txt")
    patient_age(records, "81C5B13B-F6B2-4E57-9593-6E7E4C13B2CE")
