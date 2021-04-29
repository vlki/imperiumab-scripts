#!/usr/bin/env python3

import argparse
import csv
from dotenv import load_dotenv
import os
from os.path import join, dirname
from pprint import pprint
from prompt_toolkit.shortcuts import confirm

from imperiumab.wiki import Wiki
from imperiumab import company_csv, subsidy_csv, subsidy_wiki

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Remove subsidies in CSV file from Imperium AB wiki')
    parser.add_argument('--remove-subsidies-csv', required=True,
                        help='Path to the CSV file with subsidies exported from wiki you want to remove')
    args = parser.parse_args()

    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)

    wiki_username = os.getenv('WIKI_USERNAME')
    wiki_password = os.getenv('WIKI_PASSWORD')

    if wiki_username is None or wiki_password is None:
        print('Missing .env file with WIKI_USERNAME and WIKI_PASSWORD variables to use for connecting to Imperium AB wiki. Please create .env file.')
        exit(1)

    # Get existing subsidies from CSV

    existing_subsidies = []

    with open(args.remove_subsidies_csv, mode='r') as subsidies_csv_file:
        reader = csv.DictReader(subsidies_csv_file)

        for row in reader:
            subsidy = subsidy_csv.parse_row(row)

            if subsidy.country_code == 'CZ':
                existing_subsidies.append(subsidy)

    print('Loaded {subsidies_count} subsidies from passed CSV'.format(subsidies_count=len(existing_subsidies)))

    # Check

    print('')
    answer = confirm("Are you sure you want to remove all these from wiki?")
    if answer != True:
        print('Ok, not removing anything')
        exit(0)

    # Do the removal

    try:
        wiki = Wiki(wiki_username, wiki_password)
    except Exception as e:
        print('Error when trying to login to wiki:')
        print(e)
        exit(1)

    for subsidy in existing_subsidies:
        subsidy_page = wiki.site.pages[subsidy.id]

        if not subsidy_page.exists:
            print('Page for subsidy ID {subsidy.id} not found'.format(subsidy=subsidy))
            continue

        subsidy_page.delete()
        print('Deleted page for subsidy ID {subsidy.id}'.format(subsidy=subsidy))
