# -*- coding: utf-8 -*-
import sys
import csv
import os

# globalizes header for corporate client and client

header_corporate = [
    "id",
    "name",
    "tel_number_1",
    "tel_number_2",
    "e_mail_address_1",
    "e_mail_address_2",
    "zip_code",
    "address_1",
    "address_2",
    "address_3",
    "address_4",
    "nearest_station",
    "business_category",
    "officer_name",
    "department",
    "role",
    "memo",
    "created_by",
    "updated_by",
    "created_at",
    "updated_at",
    "deleted"
]
header_client = [
     "id",
     "last_name",
     "first_name",
     "last_name_kana",
     "first_name_kana",
     "line_user_id",
     "verify_code",
     "tel_number_1",
     "tel_number_2",
     "e_mail_address_1",
     "e_mail_address_2",
     "zip_code",
     "address_1",
     "address_2",
     "address_3",
     "address_4",
     "gender",
     "date_of_birth",
     "memo",
     "created_by",
     "updated_by",
     "created_at",
     "updated_at",
     "deleted",
     "fax_number",
     "age",
     "profession",
     "station_of_employment",
     "employment"
]

def get_input_array(input_file):
    '''
    reads input_file and appends into array.
    '''
    input_array = []
    with open(input_file, 'rU', encoding="utf-8") as input_file:
        reader = csv.reader(input_file)
        for row in reader:
            input_array.append(row)
    return input_array

def get_cleaned_array(input_array):
    """ input is input_array
    output is cleaned_array
    only append rows with len 36 into cleaned_array
    """
    LENGTH = 36
    cleaned_array = []
    for row in input_array:
        if len(row) == LENGTH:
            cleaned_array.append(row)
    return cleaned_array

def separate_array(cleaned_array):
    """ input is cleaned_array
    outputs are corporate_array and client_array
    """
    SEPARATION_INDEX = 33
    corporate_array = []
    client_array = []
    for row in cleaned_array:
        if row[SEPARATION_INDEX] == 'hojin':
            corporate_array.append(row)
        else:
            client_array.append(row)
    return corporate_array, client_array

def convert_client_row(row):
    ''' input is row
    this function creates a dictionary for origin data and converts most of them into
    m_client form. New dictionary are created to convert from integers to string (tbl_age and tbl_shokugyou)
    returns output_client_array as an output.
    '''
    output_client_array = []
    client_dict = {}
    '''
    MAGIC NUMBER GLOSSARY
    '''
    client_index = {
        'FIRST_NAME': 3,
        'LAST_NAME': 2,
        'FIRST_NAME_KANA': 5,
        'LAST_NAME_KANA': 4,
        'TEL_NUMBER_1': 18,
        'TEL_NUMBER_2': 17,
        'E_MAIL_ADDRESS_1':20,
        'ZIP_CODE': 13,
        'ADDRESS_1': 14,
        'ADDRESS_2': 15,
        'ADDRESS_4': 16,
        'GENDER': 6,
        'BIRTH_YEAR': 8,
        'BIRTH_MONTH': 9,
        'BIRTH_DATE': 10,
        'MEMO': 35,
        'FAX_NUMBER': 19,
        'AGE': 7,
        'PROFESSION': 11,
        'EMPLOYMENT': 32,
        #origin data from here
        'CUSTOMER_ID': 0,
        'CUSTOMER_RANK': 1,
        'SHOKUGYOU_OTHER': 12,
        'NAME_HOJIN': 21,
        'FURIGANA_HOJIN': 22,
        'ZIP_HOJIN': 23,
        'ADDRESS_KEN_HOJIN': 24,
        'ADDRESS_SHIKU_HOJIN': 25,
        'ADDRESS_BUILDING_HOJIN':26,
        'TEL_HOJIN': 27,
        'TEL_RENRAKU': 28,
        'KEITAI_RENRAKU': 29,
        'FAX_RENRAKU': 30,
        'EMAIL_RENRAKU': 31,
        'KOJIN_HOJIN': 33,
        'B1KEIZOKU': 34,

    }

    profession_dict = {
        '10' : '学生',
        '15' : '会社員',
        '20' : '個人事業主',
        '25' : '公務員',
        '30' : '会社役員',
        '35' : '派遣社員',
        '40' : 'アルバイト',
        '45' : '無職',
        '99' : 'その他',
        ''   : ''
    }

    age_dict = {
        '10': '10代',
        '15': '20代前半',
        '17': '20代後半',
        '20': '30代前半',
        '22': '30代後半',
        '25': '40代',
        '30': '50代',
        '35': '60代',
        '0'  : ''

    }

    # initialize client_dict
    for header_name in header_client:
        origin_index = client_index.get(header_name.upper())
        if origin_index:
            client_dict[header_name] = row[origin_index]
        else:
            client_dict[header_name] = ''

    # convert gender into m_client format
    if row[client_index['GENDER']] == '男':
        client_dict['gender'] = 'M'
    elif row[client_index['GENDER']] == '女':
        client_dict['gender'] = 'W'
    else:
        client_dict['gender'] = ''

    # convert profession into m_client format
    temp_profession = row[client_index['PROFESSION']]
    client_dict['profession'] = profession_dict[temp_profession]

    # convert age into m_client format
    temp_age = row[client_index['AGE']]
    client_dict['age'] = age_dict[temp_age]

    # convert birth date into m_client format
    if (row[client_index['BIRTH_YEAR']]=='0' or
        row[client_index['BIRTH_MONTH']]=='0'  or
        row[client_index['BIRTH_DATE']]=='0'):
        client_dict['date_of_birth'] = ''
    else:
        client_dict['date_of_birth'] = row[client_index['BIRTH_YEAR']] + '-' + row[client_index['BIRTH_MONTH']] + '-' + row[client_index['BIRTH_DATE']]

    # convert memo into m_client format
    temp_memo = row[client_index['MEMO']]
    memo_job = row[client_index['SHOKUGYOU_OTHER']]
    memo_job_place = row[client_index['EMPLOYMENT']]
    if row[client_index['MEMO']] == '\\N':     
        client_dict['memo'] = temp_memo.replace('\\N', 'その他の仕事: ' + memo_job + ' 職業場所: ' + memo_job_place)
    else: 
        client_dict['memo'] = temp_memo.replace(temp_memo, temp_memo + ' ' + 'その他の仕事: ' + memo_job + ' 職業場所: ' + memo_job_place)

     # add header for csv, matching m_client
    for header_name in header_client:
        output_client_array.append(client_dict[header_name])    
    return output_client_array

def convert_corporate_row(row):
    ''' input is row
    this function creates a dictionary for origin data and converts most of them into
    m_corporate_client form.
    returns output_corporate_array as an output.
    '''
    output_corporate_array = []
    corporate_dict = {}
    '''
    MAGIC NUMBER GLOSSARY
    '''
    corporate_index = {
        #corporate_dict data from here
        'NAME': 21,
        'TEL_NUMBER_1': 27,
        'TEL_NUMBER_2': 29,
        'E_MAIL_ADDRESS_1':31,
        'FAX_NUMBER': 30,
        'ZIP_CODE': 23,
        'ADDRESS_1': 24,
        'ADDRESS_2': 25,
        'ADDRESS_4': 26,
        'NEAREST_STATION': 32,
        'BUSINESS_CATEGORY': 11,
        'OFFICER_NAME': 34,
        'DEPARTMENT': 33,
        'ROLE': 7,
        'MEMO': 35,
        #rest of origin data from here
        'CUSTOMER_ID': 0,
        'CUSTOMER_RANK': 1,
        'FIRST_NAME': 3,
        'LAST_NAME': 2,
        'FIRST_NAME_KANA': 5,
        'LAST_NAME_KANA': 4,
        'GENDER': 6,
        'BIRTH_YEAR': 8,
        'BIRTH_MONTH': 9,
        'BIRTH_DATE': 10,
        'EXTRA_FAX_NUMBER': 19,
        'OFFICER_ADDRESS_1': 13,
        'OFFICER_ADDRESS_2': 14,
        'OFFICER_ADDRESS_3': 15,
        'SHOKUGYOU_OTHER': 12,
        'FURIGANA_HOJIN': 22,
        'ADDRESS_KEN_HOJIN': 19,
        'OTHER_CONTACT_1': 18,
        'OTHER_CONTACT_2':17,
        'TEL_HOJIN': 16,
        'TEL_RENRAKU': 28,
        'EMAIL': 20,
        'B1KEIZOKU': 34,
    }

    for header_name in header_corporate:
        origin_index = corporate_index.get(header_name.upper())
        if origin_index:
            corporate_dict[header_name] = row[origin_index]
        else:
            corporate_dict[header_name] = ''

    # parametrize officer names, contacts, and their addresses
    kanji_name = row[corporate_index['LAST_NAME']] + row[corporate_index['FIRST_NAME']]
    furigana_name = row[corporate_index['LAST_NAME_KANA']] + row[corporate_index['FIRST_NAME_KANA']]
    contact_line = row[corporate_index['OTHER_CONTACT_1']] + ', '+ row[corporate_index['OTHER_CONTACT_2']]
    email = row[corporate_index['EMAIL']]
    address_line = row[corporate_index['OFFICER_ADDRESS_1']] + ' '+ row[corporate_index['OFFICER_ADDRESS_2']] + ' '+ row[corporate_index['OFFICER_ADDRESS_3']]

    # check if name is blank, replace it with officer name if it is
    if row[corporate_index['NAME']] == '':
        corporate_dict['name'] = kanji_name + ' (' + furigana_name + ')'

    # convert officer_name into m_corporate format
    temp_officer = row[corporate_index['OFFICER_NAME']]
    corporate_dict['officer_name'] = temp_officer.replace('t',kanji_name + '(' + furigana_name + ')')

    # convert department into m_corporate format
    temp_department = row[corporate_index['DEPARTMENT']]
    corporate_dict['department'] = temp_department.replace('hojin', '')

    # convert tel_number_1, zip_code, address_1 , address_2, address_4 into m_corporate format
    N_replace_array = ['tel_number_1', 'zip_code', 'address_1', 'address_2', 'address_4']
    for key_name in N_replace_array:
        temp_val = row[corporate_index[key_name.upper()]]
        corporate_dict[key_name] = temp_val.replace('\\N', '')

    # convert memo into m_corporate format
    if row[corporate_index['MEMO']] == '\\N':
        temp_memo = row[corporate_index['MEMO']]
        corporate_dict['memo'] = temp_memo.replace('\\N', 'その他連絡: ' + contact_line + ' メール: ' + email + ' 担当者住所: ' + address_line)
    else:
        temp_memo = row[corporate_index['MEMO']]
        corporate_dict['memo'] = temp_memo.replace(temp_memo, temp_memo + ' その他連絡: ' + contact_line + ' メール: ' + email + ' 担当者住所: ' + address_line )

    # convert business_category into m_corporate format
    temp_business_category = row[corporate_index['BUSINESS_CATEGORY']]
    corporate_dict['business_category'] = temp_business_category.replace(row[corporate_index['BUSINESS_CATEGORY']], '')

    # convert role into m_corporate format 
    temp_role = row[corporate_index['ROLE']]
    corporate_dict['role'] = temp_role.replace(row[corporate_index['ROLE']], '')

     # add header for csv, matching m_corporate_client
    for header_name in header_corporate:
        output_corporate_array.append(corporate_dict[header_name])
    return output_corporate_array

def convert_array(corporate_array, client_array):
    """ inputs are corporate_array and client_array
    outputs are converted_corporate_array and converted_client_array
    """
    converted_corporate_array = []
    converted_client_array = []
    for row in corporate_array:
        result_corporate_row = convert_corporate_row(row)
        converted_corporate_array.append(result_corporate_row)
    for row in client_array:
        result_client_row = convert_client_row(row)
        converted_client_array.append(result_client_row)
    return converted_corporate_array, converted_client_array

def array_to_csv(converted_array, output_file_name, header):
    ''' inputs converted_array, output_file_name, header
    this function simply writes header and the converted arrays into the new file.
    outputs the converted file.
    '''
    with open(output_file_name, "w") as output_file:
        csv_writer = csv.writer(output_file, delimiter=',')
        csv_writer.writerow(header)
        csv_writer.writerows(converted_array)

def main():
    # define variables
    input_file = 'input.csv'
    output_client_file = 'm_client_data.csv'
    output_corporate_file = 'm_corporate_client_data.csv'

    # read input csv
    input_array = get_input_array(input_file)

    # delete unnecessary lines
    cleaned_array = get_cleaned_array(input_array)

    # separate kojin array and hojin array
    (corporate_array, client_array) = separate_array(cleaned_array)

    # convert corporate and client array
    (converted_corporate_array, converted_client_array) = convert_array(corporate_array, client_array)

    # output array to csv
    array_to_csv(converted_corporate_array, output_corporate_file, header_corporate)
    array_to_csv(converted_client_array, output_client_file, header_client)

if __name__ == '__main__':
    main()
