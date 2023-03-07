# EHR Data Analysis

The ehr-utils library provides some simple analytical capabilities for EHR data.

***For end users:***

1. Input File Requirements:
    * File should be provided in `.txt` format and always include a header at the first row position. The first column of the file should be Patient IDs.
    * Please ensure there is no duplicative records in the files.
    * When calling any the functions, please ensure that the following are provided in string format:
        - File Name
        - Patient ID
        - Test Name
        - Operator
2. Installation Instruction
Run `pip install --upgrade pip && pip install -r requirements.txt` to set up your local enviroment to run the file. To run the file, execute `python main.py`. 

3. Details of Each Function
The `main.py` includes three main functions and two helper functions:
    * `parse_data` reads and parses the data files.
    ```python
    >> patient_records, lab_records = parse_data("patient_file_name.txt", "labs_file_name.txt")
    ```
    * `date_type_conversion` converts date in string format to datetime format. It is used internally in `patient_age` method.
    ```python
    >> dob_string = "1947-12-28 02:45:40.547"
    >> DOB = date_type_conversion(dob_string)
    1947-12-28 02:45:40.547000
    ```
    * `patient_age` calculates the age in years of a given patient. 
    ```python
    >> patient_is_sick(records, "1A8791E3-A61C-455A-8DEE-763EB90C9B2C", "METABOLIC: ALBUMIN", ">", 4.0)
    True
    ```
    * `search_test_results`
    ```python
    >> ssearch_test_results(lab_records, "FB2ABB23-C9D0-4D09-8464-49BF0B982F0F", "URINALYSIS: RED BLOOD CELLS")
    [3.1, 0.8, 1.1, 2.7, 0.1, 1.4, 2.7, 1.9, 1.9, 3.3, 2.7, 2.2, 0.9, 0.5, 1.9, 1.9, 2.2, 0.4]
    ```
    * `patient_is_sick`
    ```python
    >> patient_is_sick(lab_records,"1A8791E3-A61C-455A-8DEE-763EB90C9B2C", "URINALYSIS: RED BLOOD CELLS", "<", 1.5)
    False
    ```


***For conntributors:***

Please follow the instruction above to set up your environment.  

To run pytest and check test coverage, run the following code in terminal: 
```
pytest main_test.py
coverage run -m pytest main_test.py > test_report.txt
coverage report -m
```
