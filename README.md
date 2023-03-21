# EHR Data Analysis

The ehr-utils library provides analytical capabilities for EHR data.

### Setup Instructions
* In your local terminal, clone the repo: 
```git clone https://github.com/biostat821-2023/ehr-utils-heath3rq.git```
* Python version: `3.10 and above`
* Required libraries: `pytest`


### Details of Each Function/Class
The `main.py` includes two custom classes and three functions:

* Class `Lab` storing lab information of a patient as instance attributes

* Class `Patient` storing patient information as instance attributes. The `Patient` class has two properties (`age` and `age_at_first_admission`) and a method called `is_sick` to check whether a patient has ever been sick:
    - `age`: returns the age in years of a given patient.
    - `age_at_first_admission` returns the age of a given patient when their earliest lab was recorded. 
    - `patient_is_sick`: checks whether a patient has ever had a test with value above (">") or below ("<") the given level
        -  Input:  
            (a) Patient ID in string format
            (b) Lab test name of interest in string format
            (c) A number as the decision criteria of test values
        - Output: `True` or `False` indcating whether a patient has ever been sick

* `parse_data` reads and parses the data files.
    - Input: 
        (a) A path to a `.txt` file storing patient information where the first column is the patient ID. 
        (b) A path to a `.txt` file storing lab information of patients where the first column is the patient ID. 
    - Output: a dictionary with Patient IDs as keys and the `Patient` class as values

* `date_type_conversion` converts date in string format to datetime format. It is used internally in `patient_age` method.
    - Input: date of birth in string format
    - Output: date of birth in date format

* `search_test_results` searches test results of a given patient. It is used internally in `patient_is_sick` method.
    - Input: 
        (a) Lab information of patients stored in the `Lab` class, child of the `Patient` class
        (b) Lab test name of interest in string format
    - Output: A list of all lab results of a given patient 


### Examples
```python
>> patient_records = parse_data("patient_file_name.txt", "labs_file_name.txt")

>> patient_records['1A8791E3-A61C-455A-8DEE-763EB90C9B2C'].age
50

>>> patient_records['1A8791E3-A61C-455A-8DEE-763EB90C9B2C'].age_at_first_admission
19

>> patient_records['1A8791E3-A61C-455A-8DEE-763EB90C9B2C'].is_sick("<","URINALYSIS: RED BLOOD CELLS",1.5)
True
```

### Test Instruction

To run pytest and check test coverage, run the following code in terminal: 
```
pip install --upgrade pip && pip install -r requirements-test.txt
pytest main_test.py
coverage run -m pytest tests/test_main.py > test_report.txt
coverage report -m
```
