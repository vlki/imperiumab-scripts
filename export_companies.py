#!/usr/bin/env python3

import argparse
import csv
from dotenv import load_dotenv
import os
from os.path import join, dirname

from imperiumab.wiki import Wiki
from imperiumab import company_csv, company_wiki

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Export list of companies from Imperium AB wiki to CSV file data/companies_export.csv')
    args = parser.parse_args()

    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)

    wiki_username = os.getenv('WIKI_USERNAME')
    wiki_password = os.getenv('WIKI_PASSWORD')

    if wiki_username is None or wiki_password is None:
        print('Missing .env file with WIKI_USERNAME and WIKI_PASSWORD variables to use for connecting to Imperium AB wiki. Please create .env file.')
        exit(1)

    # Fetch companies from wiki

    try:
        wiki = Wiki(wiki_username, wiki_password)
    except Exception as e:
        print('Error when trying to login to wiki:')
        print(e)
        exit(1)

    companies = list(company_wiki.get_companies(wiki))

    # Wrote out to CSV

    csv_path = 'data/companies_export.csv'

    with open(csv_path, mode='w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=company_csv.get_fieldnames())

        writer.writeheader()

        for company in companies:
            writer.writerow(company_csv.map_to_row(company))

    print('Wrote {companies_count} companies to {csv_path}'.format(companies_count=len(companies), csv_path=csv_path))
