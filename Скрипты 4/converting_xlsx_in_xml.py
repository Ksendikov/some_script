#!/usr/bin/python3

import openpyxl
import os
import xml.etree.ElementTree as ET


FILE_EXTENSIONS_XLSX = 'xlsx'
PARSE_FILES = ET.parse('locale.xml')
ROOT_FILES = PARSE_FILES.getroot()


def get_files_xlsx():
    # in the folder where the script was requested, we perform a recursive
    # search for elements with the xlsx extension and return their paths
    path_to_the_file_xlsx = []
    for root, subfolders, files in os.walk(os.getcwd()):
        for file in files:
            if file.split('.')[-1] in FILE_EXTENSIONS_XLSX:
                path_to_the_file_xlsx.append(os.path.join(root, file))
    return path_to_the_file_xlsx


def search_page_in_xlsx(path_book):
    #search for pages of the book with the necessary data (search_column).
    #Returning sets of found pages.
    open_book = openpyxl.open(path_book, read_only=True)
    open_book_sheet = open_book.worksheets
    search_column = ['Text ID', 'Text', 'Text Correction']
    set_page = set()
    for page in open_book_sheet:
        for cell in page:
            list_cell_values=[]
            for cell_data in cell:
                if cell_data.value in search_column:
                    list_cell_values.append(cell_data.value)
            for list_value in list_cell_values:
                if list_value in search_column:
                    set_page.add(page)

    return set_page


def search_sheet_values(set_page):
    #find sets values and output a dictionary
    #{text_id:(text), (text_correction)}
    dict_values = {}
    for page in set_page:
        for row in range(1, page.max_row+1):
            if page[row][1].value is None or page[row][1].value == 'Text ID':
                continue
            else:
                dict_elem = {page[row][1].value: (page[row][3].value, page[row][4].value)}
                dict_values.update(dict_elem)
    return dict_values


def looking_string_in_locale():
    iter_file = ROOT_FILES.iter('String')
    return iter_file


def swap_alias(iter_file, dict_values):
    set_key = set()
    set_alias = set()
    for keys in dict_values.keys():
        set_key.add(keys)
    for strings in iter_file:
        set_alias.add(strings.attrib['alias'])
        if strings.attrib['alias'] in set_key:
            if strings.text != dict_values.get(strings.attrib['alias'])[0]:
                print(f'In the source file, the old alias {strings.attrib["alias"]} '
                      f'test does not match the TEXT value')
            strings.text = dict_values.get(strings.attrib['alias'])[1]
    if len(set_key-set_alias) >0:
        print(f'The following alias are missing in locale.xml {set_key-set_alias}')


def main():
    path_xlsx = get_files_xlsx()
    page = []

    for files in path_xlsx:
        page.append(list(search_page_in_xlsx(files)))

    list_dict = []
    for found_pages in page:
        list_dict.append(search_sheet_values(found_pages))

    looking_string = looking_string_in_locale()

    for dictionary in list_dict:
        swap_alias(looking_string,dictionary)


    PARSE_FILES.write('up_locale.xml')

if __name__ == '__main__':
    main()