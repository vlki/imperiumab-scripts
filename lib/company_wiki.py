from pprint import pprint

from lib.company import Company
from lib.wiki import parse_wiki_date

# TODO: not pretty to have it hardcoded like this, is there a better solution?
not_companies_pages = ['AB private trust I', 'AB private trust II']

def get_company_page_names(wiki):
    company_category = wiki.site.categories['Firmy a jiné právnické osoby']

    company_pages = filter(lambda company_page: company_page.name not in not_companies_pages, company_category.members())

    list(map(lambda p: p.name, company_pages))
    
def get_companies(wiki):
    company_category = wiki.site.categories['Firmy a jiné právnické osoby']
    
    company_pages = filter(lambda company_page: company_page.name not in not_companies_pages, company_category.members())

    return map(lambda company_page: map_company_page_to_company(wiki, company_page), company_pages)

def map_company_page_to_company(wiki, company_page):
    company = Company()
    company.name = company_page.name

    company_structured_data = wiki.site.raw_api(action='browsebysubject', subject=company.name)
    for structured_data_item in company_structured_data['query']['data']:
        property_name = structured_data_item['property']
        property_data = structured_data_item['dataitem']

        if property_name == 'HasIdentifier':
            company.identifier = property_data[0]['item']

        if property_name == 'HasCountryCode':
            company.country_code = property_data[0]['item']

        if property_name == 'HasAddress':
            company.address = property_data[0]['item']

        if property_name == 'Exists_since':
            company.exists_since = parse_wiki_date(property_data[0]['item'])

        if property_name == 'Exists_until':
            company.exists_until = parse_wiki_date(property_data[0]['item'])

        # TODO: parse rest of information

    # print(company)
    # print(company.exists_since)
    # print(company.exists_until)

    return company
        