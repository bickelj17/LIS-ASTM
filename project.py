#goes to the LIS result file and reads the third line from it
with open('lis_result.txt', 'r') as file:
    result = file.readlines()[2:13]
    #print('\n', result, '\n')

#converts the class from list to string
separator = ""
result = separator.join(result)

#Checking the first line of the message and printing out the relevant info
result = result.split('|')
#print('\n', result, '\n')

if (result[0].endswith('1H') and result[1]==r'\^&' and result[2]=='' and result[3]==''):
    pass
else:
    print('Beginning of the first line of the LIS message is configured incorrectly','\n')

if (len(result[4])==14 and result[5]==result[6]==result[7]==result[8]==result[9]==result[10]==''):
    pass
else:
    print('Middle of the first line of the LIS message is configured incorrectly','\n')

if (result[11]=='P' and result[12].replace(".", "").isnumeric() and result[13][0:14].isnumeric()):
    pass
else:
    print('End of the first line of the LIS message is configured incorrectly','\n')

print('Serial Number is:',result[4].removeprefix('Sofia^'))
print('FW is:',result[12])

creation_time=''
for char in result[13]:
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


#now checking the second relevant line of code
if ('2P' == result[13][-2:]):
    pass
else:
    print('Second line does not start with "2P"')

if(result[14]=='1'):
    pass
else:
    print('Section 13 does not equal 1')

if (len(result[15]))<21:
    print('Patient ID:',result[15])
else:
    print('Patient ID length too long')

#checks sections 16-37 for blank spaces
blank=16
while blank <38:
    if result[blank]=='':
        pass
    else:
        print('On the second line at position', blank, ' there is a "', result[blank], '"string where there should be nothing')
    blank+=1


site_name=''
for char in result[38]:
    if char == '[':                    #iterates through the long version of result[38]
        break
    site_name += char
if (len(site_name))<31:               #checks that site name is less than 30 characters
    print('Site Name:',site_name)
else:
    print('Site name is too long')

#now checking the third line
if ('3O' == result[38][-2:]):
    pass
else:
    print('Third line does not start with "3O"')

if(result[39]=='1'):
    pass
else:
    print('Section 39 does not equal 1')

if (len(result[40]))<21:               #checks that order number is less than 20 characters
    print('Order Number:',result[40])
else:
    print('Order Number is too long')

cassette_lot=''
cassette_expiry=''
for char in result[41]:
    if char == '^':                    #iterates forward through result[41] and sets cassette lot#
        break
    cassette_lot += char
for char in reversed(result[41]):
    if char == '^':                    #iterates backwards through result[41] and sets cassette expiry date (backwards though, gotta flip it later)
        break
    cassette_expiry += char
cassette_expiry=cassette_expiry[::-1]
if (len(cassette_expiry)!=8):
    print('cassette expiration date has incorrect number of characters')
print("Cassette Lot:", cassette_lot)
print("Cassette expiry: ", cassette_expiry[4:6],'/',cassette_expiry[6:8],'/',cassette_expiry[0:4],sep='')


assay=result[42]
print('Assay short name:',assay)


blank=43
while blank <53:
    if result[blank]=='' or result[blank]==result[48]:        #checks for blanks
        pass
    else:
        print('On the third line at position', blank, ' there is a "', result[blank], '"string where there should be nothing')
    blank+=1

user_id=result[48]
print('User ID:',user_id)

test_type=''
for char in result[53]:
    if char == '[':                    #iterates through the long version of result[38]
        break
    test_type += char
if(test_type=='P'):
    print('Test type: Patient')

if (len(test_type))!=1:
    print('test type is incorrect')             #checks that test type equals 1 character


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




