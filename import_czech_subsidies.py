import argparse
from dotenv import load_dotenv
import os
from os.path import join, dirname

from lib.kokes_od_db_cedr import KokesOdDbCedr
from lib.wiki import Wiki

# 1. Fetch all companies from Imperium AB wiki
# 2. Find subsidies for them in CEDR
# 3. Find subsidies for them in SZIF
# 4. Find subsidies for them in EU funds
# 5. Deduplicate the list of subsidies
# 6. Import subsidies to wiki

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Import subsidies of Czech companies from CEDR, SZIF and EU funds to Imperium AB wiki via kokes/od project.')
    parser.add_argument('--kokes-od-connstring', required=True, help='Connection string to the PostgreSQL database with cedr, eufondy and szif data downloaded via kokes/od. Ex: postgresql://localhost/od')
    args = parser.parse_args()

    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)

    wiki_username = os.getenv('WIKI_USERNAME')
    wiki_password = os.getenv('WIKI_PASSWORD')

    if wiki_username is None or wiki_password is None:
        print('Missing .env file with WIKI_USERNAME and WIKI_PASSWORD variables to use for connecting to Imperium AB wiki. Please create .env file.')
        exit(1)

    try:
        wiki = Wiki(wiki_username, wiki_password)
    except Exception as e:
        print('Error when trying to login to wiki:')
        print(e)
        exit(1)

    kokes_od_db_cedr = KokesOdDbCedr(args.kokes_od_connstring)

    for company in wiki.get_companies():
        if company.country_code != 'CZ' or company.identifier is None:
            continue

        # TODO: Remove
        if company.identifier != '63479401':
            continue

        # print('========================================================================')
        # print(company)
        # print('---')

        subsidies = kokes_od_db_cedr.search_subsidies_of_company(company)

        subsidies_amount_sum = 0
        for subsidy in subsidies:
            print(subsidy)
            subsidies_amount_sum += subsidy.amount_in_czk

        print(subsidies_amount_sum)

        exit(1)
        

    print(args.od_connstring)

    


