# EHR Data Analysis

The ehr-utils library provides analytical capabilities for EHR data.

### Setup Instructions
- [ ] In your local terminal, clone the repo: 
```git clone https://github.com/biostat821-2023/ehr-utils-heath3rq.git```
- [ ] Python version: `3.10 and above`
- [ ] Required library: `pytest`


### Details of Each Function/Class
The `main.py` includes two custom classes and two functions:

* Class `Lab` storing lab information of a patient as instance attributes by calling the SQL database.

* Class `Patient` storing patient information as instance attributes by calling the SQL database. The `Patient` class has two properties (`age` and `age_at_first_admission`) and a method called `is_sick` to check whether a patient has ever been sick:
    - `age`: returns the age in years of a given patient.
    - `age_at_first_admission` returns the age of a given patient when their earliest lab was recorded. 
    - `patient_is_sick`: checks whether a patient has ever had a test with value above (">") or below ("<") the given level
        +  Input:  
            - Patient ID in string format
            - Lab test name of interest in string format
            - A number as the decision criteria of test values
        + Output: `True` or `False` indcating whether a patient has ever been sick

* `parse_data` reads and parses the data files into a SQL database.
    - Input: 
        + A path to a `.txt` file storing patient information where the first column is the patient ID. 
        + A path to a `.txt` file storing lab information of patients where the first column is the patient ID. 
        + A path to a database
    - Output: This function doesn't return any value. Instead, it populates a SQL database with patient and lab information in the background. The database is updated based on the data provided as input to the function, and no direct output is generated.

* `date_type_conversion` converts date in string format to datetime format. It is used internally in `age` and `age_at_first_admission` methods.
    - Input: date of birth in string format
    - Output: date of birth in date format


### Examples
```python
>> from main import parse_data, Patient
>> parse_data("patient_file_name.txt", "labs_file_name.txt", "SampleDB.db")

>> patient = Patient("1A8791E3-A61C-455A-8DEE-763EB90C9B2C", "SampleDB.db")
>> patient.age
50

>>> patient.age_at_first_admission
19

>> patient.is_sick("<","URINALYSIS: RED BLOOD CELLS",1.5)
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
