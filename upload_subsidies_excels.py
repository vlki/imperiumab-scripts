#!/usr/bin/env python3

import argparse
import csv
from datetime import datetime
from dotenv import load_dotenv
import openpyxl
import os
from os.path import join, dirname
from pprint import pprint
import tempfile

from lib import subsidy_csv, subsidy_export_excel, subsidy_wiki, wiki

excel_file_configs = [
    {
        'file_name': 'Imperium AB subsidies export (all subsidies).xlsx',
        'filter_subsidies': lambda s: True
    },
    {
        'file_name': 'Imperium AB subsidies export (CZ only).xlsx',
        'filter_subsidies': lambda s: s.country_code == 'CZ'
    },
    {
        'file_name': 'Imperium AB subsidies export (SK only).xlsx',
        'filter_subsidies': lambda s: s.country_code == 'SK'
    },
    {
        'file_name': 'Imperium AB subsidies export (DE only).xlsx',
        'filter_subsidies': lambda s: s.country_code == 'DE'
    },
    {
        'file_name': 'Imperium AB subsidies export (HU only).xlsx',
        'filter_subsidies': lambda s: s.country_code == 'HU'
    },
    {
        'file_name': 'Imperium AB subsidies export (PL only).xlsx',
        'filter_subsidies': lambda s: s.country_code == 'PL'
    },
    {
        'file_name': 'Imperium AB subsidies export (Other countries only).xlsx',
        'filter_subsidies': lambda s: s.country_code not in ['CZ', 'SK', 'DE', 'HU', 'PL']
    }
]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Upload subsidies as Excel files to Imperium AB wiki')
    parser.add_argument('--subsidies-csv', required=True, help='Path to the CSV file with current subsidies exported from wiki')
    args = parser.parse_args()

    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)

    wiki_username = os.getenv('WIKI_USERNAME')
    wiki_password = os.getenv('WIKI_PASSWORD')

    if wiki_username is None or wiki_password is None:
        print('Missing .env file with WIKI_USERNAME and WIKI_PASSWORD variables to use for connecting to Imperium AB wiki. Please create .env file.')
        exit(1)

    # Get subsidies from CSV

    subsidies = []

    with open(args.subsidies_csv, mode='r') as subsidies_csv_file:
        reader = csv.DictReader(subsidies_csv_file)
        
        for row in reader:
            subsidies.append(subsidy_csv.parse_row(row))

    print('Loaded {subsidies_count} subsidies from passed CSV'.format(subsidies_count=len(subsidies)))

    # Login to wiki

    try:
        wiki_obj = wiki.Wiki(wiki_username, wiki_password)
    except Exception as e:
        print('Error when trying to login to wiki:')
        print(e)
        exit(1)

    # Create and upload Excel files

    for excel_file_config in excel_file_configs:
        wb = openpyxl.Workbook()
        ws = wb.active

        ws.append(subsidy_export_excel.get_header_row())

        for subsidy in filter(excel_file_config['filter_subsidies'], subsidies):
            ws.append(subsidy_export_excel.map_to_row(subsidy))

        with tempfile.NamedTemporaryFile() as tmp:
            wb.save(tmp.name)
            tmp.seek(0)
            wiki_obj.upload_file(tmp, excel_file_config['file_name'], 'Upload subsidies export Excel files')

        print('Uploaded {file_name} to Imperium AB wiki'.format(file_name=excel_file_config['file_name']))
    

