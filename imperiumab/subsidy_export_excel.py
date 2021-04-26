from imperiumab.subsidy import Subsidy
from imperiumab.csv import format_date, parse_date, parse_str, parse_int, parse_float


def get_header_row():
    return [
        'Identifikátor / Identifier',
        'Příjemce / Beneficiary',
        'Příjemce (jak je uveden v datech) / Beneficiary original name',
        'Země příjemce / Country code',

        'Kód projektu / Project code',
        'Název projektu / Project name',
        'Kód programu / Programme code',
        'Název programu / Programme name',

        'Datum podpisu / Signed on date',
        'Rok (podpisu, či začátku projektu) / Year (of signing or project start)',

        'Původní měna / Original currency',
        'Celková částka dotace v původní měně / Amount in original currency',
        'Částka z rozpočtu EU v původní měně / EU cofinancing amount in original currency',

        'Převod na EUR / Currency exchange to EUR',
        'Celková částka dotace (EUR) / Amount in EUR',
        'Částka z rozpočtu EU (EUR) / EU cofinancing amount in EUR',

        'Převod na CZK / Currency exchange to CZK',
        'Celková částka dotace (CZK) / Amount in CZK',
        'Částka z rozpočtu EU (CZK) / EU cofinancing amount in CZK',

        'EU fond / EU fund',
        'EU dotační období / EU subsidies period',

        'Zdroj / Source'
    ]


def map_to_row(subsidy):
    return [
        subsidy.id,
        subsidy.beneficiary,
        subsidy.beneficiary_original_name,
        subsidy.country_code,

        subsidy.project_code,
        subsidy.project_name,
        subsidy.programme_code,
        subsidy.programme_name,

        subsidy.signed_on,
        subsidy.year,

        subsidy.original_currency,
        subsidy.amount_in_original_currency,
        subsidy.eu_cofinancing_amount_in_original_currency,

        subsidy.currency_exchange_to_eur,
        subsidy.amount_in_eur,
        subsidy.eu_cofinancing_amount_in_eur,

        subsidy.currency_exchange_to_czk,
        subsidy.amount_in_czk,
        subsidy.eu_cofinancing_amount_in_czk,

        subsidy.eu_cofinancing_from_fund,
        subsidy.eu_cofinancing_from_period,

        subsidy.source,
    ]
