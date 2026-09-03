import os
from line_checks import *


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
    print("Patient test checked")
    length = len(file)
    check_line_1(file)
    check_line_2(file, test_type_value)
    check_line_3(file, test_type_value)
    check_line_4(file)
    check_line_analyte(file, length)
    check_last_line(file, length)


def check_qc(file, test_type_value):
    print("QC test checked")
    length = len(file)
    check_line_1(file)
    check_line_2(file, test_type_value)
    check_line_3(file, test_type_value)
    check_line_4(file)
    check_line_analyte(file, length)
    check_last_line(file, length)


def check_calibration(file, test_type_value):
    print("Calibration test checked")
    length = len(file)
    check_line_1(file)
    check_line_2(file, test_type_value)
    check_line_3(file, test_type_value)
    check_line_calibration(file)
    check_last_line(file, length)


# BEGIN
if __name__ == "__main__":
    # Simple CLI test when running this file directly.
    with open("sample_results/good/LIS_result.txt", "r", encoding="utf-8-sig") as file:
        raw_lines = file.readlines()

    check_transmission_notes(raw_lines)
    result = scrape_lines(raw_lines)
    t = test_type(result)
    if t == "P":
        check_patient(result, t)
    elif t == "Q":
        check_qc(result, t)
    elif t == "C":
        check_calibration(result, t)
    