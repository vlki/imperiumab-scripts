from imperiumab.subsidy import Subsidy
from imperiumab.csv import format_date, parse_date, parse_str, parse_int, parse_float


def get_fieldnames():
    return [
        'id',
        'beneficiary',
        'beneficiary_original_name',
        'country_code',
        'project_code',
        'project_name',
        'programme_code',
        'programme_name',
        'signed_on',
        'year',

        'original_currency',
        'amount_in_original_currency',
        'eu_cofinancing_amount_in_original_currency',

        'currency_exchange_to_eur',
        'amount_in_eur',
        'eu_cofinancing_amount_in_eur',

        'currency_exchange_to_czk',
        'amount_in_czk',
        'eu_cofinancing_amount_in_czk',

        'eu_cofinancing_from_fund',
        'eu_cofinancing_from_period',

        'source'
    ]


def map_to_row(subsidy):
    return {
        'id': subsidy.id,
        'beneficiary': subsidy.beneficiary,
        'beneficiary_original_name': subsidy.beneficiary_original_name,
        'country_code': subsidy.country_code,
        'project_code': subsidy.project_code,
        'project_name': subsidy.project_name,
        'programme_code': subsidy.programme_code,
        'programme_name': subsidy.programme_name,
        'signed_on': format_date(subsidy.signed_on),
        'year': subsidy.year,

        'original_currency': subsidy.original_currency,
        'amount_in_original_currency': subsidy.amount_in_original_currency,
        'eu_cofinancing_amount_in_original_currency': subsidy.eu_cofinancing_amount_in_original_currency,

        'currency_exchange_to_eur': subsidy.currency_exchange_to_eur,
        'amount_in_eur': subsidy.amount_in_eur,
        'eu_cofinancing_amount_in_eur': subsidy.eu_cofinancing_amount_in_eur,

        'currency_exchange_to_czk': subsidy.currency_exchange_to_czk,
        'amount_in_czk': subsidy.amount_in_czk,
        'eu_cofinancing_amount_in_czk': subsidy.eu_cofinancing_amount_in_czk,

        'eu_cofinancing_from_fund': subsidy.eu_cofinancing_from_fund,
        'eu_cofinancing_from_period': subsidy.eu_cofinancing_from_period,

        'source': subsidy.source,
    }


def parse_row(row):
    subsidy = Subsidy()

    subsidy.id = parse_str(row['id'])
    subsidy.beneficiary = parse_str(row['beneficiary'])
    subsidy.beneficiary_original_name = parse_str(row['beneficiary_original_name'])
    subsidy.country_code = parse_str(row['country_code'])
    subsidy.project_code = parse_str(row['project_code'])
    subsidy.project_name = parse_str(row['project_name'])
    subsidy.programme_code = parse_str(row['programme_code'])
    subsidy.programme_name = parse_str(row['programme_name'])
    subsidy.signed_on = parse_date(row['signed_on'])
    subsidy.year = parse_str(row['year'])

    subsidy.original_currency = parse_str(row['original_currency'])
    subsidy.amount_in_original_currency = parse_float(row['amount_in_original_currency'])
    subsidy.eu_cofinancing_amount_in_original_currency = parse_float(row['eu_cofinancing_amount_in_original_currency'])

    subsidy.currency_exchange_to_eur = parse_str(row['currency_exchange_to_eur'])
    subsidy.amount_in_eur = parse_float(row['amount_in_eur'])
    subsidy.eu_cofinancing_amount_in_eur = parse_float(row['eu_cofinancing_amount_in_eur'])

    subsidy.currency_exchange_to_czk = parse_str(row['currency_exchange_to_czk'])
    subsidy.amount_in_czk = parse_float(row['amount_in_czk'])
    subsidy.eu_cofinancing_amount_in_czk = parse_float(row['eu_cofinancing_amount_in_czk'])

    subsidy.eu_cofinancing_from_fund = parse_str(row['eu_cofinancing_from_fund'])
    subsidy.eu_cofinancing_from_period = parse_str(row['eu_cofinancing_from_period'])

    subsidy.source = parse_str(row['source'])

    return subsidy
