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
from lxml import html
import pprint as pp

PATH = (str(os.path.dirname(os.path.realpath(__file__))) + '/data/')
OUTPUT_PATH = (str(os.path.dirname(os.path.realpath(__file__))) + '/results/')


def get_file_list():
    this_file_list = []
    for root, dirs, files in os.walk(PATH):
        for file in files:
            this_file_list.append(str(file))
            #print('\nAdded {} to scan list.'.format(str(file)))
    #print('\nFile list complete!')
    return this_file_list


def check_files(list_to_check, run_type):
    #print('\nStarting file scan . . .')
    results_list = []

    for this_filename in list_to_check:
        #print("\nChecking {} . . .\n".format(this_filename))
        with open(str(PATH) + this_filename, encoding="utf8") as this_file:
            data = this_file.read()
            build_result_struct(data, results_list, run_type)

    #print("######################################\n")
    #print("      !! SCANNING COMPLETE !!         \n")
    #print("######################################\n")
    pp.pprint(results_list)
    #print("\n######################################\n")
    return results_list


def build_result_struct(data, results_list, run_type):
    post_list = []
    name_list = re.findall('(?:<span class="author--name">)(.*)(?:</span>)', data)
    username_list = re.findall('(?:<span class="author--username">)(.*)(?:</span>)', data)

    if run_type == 'posts':
        parser = html.HTMLParser(encoding='utf-8')
        root = html.fromstring(data, parser=parser)
        post_list = root.cssselect('div.card--body')

    for j in range(len(name_list)):
        if run_type == 'users':
            data_dict = {'name': name_list[j], 'username': username_list[j]}
            if data_dict not in results_list:
                results_list.append(data_dict)
        elif run_type == 'posts':
            data_dict = {'name': name_list[j], 'username': username_list[j]}
            try:
                data_dict['post'] = post_list[j].text_content().replace("\n", "").strip()
            except IndexError:
                continue
            results_list.append(data_dict)


def get_output_filename(run_type):
    if run_type == 'users':
        this_filename = 'users_result.txt'
    elif run_type == 'posts':
        this_filename = 'posts_result.txt'
    else:
        this_filename = 'results.txt'
    return this_filename


def output_results(this_result, filename):
    print('\nSaving results to {}'.format(OUTPUT_PATH+filename))
    with open(str(OUTPUT_PATH)+filename, 'w+', encoding="utf8") as this_output:
        this_output.write(str(this_result))


if __name__ == '__main__':
    file_list = get_file_list()
    output_results(check_files(file_list, 'users'), get_output_filename('users'))
    output_results(check_files(file_list, 'posts'), get_output_filename('posts'))
