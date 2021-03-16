import mwclient
from pprint import pprint

from lib.company import Company

class Wiki:
    def __init__(self, username, password):
        self.site = mwclient.Site('imperiumab.investigace.cz', path='/')
        self.site.login(username, password)

    def get_company_page_names(self):
        company_category = self.site.categories['Firmy a jiné právnické osoby']

        list(map(lambda p: p.name, company_category.members()))
        
    def get_companies(self):
        company_category = self.site.categories['Firmy a jiné právnické osoby']

        return map(self.map_company_page_to_company, company_category.members())

    def map_company_page_to_company(self, company_page):
        company = Company()
        company.name = company_page.name

        company_structured_data = self.site.raw_api(action='browsebysubject', subject=company.name)
        for structured_data_item in company_structured_data['query']['data']:
            property_name = structured_data_item['property']
            property_data = structured_data_item['dataitem']

            if property_name == 'HasIdentifier':
                company.identifier = property_data[0]['item']

            if property_name == 'HasCountryCode':
                company.country_code = property_data[0]['item']

            # TODO: parse rest of information

        return company
        