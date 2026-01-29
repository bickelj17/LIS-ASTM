import re

def scrape_lines(file):
    array=[]
    for line in file:
        if (file.index(line)%2)==0 and file.index(line)>0 and file.index(line) < len(file)-2:  #adds all the relevant lines of the result to an array
            array.append(line)
    
    
    for i in list(range(len(array))):        #breaks each line of the result into its individual pieces of data
        array[i]=array[i].split('|')
    
    return array

def check_line_1(result):
    reporting_array_1=[]
    if (result[0][0].endswith('1H') and result[0][1]=='\\^&' ): 
        pass
    else:
        print('Beginning of the first line of the LIS message is configured incorrectly','\n')
    if (result[0][2]==result[0][3]==result[0][5]==result[0][6]==result[0][7]==result[0][8]==result[0][9]==result[0][10]==''):
        pass
    else:
        print("there are values where blank spaces should be")
    if(len(result[0][4])!=14):
        print("serial number configured incorrectly")
    if (result[0][11]=='P' or result[0][11]=='Q' or result[0][11]=='C'):
        pass
    else:
        print("test identifier is incorrect")
    if (result[0][12].replace(".", "").isnumeric() and result[0][13][0:14].isnumeric()):
        pass
    else:
        print('FW or date are configured incorrectly','\n')
    
    print('Serial Number is:',result[0][4].removeprefix('Sofia^'))
    x='Serial Number is:',result[0][4].removeprefix('Sofia^')
    reporting_array_1.append(x)
    print(reporting_array_1)
    print('FW is:',result[0][12])
    
    creation_time=''
    for char in result[0][13]:
        if char == '[':                    #iterates through the long version of result[13]
            break
        creation_time += char

    if (len(creation_time))!=14:               #checks that creation date/time is exactly 15 characters
        print('Message creation date and time incorrect length')
    else:
        #print('Message created: ',creation_time[4:6],'/', creation_time[6:8],'/',creation_time[0:4], ' at ', creation_time[8:10],':',creation_time[10:12], ' UTC',sep='')
        if(int(creation_time[8:10])>12):
            print('Message created: ',int(creation_time[8:10])-20,':',creation_time[10:12], ' Local PST',sep='')
        else:
            print('Message created: ',int(creation_time[8:10])-8,':',creation_time[10:12], ' Local PST',sep='')
    return reporting_array_1





def check_line_2(result):
    if ('2P' == result[1][0][-2:]):
        pass
    else:
        print('Second line does not start with "2P"')

    if(result[1][1]=='1'):
        pass
    else:
        print('Section 13 does not equal 1')
    
    if (len(result[1][2]))<21:
        print('Patient ID:',result[1][2])
    else:
        print('Patient ID length too long')

    blank=3
    while blank <25:
        if result[1][blank]=='':
            pass
        else:
            print('On the second line at position', blank, ' there is a "', result[1][blank], '"string where there should be nothing')
        blank+=1
    
    site_name=''
    for char in result[1][25]:
        if char == '[':                    #iterates through the long version of result[38]
            break
        site_name += char
    if (len(site_name))<31:               #checks that site name is less than 30 characters
        print('Site Name:',site_name)
    else:
        print('Site name is too long')
    return


def check_line_3(result):
    if ('3O' == result[2][0][-2:]):
        pass
    else:
        print('Third line does not start with "3O"')

    if(result[2][1]=='1'):
        pass
    else:
        print('Section 39 does not equal 1')

    if (len(result[2][2]))<21:               #checks that order number is less than 20 characters
        print('Order Number:',result[2][2])
    else:
        print('Order Number is too long')

    cassette_lot=''
    cassette_expiry=''
    for char in result[2][3]:
        if char == '^':                    #iterates forward through result[41] and sets cassette lot#
            break
        cassette_lot += char
    for char in reversed(result[2][3]):
        if char == '^':                    #iterates backwards through result[41] and sets cassette expiry date (backwards though, gotta flip it later)
            break
        cassette_expiry += char
    cassette_expiry=cassette_expiry[::-1]
    if (len(cassette_expiry)!=8):
        print('cassette expiration date has incorrect number of characters')
    print("Cassette Lot:", cassette_lot)
    print("Cassette expiry: ", cassette_expiry[4:6],'/',cassette_expiry[6:8],'/',cassette_expiry[0:4],sep='')

    assay=result[2][4]
    print('Assay short name:',assay)

    blank=5
    while blank <15:
        if result[2][blank]=='' or result[2][blank]==result[2][10]:        #checks for blanks
            pass
        else:
            print('On the third line at position', blank, ' there is a "', result[2][blank], '"string where there should be nothing')
        blank+=1

    user_id=result[2][10]
    print('User ID:',user_id)

    test_type=''
    for char in result[2][15]:
        if char == '[':                    #iterates through the long version of result[38]
            break
        test_type += char
    if(test_type=='P'):
        print('Test type: Patient')

    if (len(test_type))!=1:
        print('test type is incorrect')             #checks that test type equals 1 character


#BEGIN
'''with open('LIS_result.txt', 'r', encoding='utf-8-sig') as file:
    result = file.readlines()

result = scrape_lines(result)
check_line_1(result)
check_line_2(result)
check_line_3(result)
'''

'''



    #now checking the fourth line
    if ('4C' == result[53][-2:]):
        pass
    else:
        print('Fourth line does not start with "4C"')

    if(result[54]=='1'):
        pass
    else:
        print('Section 54 does not equal 1')



    if(result[55]==''):
        pass
    else:
        print('Section 55 does not equal ""')

    test_mode=''
    for char in result[56]:
        if char == '[':                    #iterates through the long version of result[56]
            break
        test_mode += char
    if(test_mode == 'Read-Now Mode' or test_mode=='Walk Away Mode'):
        print('Test mode:' , test_mode)
    else:
        print('Test mode incorrect')


    #now checking the fith line
    if ('5R' == result[56][-2:]):
        pass
    else:
        print('Fith line does not start with "5R"')

    if(result[57]=='1'):
        pass
    else:
        print('Section 57 does not equal 1')

    analyte_1_name=''
    for char in reversed(result[58]):
        if char == '^':                    #iterates backwards through result[58] and sets analyte name (backwards though, gotta flip it later)
            break
        analyte_1_name += char
    analyte_1_name=analyte_1_name[::-1]
    print(analyte_1_name,'= ',end='')

    analyte_1_result=result[59]
    print(analyte_1_result)

    blank=60
    while blank <68:
        if result[blank]=='' or result[blank]==result[64]:        #checks for blanks
            pass
        else:
            print('On the fith line at position', blank, ' there is a "', result[blank], '"string where there should be nothing')
        blank+=1

    test_result_type=result[64]
    if test_result_type == ('F' or 'R'):       #test test result type ie if its retransmitted or final
        pass
    else:
        print('test result type incorrect')


    test_time=''
    for char in result[68]:
        if char == '[':                    #iterates through the long version of result[56]
            break
        test_time += char
    #print(test_time)
    if (len(test_time))!=14:               #checks that execution date/time is exactly than 15 characters
        print('Test execution date and time incorrect length')
    else:
        #print('Test executed at: ',test_time[4:6],'/', test_time[6:8],'/',test_time[0:4], ' at ', test_time[8:10],':',test_time[10:12], ' UTC',sep='')
        #print(int(test_time[8:10])-8,':',test_time[10:12], ' Local PST 24H',sep='')
        if(int(test_time[8:10])>12):
            print('Test executed at: ',int(test_time[8:10])-20,':',test_time[10:12], ' Local PST',sep='')
        else:
            print('Test executed at: ',int(test_time[8:10])-8,':',test_time[10:12], ' Local PST',sep='')

    #checking the sixthline now
    if ('6L' == result[68][-2:]):
        pass
    else:
        print('Sixth line does not start with "6L"')


    if(result[69]=='1'):
        pass
    else:
        print('Section 69 does not equal 1')

    if(result[70][0]=='N'):
        pass
    else:
        print('Section 70 does not equal "N"')

    '''