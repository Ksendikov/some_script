#!/usr/bin/python3

import xml.etree.ElementTree as ET
import sys


#Enter the initial data
FILE_EXTENSIONS = 'locale.xml'
SORT_ATTRIBUTE = input ('Enter the name of the attribute (alias, version, tag): ')
ATTRIBUTES = ('alias', 'tag', 'version')

TREE = ET.parse(FILE_EXTENSIONS)
ROOT = TREE.getroot()


def check_attribute(attribute):
    # check user-entered attribute for spelling errors
    if attribute in ATTRIBUTES:
        return attribute
    else:
        return sys.exit('You entered an invalid value')


def sortchildrenby(parent, attr):
    #We sort the received data
    parent[:] = sorted(parent, key=lambda child: child.get(attr))
    return parent


def iterating_root_file(root_file, attribute):
    #Iterate root file and send data to function sortchildrendy
    for strings in root_file:
        for string in strings:
            sortchildrenby(string, attribute)



def main():
    attribute = check_attribute(SORT_ATTRIBUTE)
    iterating_root_file(ROOT, attribute)
    TREE.write('sorting_version.xml')

if __name__ == '__main__':

    main()