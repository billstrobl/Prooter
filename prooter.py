#!/usr/bin/env python3
########################################################################################################################
#
# PRooter.py
#
# Searches through HTML posts to find names, usernames, and posts. Creates an output that can be used elsewhere.
#
# Notes: This script relies on having the data locally available.
# Future versions may include allowing remote source urls.
# Specify the correct path to your data in the path var on line 17.
########################################################################################################################

import os
import re
import pprint as pp

PATH = (str(os.path.dirname(os.path.realpath(__file__))) + '/data/')
OUTPUT_PATH = (str(os.path.dirname(os.path.realpath(__file__))) + '/results/result.txt')

def get_file_list():
    this_file_list = []
    for root, dirs, files in os.walk(PATH):
        for file in files:
            this_file_list.append(str(file))
            print('\nAdded {} to scan list.'.format(str(file)))
    print('\nFile list complete!')
    return this_file_list


def check_files(list_to_check):
    print('\nStarting file scan . . .')
    results_list = []

    for this_filename in list_to_check:
        print("\nChecking {} . . .\n".format(this_filename))
        with open(str(PATH) + this_filename, encoding="utf8") as this_file:
            data = this_file.read()
            author_name_list = re.findall('(?:<span class="author--name">)(.*)(?:</span>)', data)
            author_username_list = re.findall('(?:<span class="author--username">)(.*)(?:</span>)', data)

        for j in range(len(author_name_list)):
            data_dict = {'name': author_name_list[j], 'username': author_username_list[j]}
            results_list.append(data_dict)

    print("######################################\n")
    print("      !! SCANNING COMPLETE !!         \n")
    print("######################################\n")
    pp.pprint(results_list)
    print("\n######################################\n")

    return results_list


def output_results(this_result):
    print('\nSaving results to {}'.format(OUTPUT_PATH))
    with open(str(OUTPUT_PATH), 'w+', encoding="utf8") as this_output:
        this_output.write(str(this_result))


if __name__ == '__main__':
    file_list = get_file_list()
    results = check_files(file_list)
    output_results(results)
