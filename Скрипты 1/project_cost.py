#!/usr/bin/python3

import os
import xml.etree.ElementTree as ET
import re


#Search for files with the extension specified in []
FILE_EXTENSIONS = 'xml'

WORD_COST = 0.05 #word cost $


def get_files():
    # Searching for files with the extension 'file_extensions'
    texts = []
    for root, subfolders, files in os.walk(os.getcwd()):
        for file in files:
            if file.split('.')[-1] in FILE_EXTENSIONS:
                texts.append(os.path.join(root, file))
    return texts


def parsing_files(texts):
    # iterating over files by String and outputting text content to set
    iter_texts = []
    setting_element_texts = set()
    parser_texts = ET.parse(texts)
    root_texts = parser_texts.getroot()
    iter_texts.append(root_texts.iter('String'))
    for value in iter_texts:
        for string in value:
            setting_element_texts.add(string.text)
    return setting_element_texts


def container(union_set):
    # count the words in the resulting combined set
    word_list = []
    for listing in union_set:
        for words in listing.split():
           word_list.append(words)
    return word_list


def main():
    texts = get_files()

    union_set_all_found_elements = set()
    for text in texts:
        for element in parsing_files(text):
            union_set_all_found_elements.add(element)

    delete_links=set()
    for strings in union_set_all_found_elements:
        link_search = re.sub(r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]
         {7} +|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]|[^A-Za]))''',
                     '', str(strings))
        delete_links.add(link_search)

    word_list = float(len(container(delete_links)))

    return int(word_list * WORD_COST)

if __name__ == '__main__':
    print(main())