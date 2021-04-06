#!/usr/bin/env python3

import argparse
import csv
from pprint import pprint

from lib.kokes_od_db_eufondy import KokesOdDbEufondy
from lib import company_csv, subsidy_csv

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Find subsidies of Czech companies from eufondy database, writes the result to data/subsidies_from_eufondy.csv.')
    parser.add_argument('--companies-csv', required=True, help='Path to the CSV file with companies to find subsidies for, expects format of exported companies from wiki')
    parser.add_argument('--kokes-od-connstring', required=True, help='Connection string to the PostgreSQL database with eufondy data downloaded via kokes/od. Ex: postgresql://localhost/od')
    args = parser.parse_args()    

    # Get companies from CSV

    companies = []

    with open(args.companies_csv, mode='r') as companies_csv_file:
        reader = csv.DictReader(companies_csv_file)
        
        for row in reader:
            companies.append(company_csv.parse_row(row))

    print('Loaded {companies_count} companies from passed CSV'.format(companies_count=len(companies)))

    # Find subsidies from eufondy db

    kokes_od_db_eufondy = KokesOdDbEufondy(args.kokes_od_connstring)
    subsidies = []

    for company in companies:
        if company.country_code != 'CZ':
            continue

        company_subsidies = kokes_od_db_eufondy.search_subsidies_of_company(company)

        print("{company.name}: found {subsidies_count} subsidies".format(company=company, subsidies_count=len(company_subsidies)))

        subsidies.extend(company_subsidies)

    # Write to out CSV
    
    # csv_path = 'data/subsidies_from_szif.csv'

    # with open(csv_path, mode='w') as csv_file:
    #     writer = csv.DictWriter(csv_file, fieldnames=subsidy_csv.get_fieldnames())

    #     writer.writeheader()
        
    #     for subsidy in subsidies:
    #         writer.writerow(subsidy_csv.map_to_row(subsidy))

    # print('Wrote {subsidies_count} subsidies to {csv_path}'.format(subsidies_count=len(subsidies), csv_path=csv_path))
