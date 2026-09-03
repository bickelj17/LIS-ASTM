import re
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

# The instrument timestamps are UTC; the lab is Pacific time. ZoneInfo knows
# the real PST/PDT switch-over dates, so this stays correct year-round
# instead of someone having to hand-flip a +7/+8 offset twice a year.
LOCAL_TZ = ZoneInfo("America/Los_Angeles")


def format_local_time(raw_utc_timestamp, label):
    """
    raw_utc_timestamp: 14-character UTC timestamp, e.g. '20260225192717'
                        (YYYYMMDDHHMMSS, no timezone info in the file itself).
    label: text to print before the value, e.g. 'Message created'.
    Converts to Pacific local time (auto-picks PST vs PDT) and prints it.
    """
    try:
        utc_dt = datetime.strptime(raw_utc_timestamp, "%Y%m%d%H%M%S").replace(tzinfo=timezone.utc)
    except ValueError:
        print(f'Error: {label} timestamp "{raw_utc_timestamp}" is not a valid date/time')
        return
    local_dt = utc_dt.astimezone(LOCAL_TZ)
    print(f'{label}: {local_dt.month:02d}/{local_dt.day:02d}/{local_dt.year} '
          f'at {local_dt.hour:02d}:{local_dt.minute:02d} Local {local_dt.tzname()}')


# The raw transmission log tags a problem frame by appending a note right
# after the frame's own [CR][ETX]<checksum>[CR][LF] bytes, e.g.:
#   ...[CR][ETX]72[CR][LF]  *Bad checksum
#   ...[CR][ETX]AE[CR][LF]  *Frame number out of sequence
# Rather than hardcoding just those two strings, this matches the shape of
# the note itself ("[LF]" followed by "*" and free text) so any future
# note logged in the same format gets caught automatically.
TRANSMISSION_NOTE_RE = re.compile(r'\[LF\]\s*\*(?P<note>.+?)\s*$')


def check_transmission_notes(file):
    """
    Scans the raw file lines (before scrape_lines() splits them on '|') for
    an instrument/log-reported transmission problem such as a bad checksum
    or an out-of-sequence frame number, and reports every one found.
    """
    for line_number, line in enumerate(file, start=1):
        match = TRANSMISSION_NOTE_RE.search(line)
        if match:
            print('Error: Line', line_number, 'reports:', match.group('note'))


def scrape_lines(file):
    array=[]
    for idx, line in enumerate(file):        #adds all the relevant lines of the result to an array
        if (idx%2)==0 and idx>0 and idx < len(file)-2:
            array.append(line)

    for i in list(range(len(array))):        #breaks each line of the result into its individual pieces of data
        array[i]=array[i].split('|')

    return array

def check_line_1(result):
    if (result[0][0].endswith('1H') and result[0][1]=='\\^&' ): 
        pass
    else:
        print('Error: Beginning of the first line of the LIS message is configured incorrectly','\n')
    if (result[0][2]==result[0][3]==result[0][5]==result[0][6]==result[0][7]==result[0][8]==result[0][9]==result[0][10]==''):
        pass
    else:
        print("Error: there are values where blank spaces should be")
    if(len(result[0][4])!=14):
        print("Error: serial number configured incorrectly")
    if (result[0][11]=='P'):
        pass
    else:
        print("Error: test identifier is incorrect")
    if (result[0][12].replace(".", "").isnumeric() and result[0][13][0:14].isnumeric()):
        pass
    else:
        print('Error: FW or date are configured incorrectly','\n')
    
    print('Serial Number is:',result[0][4].removeprefix('Sofia^'))
    print('FW is:',result[0][12])
    
    creation_time=''
    for char in result[0][13]:
        if char == '[':                    #iterates through the long version of result[13]
            break
        creation_time += char

    if (len(creation_time))!=14:               #checks that creation date/time is exactly 15 characters
        print('Error: Message creation date and time incorrect length')
    else:
        format_local_time(creation_time, 'Message created')
    return





def check_line_2(result,test_type):
    if ('2P' == result[1][0][-2:]):
        pass
    else:
        print('Error: Second line does not start with "2P"')

    if(result[1][1]=='1'):
        pass
    else:
        print('Error: Section 13 does not equal 1')
    
    if (test_type == "P"):
        if (len(result[1][2]))<21:
            print('Patient ID:',result[1][2])
        else:
            print('Error: Patient ID length too long')
    
    if (test_type == "Q" or test_type == "C"):
        if (len(result[1][2]))<21:
            print('Cassette serial #:',result[1][2])
        else:
            print('Error: Cassette serial # length too long')
    

    blank=3
    while blank <25:
        if result[1][blank]=='':
            pass
        else:
            print('Error: On the second line at position', blank, ' there is a "', result[1][blank], '"string where there should be nothing')
        blank+=1
    
    site_name=''
    for char in result[1][25]:
        if char == '[':                    #iterates through the long version of result[38]
            break
        site_name += char
    if (len(site_name))<31:               #checks that site name is less than 30 characters
        print('Site Name:',site_name)
    else:
        print('Error: Site name is too long')
    return


def check_line_3(result,test_type):
    if ('3O' == result[2][0][-2:]):
        pass
    else:
        print('Error: Third line does not start with "3O"')

    if(result[2][1]=='1'):
        pass
    else:
        print('Error: Section 39 does not equal 1')

    if (test_type == "P"):
        if (len(result[2][2]))<21:               #checks that order number is less than 20 characters
            print('Order Number:',result[2][2])
        else:
            print('Error: Order Number is too long')
    if (test_type == "Q"):
        if (len(result[2][2]))<21:               #checks that order number is less than 20 characters
            print('Kit lot number:',result[2][2])
        else:
            print('Error: Kit lot number is too long')
    if (test_type == "C"):
        if (len(result[2][2]))<21:               #checks that order number is less than 20 characters
            print('Calibration lot Number:',result[2][2])
        else:
            print('Error: Calibration lot Number is too long')

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
        print('Error: cassette expiration date has incorrect number of characters')
    print("Cassette Lot:", cassette_lot)
    print("Cassette expiry: ", cassette_expiry[4:6],'/',cassette_expiry[6:8],'/',cassette_expiry[0:4],sep='')

    
    assay=result[2][4]
    if(test_type== "P" or test_type=="Q"):
        print('Assay short name:',assay)
    if (test_type== "C" ):
         print('Calibration short name:',assay)

    blank=5
    while blank <15:
        if result[2][blank]=='' or result[2][blank]==result[2][10]:        #checks for blanks
            pass
        else:
            print('Error: On the third line at position', blank, ' there is a "', result[2][blank], '"string where there should be nothing')
        blank+=1

    user_id=result[2][10]
    if (len(user_id))<21:
        print('User ID:',user_id)
    else:
        print('Error: User ID length too long')

    test_type=''
    for char in result[2][15]:
        if char == '[':                    #iterates through the long version of result[38]
            break
        test_type += char
    if(test_type=='P' or test_type=='Q' or test_type=='C'):
        pass
    else:
        print('Error: test type is undefined')
        

    if (len(test_type))!=1:
        print('Error: test type is incorrect')             #checks that test type equals 1 character


def check_line_4(result):
    #now checking the fourth line
    if ('4C' == result[3][0][-2:]):
        pass
    else:
        print('Error: Fourth line does not start with "4C"')

    if(result[3][1]=='1'):
        pass
    else:
        print('Error: Section 54 does not equal 1')

    if(result[3][2]==''):
        pass
    else:
        print('Error: Section 55 does not equal ""')

    test_mode=''
    for char in result[3][3]:
        if char == '[':                    #iterates through the long version of result[56]
            break
        test_mode += char
    if(test_mode == 'Read-Now Mode' or test_mode=='Walk Away Mode'):
        print('Test mode:' , test_mode)
    else:
        print('Error: Test mode incorrect')


def check_line_analyte(result, length):
    #now checking the analytes lines
    analytes = []  # collected here, printed (and S/CO-merged) after the loop
    for i in range(length-5):
        if (str(i+5) + 'R' == result[i+4][0][-2:]):
            pass
        else:
            print('Error: Line', i+5, 'does not start with "', i+5, 'R"')

        if(result[i+4][1]==str(i+1)):
            pass
        else:
            print('Error: Section 57 does not equal 1')

        analyte_1_name=''
        for char in reversed(result[i+4][2]):
            if char == '^':                    #iterates backwards through result[58] and sets analyte name (backwards though, gotta flip it later)
                break
            analyte_1_name += char
        analyte_1_name=analyte_1_name[::-1]

        analyte_1_result=result[i+4][3]
        if analyte_1_result == '':
            print('Error: Analyte result value is missing')

        blank=4
        while blank <11:
            if result[i+4][blank]=='' or result[i+4][blank]==result[i+4][8]:        #checks for blanks
                pass
            else:
                print('Error: On the fith line at position', blank, ' there is a "', result[i+4][blank], '"string where there should be nothing')
            blank+=1

        transmission_type=result[i+4][8]
        if transmission_type =='F' or transmission_type =='R':       #test test result type ie if its retransmitted or final
            pass
        else:
            print('Error: Transmission type incorrect')


        test_time=''
        for char in result[i+4][12]:
            if char == '[':                    #iterates through the long version of result[56]
                break
            test_time += char
        if (len(test_time))!=14:               #checks that execution date/time is exactly than 15 characters
            print('Error: Test execution date and time incorrect length')
            test_time = None

        analytes.append({'name': analyte_1_name, 'value': analyte_1_result, 'test_time': test_time})

    print_analytes(analytes)


def print_analytes(analytes):
    """
    Print each analyte's result, merging a companion S/CO (signal-to-
    cutoff) reading into its matching analyte instead of listing it as
    its own unrelated result. Some instruments report the numeric S/CO
    value as its own analyte line named "<analyte>_VAL" (e.g. "Legion"
    and "Legion_VAL" - see More sample/SCO ASTM for real examples).
    """
    merged = [a for a in analytes if not a['name'].endswith('_VAL')]
    for a in analytes:
        if not a['name'].endswith('_VAL'):
            continue
        base_name = a['name'][:-len('_VAL')]
        target = next((m for m in merged if m['name'] == base_name), None)
        if target is not None:
            target['sco_value'] = a['value']
        else:
            # No matching base analyte - report it on its own rather than
            # silently dropping it.
            merged.append(a)

    for a in merged:
        line = f"{a['name']} = {a['value']}"
        if a.get('sco_value') is not None:
            line += f" (S/CO {a['sco_value']})"
        print(line)
        if a['test_time']:
            format_local_time(a['test_time'], 'Test executed at')

def check_line_calibration(result):
    #now checking the calibration result line
    if ('4R' == result[3][0][-2:]):
        pass
    else:
        print('Error: Fourth line does not start with "4R"')
    
    if(result[3][1]=='1'):
        pass
    else:
        print('Error: Section 54 does not equal 1')

    analyte_1_name=''
    for char in reversed(result[3][2]):
        if char == '^':                    #iterates backwards through result[58] and sets analyte name (backwards though, gotta flip it later)
            break
        analyte_1_name += char
    analyte_1_name=analyte_1_name[::-1]
    print(analyte_1_name,'= ',end='')

    analyte_1_result=result[3][3]
    print(analyte_1_result)
    if analyte_1_result == '':
        print('Error: Analyte result value is missing')

    blank=4
    while blank <11:
        if result[3][blank]=='' or result[3][blank]==result[3][8]:        #checks for blanks
            pass
        else:
            print('Error: On the fith line at position', blank, ' there is a "', result[3][blank], '"string where there should be nothing')
        blank+=1

    transmission_type=result[3][8]
    if (transmission_type == 'F' or transmission_type == 'R'):       #test test result type ie if its retransmitted or final
        pass
    else:
        print('Error: Transmission type incorrect')


    test_time=''
    for char in result[3][12]:
        if char == '[':                    #iterates through the long version of result[56]
            break
        test_time += char
    #print(test_time)
    if (len(test_time))!=14:               #checks that execution date/time is exactly 14 characters
        print('Error: Test execution date and time incorrect length')
    else:
        format_local_time(test_time, 'Test executed at')



def check_last_line(result, length):
    #checking the the last line now


    if (str(length) + 'L' == result[length-1][0][-2:]):
        pass
    else:
        print('Error: Last line does not start with "', length, 'L"')

    if(result[length-1][1]=='1'):
        pass
    else:
        print('Error: Section 69 does not equal 1')

    if(result[length-1][2][0]=='N'):
        pass
    else:
        print('Error: Section 70 does not equal "N"')


