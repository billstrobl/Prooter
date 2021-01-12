#############################################################
#
# ParlerRooter.py
#
# Search through posts from Parler to find real and usernames
#
# Notes: This script relies on having the data locally available.
# Future versions may include allowing remote source urls.
# Specify the correct path to your data in the path var on line 17.
#############################################################

import os
import re
import pprint as pp
from pathlib import Path

PATH = Path('./data')


def get_file_list():
    this_file_list = []
    for root, dirs, files in os.walk(PATH):
        for file in files:
            this_file_list.append(str(file))
            print('Added ' + str(file) + 'to scan list.')
    return this_file_list


def check_files(list_to_check):
    print('\n\nScanning File List . . .\n\n')
    data_list = []

    for i in list_to_check:
        this_filename = i
        pp.pprint("Checking " + this_filename + ". . .")
        with open('./data/' + this_filename, encoding="utf8") as this_file:
            data = this_file.read()
            author_name_list = re.findall('(?:<span class="author--name">)(.*)(?:</span>)', data)
            author_username_list = re.findall('(?:<span class="author--username">)(.*)(?:</span>)', data)

        for j in range(len(author_name_list)):
            data_dict = {'name': author_name_list[j], 'username': author_username_list[j]}
            data_list.append(data_dict)

        pp.pprint("File scanned.")

    pp.pprint("##############################################")
    pp.pprint("!! SCANNING COMPLETE !!")
    pp.pprint("##############################################")
    pp.pprint(data_list)
    pp.pprint("##############################################")


if __name__ == '__main__':
    file_list = get_file_list()
    check_files(file_list)
