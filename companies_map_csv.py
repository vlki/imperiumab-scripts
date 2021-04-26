#!/usr/bin/env python3

import argparse
import csv
from dotenv import load_dotenv
import os
from os.path import join, dirname
from pprint import pprint
import urllib.parse

from imperiumab.kokes_od_db_ares import KokesOdDbAres
from imperiumab.wiki import Wiki
from imperiumab import company_csv, company_wiki, subsidy_csv, subsidy_wiki

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Export list of companies from Imperium AB wiki to CSV file data/companies_export.csv')
    parser.add_argument('--companies-csv', required=True,
                        help='Path to the CSV file with companies to find subsidies for, expects format of exported companies from wiki')
    parser.add_argument('--subsidies-csv', required=True,
                        help='Path to the CSV file with current subsidies exported from wiki')
    parser.add_argument('--kokes-od-connstring', required=True,
                        help='Connection string to the PostgreSQL database with ares data downloaded via kokes/od. Ex: postgresql://localhost/od')
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

    # Get subsidies from CSV

    subsidies = []

    with open(args.subsidies_csv, mode='r') as subsidies_csv_file:
        reader = csv.DictReader(subsidies_csv_file)

        for row in reader:
            subsidies.append(subsidy_csv.parse_row(row))

    print('Loaded {subsidies_count} subsidies from passed CSV'.format(subsidies_count=len(subsidies)))

    # Fill Czech addresses

    kokes_od_db_ares = KokesOdDbAres(args.kokes_od_connstring)

    for company in companies:
        if company.country_code == 'CZ':
            ares_info = kokes_od_db_ares.find_info_for_company_identifier(company.identifier)

            if ares_info and ares_info['address']:
                company.address = ares_info['address']

            if ares_info and ares_info['exists_since']:
                company.exists_since = ares_info['exists_since']

            if ares_info and ares_info['exists_until']:
                company.exists_until = ares_info['exists_until']

            # if ares_info and ares_info['address']:
            #     print(ares_info['address'] + ' | ' + company.name)
            #     company.address = ares_info['address']
            # else:
            #     print('--- | ' + company.name)

    # Get wiki urls

    print("Fetching company wiki urls...")

    try:
        wiki = Wiki(wiki_username, wiki_password)
    except Exception as e:
        print('Error when trying to login to wiki:')
        print(e)
        exit(1)

    company_page_urls = {}

    for company in companies:
        company_page_urls[company.name] = company_wiki.get_company_page_url(wiki, company.name)

    # Get subsidies

    print("Fetching company subsidies...")

    company_subsidies = {}

    for company in companies:
        company_subsidies[company.name] = []

        for subsidy in subsidies:
            if subsidy.beneficiary == company.name:
                company_subsidies[company.name].append(subsidy)

    # Wrote out to CSV

    print("Writing output csv...")

    csv_path = 'data/companies_map.csv'

    with open(csv_path, mode='w') as csv_file:
        fieldnames = [
            'Name',
            'Country',
            'Identifier',
            'Address',
            'Exists since',
            'Exists until',
            'Wiki URL',
            'Subsidies count'
        ]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()

        for company in companies:
            mapped_row = company_csv.map_to_row(company)
            row = {
                'Name': mapped_row['name'],
                'Country': mapped_row['country_code'],
                'Identifier': mapped_row['identifier'],
                'Address': mapped_row['address'],
                'Exists since': mapped_row['exists_since'],
                'Exists until': mapped_row['exists_until'],
                'Wiki URL': company_page_urls[company.name],
                'Subsidies count': len(company_subsidies[company.name])
            }
            writer.writerow(row)

    print('Wrote {companies_count} companies to {csv_path}'.format(companies_count=len(companies), csv_path=csv_path))
