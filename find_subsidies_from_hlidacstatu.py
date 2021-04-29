#!/usr/bin/env python3

import argparse
import csv
from dotenv import load_dotenv
import os
from os.path import join, dirname
from pprint import pprint

from imperiumab import company_csv, hlidac_statu_subsidies, subsidy_csv

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Find subsidies of Czech companies from Hlidacstatu.cz, writes the result to data/subsidies_from_hlidacstatu.csv.')
    parser.add_argument('--companies-csv', required=True,
                        help='Path to the CSV file with companies to find subsidies for, expects format of exported companies from wiki')
    args = parser.parse_args()

    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)

    hlidac_statu_auth_token = os.getenv('HLIDAC_STATU_AUTH_TOKEN')

    if hlidac_statu_auth_token is None:
        print('Missing .env file with HLIDAC_STATU_AUTH_TOKEN variables to use for connecting to Imperium AB wiki. Please create .env file.')
        exit(1)

    # Get companies from CSV

    companies = []

    with open(args.companies_csv, mode='r') as companies_csv_file:
        reader = csv.DictReader(companies_csv_file)

        for row in reader:
            companies.append(company_csv.parse_row(row))

    print('Loaded {companies_count} companies from passed CSV'.format(companies_count=len(companies)))

    # Find subsidies via Hlidac statu API

    companies_cz = list(filter(lambda c: c.country_code == 'CZ', companies))
    all_subsidies = []

    for company in companies_cz:
        company_subsidies = hlidac_statu_subsidies.find_subsidies_of_company(hlidac_statu_auth_token, company)

        print("{company.name}: found {subsidies_count} subsidies".format(
            company=company, subsidies_count=len(company_subsidies)))

        all_subsidies += company_subsidies

    # Write to out CSV

    csv_path = 'data/subsidies_from_hlidacstatu.csv'

    with open(csv_path, mode='w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=subsidy_csv.get_fieldnames())

        writer.writeheader()

        for subsidy in all_subsidies:
            writer.writerow(subsidy_csv.map_to_row(subsidy))

    print('Wrote {subsidies_count} subsidies to {csv_path}'.format(
        subsidies_count=len(all_subsidies), csv_path=csv_path))
