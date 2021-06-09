#!/usr/bin/python3

import os
import xml.etree.ElementTree as ET

FILE_EXTENSIONS = 'xml'

def return_preview_file():
    #in the folder where the script is running, we search for the
    # file preview_graphics.xml and return the path to it
    levels_list = []
    for root, subfolders, files in os.walk(os.getcwd()):
        for file in files:
            if file == 'preview_graphics.xml':
                levels_list.append((os.path.join(root, file)))
    return levels_list


def get_files():
    # in the folder where the script was requested, we perform a recursive
    # search for elements with the xlm extension and return their paths
    path_to_the_file = []
    for root, subfolders, files in os.walk(os.getcwd()):
        for file in files:
            if file.split('.')[-1] in FILE_EXTENSIONS:
                path_to_the_file.append(os.path.join(root, file))
    for element in path_to_the_file:
        if 'preview_graphics.xml' in element.split('/'):
            path_to_the_file.remove(element)
    return path_to_the_file


def looking_for_alias(path_file):
    #search for alias values in the specified path and merge them into a
    #dictionary {alias value: path}
    general_dict = {}
    for string in path_file:
        iter_file = []
        parse_files = ET.parse(string)
        root_file = parse_files.getroot()
        iter_file.append(root_file.iter('Sprite'))
        for strings in iter_file:
            elements_alias = set()
            for alias in strings:
                elements_alias.add(alias.attrib['alias'])
            dict_element = {tuple(elements_alias): string}
            general_dict.update(dict_element)
    return general_dict


def iteration_dictionary(dictionary):
    #transform keys of dictionaries into a set
    set_keys_dictionary = set()
    for key in dictionary:
        for iter_key in key:
            set_keys_dictionary.add(iter_key)
    return set_keys_dictionary


def search_indescribable_alias(set_key_preview, set_key_levels):
    #search preview alias that are used in levels but are not described in
    #preview_graphics.xml;
    result = set_key_levels - set_key_preview
    return result


def search_indescribable_preview(set_key_preview, set_key_levels):
    #search for preview alias, which are described in preview_graphics.xml,
    #but are not used in any of the levels
    result = set_key_preview-set_key_levels
    return result

def search_name_indescribable_preview(set_key_preview, dictionary_levels):
    #levels that use alias not described in preview_graphics.xml;
    path_container = []
    name_files = []
    for key, value in dictionary_levels.items():
        for iter_key in key:
            if not iter_key in set_key_preview:
                path_container.append(value)
    for element in path_container:
        name_files.append(element.split('/')[-1])
    return name_files


def main():
    path_file = get_files()
    preview_file = return_preview_file()
    dictionary_preview = looking_for_alias(preview_file)
    set_key_preview = iteration_dictionary(dictionary_preview)
    dictionary_levels = looking_for_alias(path_file)
    set_key_levels = iteration_dictionary(dictionary_levels)
    print(search_indescribable_alias(set_key_preview, set_key_levels))
    print(search_indescribable_preview(set_key_preview,set_key_levels))
    print(search_name_indescribable_preview(set_key_preview,dictionary_levels))

if __name__ == '__main__':
    main()