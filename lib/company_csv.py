from lib.company import Company
from lib.csv import format_date, parse_date, parse_str

def get_fieldnames():
    return [
        'name',
        'identifier',
        'address',
        'country_code',
        'exists_since',
        'exists_until',
        'owners',
        'officials',
        'media_mentions'
    ]

def map_to_row(company):
    return {
        'name': company.name,
        'identifier': company.identifier,
        'address': company.address,
        'country_code': company.country_code,
        'exists_since': format_date(company.exists_since),
        'exists_until': format_date(company.exists_until),
        # TODO:
        'owners': None,
        'officials': None,
        'media_mentions': None
    }

def parse_row(row):
    company = Company()
    
    company.name = parse_str(row['name'])
    company.country_code = parse_str(row['country_code'])
    company.identifier = parse_str(row['identifier'])
    company.address = parse_str(row['address'])
    company.exists_since = parse_date(row['exists_since'])
    company.exists_until = parse_date(row['exists_until'])
    
    # TODO
    company.owners = None
    company.officials = None
    company.media_mentions = None

    return company
