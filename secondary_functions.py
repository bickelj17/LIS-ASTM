import os
from base_functions import *


def test_type(file):
    test_type_value = ""
    for char in file[2][15]:
        if char == "[":  # iterates through the long version of result[38]
            break
        test_type_value += char
    if test_type_value in ("P", "Q", "C"):
        return test_type_value
    else:
        return "error"


def check_patient(file, test_type_value):
    # Parsed ASTM records are passed in as `file`.
    length = len(file)
    check_line_1(file)
    check_line_2(file, test_type_value)
    check_line_3(file, test_type_value)
    check_line_4(file)
    check_line_analyte(file, length)
    check_last_line(file, length)
    print("Patient test checked")


def check_qc(file, test_type_value):
    length = len(file)
    check_line_1(file)
    check_line_2(file, test_type_value)
    check_line_3(file, test_type_value)
    check_line_4(file)
    check_line_analyte(file, length)
    check_last_line(file, length)
    print("QC test checked")


def check_calibration(file, test_type_value):
    length = len(file)
    check_line_1(file)
    check_line_2(file, test_type_value)
    check_line_3(file, test_type_value)
    check_line_calibration(file)
    check_last_line(file, length)
    print("Calibration test checked")


# BEGIN
if __name__ == "__main__":
    # Simple CLI test when running this file directly
    with open("LIS_result.txt", "r", encoding="utf-8-sig") as file:
        result = file.readlines()

    result = scrape_lines(result)
    t = test_type(result)
    if t == "P":
        check_patient(result, t)
    elif t == "Q":
        check_qc(result, t)
    elif t == "C":
        check_calibration(result, t)
    