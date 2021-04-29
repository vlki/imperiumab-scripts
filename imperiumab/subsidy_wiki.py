import json
from pprint import pprint
import urllib.parse

from imperiumab.subsidy import Subsidy
from imperiumab.wiki import parse_wiki_date, format_wiki_str


def get_subsidy_page_names(wiki):
    subsidy_category = wiki.site.categories['Dotace']

    list(map(lambda p: p.name, subsidy_category.members()))


def get_subsidies(wiki):
    subsidy_category = wiki.site.categories['Dotace']

    return map(lambda subsidy_page: map_subsidy_page_to_subsidy(wiki, subsidy_page), subsidy_category.members())


def get_subsidies_for_company(wiki, company_name):
    query = "[[Category:Dotace]][[Has beneficiary::{company_name}]]|limit=2000".format(company_name=company_name)

    subsidies = []

    for answer in wiki.site.ask(query):
        for property_name, property_data in answer.items():
            if property_name == 'fulltext':
                subsidies.append(map_subsidy_page_to_subsidy(wiki, wiki.site.pages[property_data]))

    return subsidies


def map_subsidy_page_to_subsidy(wiki, subsidy_page):
    subsidy = Subsidy()
    subsidy.id = subsidy_page.name

    print(subsidy.id)

    subsidy_structured_data = wiki.site.raw_api(action='smwbrowse', browse='subject', params=json.dumps(
        {'subject': subsidy_page.name, 'ns': 0, 'iw': '', 'subobject': ''}))
    # pprint(subsidy_structured_data)
    for structured_data_item in subsidy_structured_data['query']['data']:
        property_name = structured_data_item['property']
        property_data = structured_data_item['dataitem']

        if property_name == 'Has_beneficiary':
            beneficiary_encoded_page_name = property_data[0]['item']

            beneficiary_structured_data = wiki.site.raw_api(action='smwbrowse', browse='subject', params=json.dumps(
                {'subject': beneficiary_encoded_page_name, 'ns': 0, 'iw': '', 'subobject': ''}))
            for beneficiary_structured_data_item in beneficiary_structured_data['query']['data']:
                if beneficiary_structured_data_item['property'] == '_SKEY':
                    subsidy.beneficiary = beneficiary_structured_data_item['dataitem'][0]['item']

        if property_name == 'Has_beneficiary_original_name':
            subsidy.beneficiary_original_name = property_data[0]['item']

        if property_name == 'Has_country_code':
            subsidy.country_code = property_data[0]['item']

        if property_name == 'Has_project_code':
            subsidy.project_code = property_data[0]['item']

        if property_name == 'Has_project_name':
            subsidy.project_name = property_data[0]['item']

        if property_name == 'Has_programme_code':
            subsidy.programme_code = property_data[0]['item']

        if property_name == 'Has_programme_name':
            subsidy.programme_name = property_data[0]['item']

        if property_name == 'Was_signed_on':
            subsidy.signed_on = parse_wiki_date(property_data[0]['item'])

        if property_name == 'Was_in_year':
            subsidy.year = property_data[0]['item']

        if property_name == 'Has_source':
            subsidy.source = property_data[0]['item']

        if property_name == 'Has_EU_cofinancing_from_fund':
            subsidy.eu_cofinancing_from_fund = property_data[0]['item']

        if property_name == 'Has_EU_cofinancing_from_period':
            subsidy.eu_cofinancing_from_period = property_data[0]['item']

        if property_name == 'Has_original_currency':
            subsidy.original_currency = property_data[0]['item']

        if property_name == 'Has_amount_in_original_currency':
            subsidy.amount_in_original_currency = property_data[0]['item']

        if property_name == 'Has_EU_cofinancing_amount_in_original_currency':
            subsidy.eu_cofinancing_amount_in_original_currency = property_data[0]['item']

        if property_name == 'Has_currency_exchange_to_EUR':
            subsidy.currency_exchange_to_eur = property_data[0]['item']

        if property_name == 'Has_amount_in_EUR':
            subsidy.amount_in_eur = property_data[0]['item']

        if property_name == 'Has_EU_cofinancing_amount_in_EUR':
            subsidy.eu_cofinancing_amount_in_eur = property_data[0]['item']

        if property_name == 'Has_currency_exchange_to_CZK':
            subsidy.currency_exchange_to_czk = property_data[0]['item']

        if property_name == 'Has_amount_in_CZK':
            subsidy.amount_in_czk = property_data[0]['item']

        if property_name == 'Has_EU_cofinancing_amount_in_CZK':
            subsidy.eu_cofinancing_amount_in_czk = property_data[0]['item']

    # print(subsidy)
    # pprint(vars(subsidy))
    # exit(1)

    return subsidy


page_template = """
{{| class="wikitable"
|-
!Identifikátor
|{subsidy[id]}
|-
!Příjemce
|[[Has beneficiary::{subsidy[beneficiary]}]]
|-
!Příjemce (jak je uveden v datech)
|[[Has beneficiary original name::{subsidy[beneficiary_original_name]}]]
|-
!Země příjemce
|[[Has country code::{subsidy[country_code]}]]
|-
!Kód projektu
|[[Has project code::{subsidy[project_code]}]]
|-
!Název projektu
|[[Has project name::{subsidy[project_name]}]]
|-
!Kód programu
|[[Has programme code::{subsidy[programme_code]}]]
|-
!Název programu
|[[Has programme name::{subsidy[programme_name]}]]
|-
!Datum podpisu
|[[Was signed on::{subsidy[signed_on]}]]
|-
!Rok (podpisu, či začátku projektu)
|[[Was in year::{subsidy[year]}]]
|-
!Původní měna
|[[Has original currency::{subsidy[original_currency]}]]
|-
!Celková částka dotace v původní měně
|[[Has amount in original currency::{subsidy[amount_in_original_currency]}]]
|-
!Částka z rozpočtu EU v původní měně
|[[Has EU cofinancing amount in original currency::{subsidy[eu_cofinancing_amount_in_original_currency]}]]
|-
!Převod na EUR
|[[Has currency exchange to EUR::{subsidy[currency_exchange_to_eur]}]]
|-
!Celková částka dotace (EUR)
|[[Has amount in EUR::{subsidy[amount_in_eur]}]]
|-
!Částka z rozpočtu EU (EUR)
|[[Has EU cofinancing amount in EUR::{subsidy[eu_cofinancing_amount_in_eur]}]]
|-
!Převod na CZK
|[[Has currency exchange to CZK::{subsidy[currency_exchange_to_czk]}]]
|-
!Celková částka dotace (CZK)
|[[Has amount in CZK::{subsidy[amount_in_czk]}]]
|-
!Částka z rozpočtu EU (CZK)
|[[Has EU cofinancing amount in CZK::{subsidy[eu_cofinancing_amount_in_czk]}]]
|-
!EU fond
|[[Has EU cofinancing from fund::{subsidy[eu_cofinancing_from_fund]}]]
|-
!EU dotační období
|[[Has EU cofinancing from period::{subsidy[eu_cofinancing_from_period]}]]
|-
!Zdroj
|{{{{#set: Has source = {subsidy[source]} |template=BySetTemplateSimpleValueOutput }}}}
|}}

[[Category:Dotace]]
"""


def build_subsidy_page(subsidy):
    subsidy_obj = vars(subsidy)

    for subsidy_attr in subsidy_obj.keys():
        if subsidy_obj[subsidy_attr] is None:
            subsidy_obj[subsidy_attr] = ''

    return page_template.format(subsidy=subsidy_obj)


def exists_subsidy_page(wiki, subsidy):
    page = wiki.site.pages[subsidy.id]

    return page.exists


def create_subsidy_page(wiki, subsidy, change_text):
    page = wiki.site.pages[subsidy.id]

    if page.exists:
        raise Exception('Could not create as the page already exists')

    page.edit(build_subsidy_page(subsidy), change_text)
