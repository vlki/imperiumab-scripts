from datetime import datetime
import decimal
from pprint import pprint
import re
import requests
from slugify import slugify

from imperiumab.subsidy import Subsidy
from imperiumab import exchange_rates


def find_subsidies_of_company(auth_token, company):
    all_hs_subsidies = []
    page = 1

    while True:
        headers = {
            'Authorization': 'Token ' + auth_token,
            'Content-Type': 'application/json'
        }
        params = {
            'dotaz': 'ico:' + company.identifier,
            'strana': page,
            'razeni': 2  # sort by date of signing, oldest first
        }

        r = requests.get('https://www.hlidacstatu.cz/api/v2/dotace/hledat', headers=headers, params=params)

        # pprint(r.request.url)
        # pprint(r.request.headers)
        # print(r.text)

        payload = r.json()

        # pprint(payload)

        if payload['Total'] == 0:
            break

        if len(payload['Results']) == 0:
            break

        all_hs_subsidies += payload['Results']
        page += 1

    subsidies_pairs = []
    remove_hs_ids = []

    for hs_subsidy in all_hs_subsidies:
        # print(hs_subsidy)
        # print(map_hlidac_statu_subsidy_to_subsidy(company, hs_subsidy))
        subsidies_pairs.append({
            'hs_subsidy': hs_subsidy,
            'subsidy': map_hlidac_statu_subsidy_to_subsidy(company, hs_subsidy)
        })

        if 'Duplicita' in hs_subsidy:
            # Hlidac statu returns the duplicate ID without being slugified
            duplicate_id = slugify(hs_subsidy['Duplicita'])

            if hs_subsidy['IdDotace'].startswith('eufondy-') and duplicate_id.startswith('cedr-'):
                remove_hs_ids.append(duplicate_id)
            elif hs_subsidy['IdDotace'].startswith('cedr-') and duplicate_id.startswith('cedr-'):
                remove_hs_ids.append(duplicate_id)
            elif hs_subsidy['IdDotace'].startswith('deminimis-') and duplicate_id.startswith('eufondy-'):
                remove_hs_ids.append(hs_subsidy['IdDotace'])
            elif hs_subsidy['IdDotace'].startswith('dotinfo-') and duplicate_id.startswith('cedr-'):
                remove_hs_ids.append(hs_subsidy['IdDotace'])
            elif hs_subsidy['IdDotace'].startswith('dotinfo-') and duplicate_id.startswith('eufondy-'):
                remove_hs_ids.append(hs_subsidy['IdDotace'])
            elif hs_subsidy['IdDotace'].startswith('deminimis-') and duplicate_id.startswith('deminimis-'):
                remove_hs_ids.append(duplicate_id)
            elif hs_subsidy['IdDotace'].startswith('deminimis-') and duplicate_id.startswith('cedr-'):
                remove_hs_ids.append(hs_subsidy['IdDotace'])
            else:
                print(hs_subsidy['IdDotace'])
                print(duplicate_id)
                raise Exception('Subsidy has duplicate, but there is no rule to remove it')

    # pprint(remove_hs_ids)

    subsidies_result = []

    for subsidies_pair in subsidies_pairs:
        hs_subsidy = subsidies_pair['hs_subsidy']
        subsidy = subsidies_pair['subsidy']

        if hs_subsidy['IdDotace'] in remove_hs_ids:
            continue

        subsidies_result.append(subsidy)

    return subsidies_result


def map_hlidac_statu_subsidy_to_subsidy(company, hs_subsidy, today_date=None):
    if today_date is None:
        today_date = datetime.now().date()

    subsidy = Subsidy()
    subsidy.country_code = 'CZ'

    subsidy.id = hs_subsidy['IdDotace']

    if subsidy.id.startswith('cedr-'):
        subsidy.id = subsidy.id.replace('cedr-', 'CEDR-', 1)
    elif subsidy.id.startswith('szif-'):
        subsidy.id = subsidy.id.replace('szif-', 'SZIF-', 1)
    elif subsidy.id.startswith('dotinfo-'):
        subsidy.id = subsidy.id.replace('dotinfo-', 'DOTINFO-', 1)
    elif subsidy.id.startswith('eufondy-'):
        subsidy.id = subsidy.id.replace('eufondy-', 'EUFONDY-', 1)
    elif subsidy.id.startswith('czechinvest-'):
        subsidy.id = subsidy.id.replace('czechinvest-', 'CZECHINVEST-', 1)
    elif subsidy.id.startswith('deminimis-'):
        subsidy.id = subsidy.id.replace('deminimis-', 'DEMINIMIS-', 1)
    else:
        raise Exception('Unknown id prefix ' + subsidy.id)

    subsidy.beneficiary = company.name

    if 'Prijemce' in hs_subsidy and 'ObchodniJmeno' in hs_subsidy['Prijemce']:
        subsidy.beneficiary_original_name = hs_subsidy['Prijemce']['ObchodniJmeno']

    if 'KodProjektu' in hs_subsidy:
        subsidy.project_code = hs_subsidy['KodProjektu']

    if 'NazevProjektu' in hs_subsidy:
        subsidy.project_name = hs_subsidy['NazevProjektu']

    if 'Program' in hs_subsidy and 'Nazev' in hs_subsidy['Program']:
        subsidy.programme_name = hs_subsidy['Program']['Nazev']

    if 'Program' in hs_subsidy and 'Kod' in hs_subsidy['Program']:
        subsidy.programme_code = hs_subsidy['Program']['Kod']

    if 'DatumPodpisu' in hs_subsidy:
        datetime_obj = None

        try:
            datetime_obj = datetime.strptime(hs_subsidy['DatumPodpisu'], '%Y-%m-%dT00:00:00')
        except ValueError:
            pass

        try:
            datetime_obj = datetime.strptime(hs_subsidy['DatumPodpisu'], '%Y-%m-%dT00:00:00Z')
        except ValueError:
            pass

        if datetime_obj:
            subsidy.signed_on = datetime_obj.date()

    if subsidy.signed_on:
        subsidy.year = subsidy.signed_on.year

    # dotinfo subsidies
    if subsidy.year is None and subsidy.project_name.startswith('CZ.1.02/'):
        subsidy.year = '2007-2013'

    subsidy.original_currency = 'CZK'

    if 'DotaceCelkem' in hs_subsidy:
        subsidy.amount_in_original_currency = round(decimal.Decimal(hs_subsidy['DotaceCelkem']), 2)
        subsidy.amount_in_czk = round(decimal.Decimal(hs_subsidy['DotaceCelkem']), 2)

    # SZIF and EUFONDY subsidies
    if len(hs_subsidy['Rozhodnuti']) == 2:
        cz_rozhodnuti = list(filter(lambda r: r['Poskytovatel'] == 'CZ', hs_subsidy['Rozhodnuti']))
        eu_rozhodnuti = list(filter(lambda r: r['Poskytovatel'] == 'EU', hs_subsidy['Rozhodnuti']))

        if len(cz_rozhodnuti) == 1 and len(eu_rozhodnuti) == 1:
            if 'CerpanoCelkem' in eu_rozhodnuti[0]:
                subsidy.eu_cofinancing_amount_in_czk = round(decimal.Decimal(eu_rozhodnuti[0]['CerpanoCelkem']), 2)

            if subsidy.year is None and 'Rok' in eu_rozhodnuti[0]:
                subsidy.year = eu_rozhodnuti[0]['Rok']

    exchange_rates.fill_subsidy_eur_info(subsidy)

    subsidy.source = 'Záznam dotace {hs_id} v databázi Hlídač státu. Dostupné z: https://www.hlidacstatu.cz/Dotace/Detail/{hs_id} [Cit. {today_date}]'.format(
        hs_id=hs_subsidy['IdDotace'], today_date=today_date)

    return subsidy
