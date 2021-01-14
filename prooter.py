#!/usr/bin/env python3
########################################################################################################################
#
# PRooter.py
#
# Searches through HTML posts to find names, usernames, and posts. Creates an output that can be used elsewhere.
#
# This function takes two arguments from the command line. run_type and file_format.
# run_type is 'users', 'posts', or 'all' and controls what data will be parsed out from the HTML files.
# file_format sets the file extension and processing needed to correctly create that kind of file. '.txt' or '.csv'
#
# Notes: This script relies on having the data locally available. Future versions may include allowing remote sources.
# Specify the correct path to your data in the path var on line 25.
# The path for the output files is also specified on line 26.
########################################################################################################################

import os
import re
import csv
import logging
import click
from lxml import html
import pprint as pp

SOURCE_PATH = os.path.join(str(os.path.dirname(os.path.realpath(__file__))), 'data')
OUTPUT_PATH = os.path.join(str(os.path.dirname(os.path.realpath(__file__))), 'results')


def get_file_list(base_source_path):
    this_file_list = []
    for _, _, files in os.walk(base_source_path):
        for file in files:
            if str(file) == '.dummyfile':
                continue
            this_file_list.append(str(file))
            logging.debug('\nAdded {} to scan list.'.format(str(file)))
    logging.debug('\nFile list complete!')
    return this_file_list


def check_files(base_source_path, list_to_check, run_type):
    logging.debug('\nStarting file scan . . .')
    results_list = []

    for source_file in list_to_check:
        logging.debug("\nChecking {} . . .\n".format(source_file))
        with open(os.path.join(base_source_path, source_file), encoding="utf8") as this_file:
            data = this_file.read()
            build_result_struct(data, results_list, run_type)

    if run_type == 'users':
        results_list = sorted(results_list, key=lambda k: k['name'])

    logging.debug("######################################\n")
    logging.debug("      !! SCANNING COMPLETE !!         \n")
    logging.debug("######################################\n")
    logging.debug(pp.pprint(results_list))
    logging.debug("\n######################################\n")
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
        output_filename = 'users_result'
    elif run_type == 'posts':
        output_filename = 'posts_result'
    else:
        output_filename = 'results'
    return output_filename


def output_results(base_output_path, this_result, filename, output_type):
    output_filename = filename + '.' + output_type
    output_path = os.path.join(base_output_path, output_filename)
    logging.info('\nSaving results to {}'.format(output_path))
    with open(output_path, 'w+', encoding="utf8") as this_output:
        if output_type == 'txt':
            this_output.write(str(this_result))
        elif output_type == 'csv':
            try:
                keys = this_result[0].keys()
                dict_writer = csv.DictWriter(this_output, keys)
                dict_writer.writeheader()
                dict_writer.writerows(this_result)
            except IndexError:
                logging.info('No results found. Nothing to output to CSV.')


@click.command()
@click.option('-r', '--run_type', default="users", prompt="What data would you like? users, posts, or all",
              help="Determines data to parse. Valid values: users, posts, all.")
@click.option('-f', '--file_format', default="txt", prompt="Desired output format? txt or csv",
              help="Output file extension. Valid values: txt, csv")
def run(run_type, file_format):
    logging.basicConfig(format="%(asctime)s: %(message)s", level=logging.INFO, datefmt="%H:%M:%S")
    file_list = get_file_list(SOURCE_PATH)
    if run_type == 'all':
        output_results(OUTPUT_PATH, check_files(SOURCE_PATH, file_list, 'users'), get_output_filename('users'),
                       file_format)
        output_results(OUTPUT_PATH, check_files(SOURCE_PATH, file_list, 'posts'), get_output_filename('posts'),
                       file_format)
    else:
        output_results(OUTPUT_PATH, check_files(SOURCE_PATH, file_list, run_type), get_output_filename(run_type),
                       file_format)


if __name__ == '__main__':
    run()
