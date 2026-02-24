import os
from base_functions import *


def check_patient(file):
    check_line_1(file)
    check_line_2(file)
    check_line_3(file)
    check_line_4(file)
    check_line_5(file)
    check_line_6(file)
    print("patient test checked")



# BEGIN
if __name__ == "__main__":
    # Simple CLI test when running this file directly
    with open("LIS_result.txt", "r", encoding="utf-8-sig") as file:
        result = file.readlines()

    result = scrape_lines(result)
    check_patient(result)