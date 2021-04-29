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
    parser = argparse.ArgumentParser(description='Import subsidies from CSV file to Imperium AB wiki')
    parser.add_argument('--companies-csv', required=True,
                        help='Path to the CSV file with current companies exported from wiki')
    parser.add_argument('--subsidies-csv', required=True,
                        help='Path to the CSV file with current subsidies exported from wiki')
    parser.add_argument('--import-csv', required=True, help='Path to the CSV file with subsidies to import')
    args = parser.parse_args()

    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)

    wiki_username = os.getenv('WIKI_USERNAME')
    wiki_password = os.getenv('WIKI_PASSWORD')

    if wiki_username is None or wiki_password is None:
        print('Missing .env file with WIKI_USERNAME and WIKI_PASSWORD variables to use for connecting to Imperium AB wiki. Please create .env file.')
        exit(1)

    # Get companies from CSV

    companies = []

    with open(args.companies_csv, mode='r') as companies_csv_file:
        reader = csv.DictReader(companies_csv_file)

        for row in reader:
            companies.append(company_csv.parse_row(row))

    print('Loaded {companies_count} companies from passed CSV'.format(companies_count=len(companies)))

    # Get existing subsidies from CSV

    existing_subsidies = []

    with open(args.subsidies_csv, mode='r') as subsidies_csv_file:
        reader = csv.DictReader(subsidies_csv_file)

        for row in reader:
            existing_subsidies.append(subsidy_csv.parse_row(row))

    print('Loaded {subsidies_count} subsidies from passed CSV'.format(subsidies_count=len(existing_subsidies)))

    # Get import subsidies from CSV

    import_subsidies = []

    with open(args.import_csv, mode='r') as import_csv_file:
        reader = csv.DictReader(import_csv_file)

        for row in reader:
            import_subsidies.append(subsidy_csv.parse_row(row))

    print('Loaded {import_subsidies_count} subsidies to be imported from passed CSV'.format(
        import_subsidies_count=len(import_subsidies)))

    # Identify and remove duplicates

    companies_by_name = {}
    for company in companies:
        companies_by_name[company.name] = company

    existing_subsidies_by_beneficiary = {}
    for existing_subsidy in existing_subsidies:
        if existing_subsidy.beneficiary not in existing_subsidies_by_beneficiary:
            existing_subsidies_by_beneficiary[existing_subsidy.beneficiary] = []

        existing_subsidies_by_beneficiary[existing_subsidy.beneficiary].append(existing_subsidy)

    import_subsidies_by_beneficiary = {}
    for import_subsidy in import_subsidies:
        if import_subsidy.beneficiary not in import_subsidies_by_beneficiary:
            import_subsidies_by_beneficiary[import_subsidy.beneficiary] = []

        import_subsidies_by_beneficiary[import_subsidy.beneficiary].append(import_subsidy)

    filtered_company_import_subsidies = {}

    for beneficiary in import_subsidies_by_beneficiary.keys():
        company_import_subsidies = sorted(import_subsidies_by_beneficiary[beneficiary], key=lambda s: str(s.year))

        company = companies_by_name[beneficiary]

        if company is None:
            print('Skipping import of {company_import_subsidies_count} subsidies, because company with name {beneficiary} does not exist in wiki'.format(
                company_import_subsidies_count=len(company_import_subsidies), beneficiary=beneficiary))
            continue

        company_existing_subsidies = []
        if company.name in existing_subsidies_by_beneficiary:
            company_existing_subsidies = sorted(existing_subsidies_by_beneficiary[company.name], key=lambda s: str(s.year))

        filtered_company_import_subsidies[company.name] = []
        for import_subsidy in company_import_subsidies:
            will_import = True

            for existing_subsidy in company_existing_subsidies:
                if import_subsidy.year == existing_subsidy.year and import_subsidy.amount_in_czk == existing_subsidy.amount_in_czk:
                    print('- Wont be importing {import_subsidy}, because it seems to be already on wiki as {existing_subsidy}'.format(
                        import_subsidy=import_subsidy, existing_subsidy=existing_subsidy))
                    will_import = False

            if will_import:
                filtered_company_import_subsidies[company.name].append(import_subsidy)

        # print('==============================================')
        # print('==============================================')
        # print('==============================================')
        print('{company.name}: will be importing {import_subsidies_count} subsidies'.format(
            company=company, import_subsidies_count=len(filtered_company_import_subsidies)))
        # print('==============================================')
        # for subsidy in company_existing_subsidies:
        #     print(subsidy)
        # print('==============================================')
        # for subsidy in filtered_company_import_subsidies:
        #     print(subsidy)

    # Ask for confirmation

    print('')
    answer = confirm("Are you sure you want to import all these to wiki?")
    if answer != True:
        print('Ok, not importing anything')
        exit(0)

    # Do the import

    try:
        wiki = Wiki(wiki_username, wiki_password)
    except Exception as e:
        print('Error when trying to login to wiki:')
        print(e)
        exit(1)

    for beneficiary in filtered_company_import_subsidies.keys():
        import_subsidies = filtered_company_import_subsidies[beneficiary]

        print('Importing {import_subsidies_count} subsidies for {beneficiary}...'.format(
            import_subsidies_count=len(import_subsidies), beneficiary=beneficiary))

        for import_subsidy in import_subsidies:
            if subsidy_wiki.exists_subsidy_page(wiki, import_subsidy):
                print('Skipping {subsidy}, page already exists'.format(subsidy=import_subsidy))
                continue

            print('Importing {subsidy}'.format(subsidy=import_subsidy))

            subsidy_wiki.create_subsidy_page(wiki, import_subsidy, 'Import')
            # exit(1)

            # print(subsidy_wiki.build_subsidy_page(import_subsidy))
            # exit(1)
