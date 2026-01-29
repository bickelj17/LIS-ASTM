import os
from base_functions import *

def check_patient(file):
    reporting_array_2=[]
    reporting_array_2.append(check_line_1(file))
    #check_line_2(file)
    print("patient test checked")

    return reporting_array_2
    

#BEGIN
with open('LIS_result.txt', 'r', encoding='utf-8-sig') as file:
    result = file.readlines()

result = scrape_lines(result)
check_patient(result)