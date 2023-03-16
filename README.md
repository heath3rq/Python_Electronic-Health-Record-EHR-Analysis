# EHR Data Analysis

The ehr-utils library provides analytical capabilities for EHR data.

### Setup Instructions
* In your local terminal, clone the repo: 
```git clone https://github.com/biostat821-2023/ehr-utils-heath3rq.git```
* Python version: `3.10 and above`
* Required libraries: `datatime`


### Details of Each Function and Expected Input
The `main.py` includes three main functions and two helper functions:
* `parse_data` reads and parses the data files.
    - Input: 
        a. A path to a `.txt` file storing patient information where the first column is the patient ID. 
        b. A path to a `.txt` file storing lab information of patients where the first column is the patient ID. 
    - Output: a tuple of two dictionaries, one for patient information and the other for lab information of patients. 

* `date_type_conversion` converts date in string format to datetime format. It is used internally in `patient_age` method.
    - Input: date of birth in string format
    - Output: date of birth in date format

* `patient_age` calculates the age in years of a given patient. 
    - Input: 
        a. Patient information stored in dictionary format. This is the first dictionary in the resulting tuple from `parse_date` function. 
        b. Patient ID in string format
    - Output: the age of a given patient

* `search_test_results`: searches test results of a given patient. It is used internally in `patient_is_sick` method.
    - Input: 
        a. Lab information of patients stored in dictionary format. This is the second dictionary in the resulting tuple from `parse_date` function. 
        b. Patient ID in string format
        c. Lab test name of interest in string format
    - Output: 

* `patient_is_sick`: checks whether a patient has ever had a test with value above (">") or below ("<") the given level
    - Input: 
        a. Lab information of patients stored in dictionary format. This is the second dictionary in the resulting tuple from `parse_date` function. 
        b. Patient ID in string format
        c. Lab test name of interest in string format
        d. A number as the decision criteria of test values
    - Output: `True` or `False` indcating whether a patient has ever been sick

* `patient_age_at_first_admission`: computes the age of a given patient when their earliest lab was recorded. 


### Examples
```python
>> patient_records, lab_records = parse_data("patient_file_name.txt", "labs_file_name.txt")

>> dob_string = "1947-12-28 02:45:40.547"
>> DOB = date_type_conversion(dob_string)
1947-12-28 02:45:40.547000

>> patient_age(patient_records, "1A8791E3-A61C-455A-8DEE-763EB90C9B2C")
50

>> ssearch_test_results(lab_records, "FB2ABB23-C9D0-4D09-8464-49BF0B982F0F", "URINALYSIS: RED BLOOD CELLS")
[3.1, 0.8, 1.1, 2.7, 0.1, 1.4, 2.7, 1.9, 1.9, 3.3, 2.7, 2.2, 0.9, 0.5, 1.9, 1.9, 2.2, 0.4]

>> patient_is_sick(lab_records, "1A8791E3-A61C-455A-8DEE-763EB90C9B2C", "METABOLIC: ALBUMIN", ">", 4.0)
True

>>> patient_age_at_first_admission(lab_records, patient_records, "FB2ABB23-C9D0-4D09-8464-49BF0B982F0F")
19
```

### Test Instruction

To run pytest and check test coverage, run the following code in terminal: 
```
pip install --upgrade pip && pip install -r requirements-test.txt
pytest main_test.py
coverage run -m pytest main_test.py > test_report.txt
coverage report -m
```
