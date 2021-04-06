from datetime import datetime
import hashlib
import psycopg2
from pprint import pprint

from lib.subsidy import Subsidy

class KokesOdDbEufondy:
    def __init__(self, connstring):
        self.conn = psycopg2.connect(connstring, options='-c search_path=eufondy')

    def search_subsidies_of_company(self, company):


    def search_period_2007_2013(self, company):
        today_date = datetime.now().date()
        subsidies = []

        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT
                    "prijemce",
                    "projekt",
                    "operacni_program",
                    "fond_eu",
                    "datum_alokace",
                    "castka_proplacena",
                    "stav"
                FROM prehled_2017_2013
                WHERE "ico" = %(identifier)s
                """,
                {'identifier': company.identifier})

            prehled_2017_2013_records = list(cur.fetchall())

            for prehled_2017_2013_record in prehled_2017_2013_records:
                (
                    prijemce,
                    projekt,
                    operacni_program,
                    fond_eu,
                    datum_alokace,
                    castka_proplacena,
                    stav
                ) = zadatele_record

                subsidy = Subsidy()
                
                subsidy.id = 'EUFONDY-07-13-' + str(rok) + '-' + hashlib.md5(opatreni.encode()).hexdigest()[-6:]
                subsidy.beneficiary = company.name
                subsidy.country_code = 'CZ'
                
                subsidy.project_name = opatreni
                
                subsidy.year = rok
                subsidy.original_currency = 'CZK'
                
                subsidy.source = 'Seznam příjemců dotací za rok {rok} spravovaný Státním zemědělským intervenčním fondem (SZIF). Dostupné z: https://www.szif.cz/cs/seznam-prijemcu-dotaci [Cit. {today_date}]'.format(rok=rok, today_date=today_date)

                amount_in_czk = celkem_czk
                eu_cofinancing_amount_in_czk = zdroje_eu
            
                subsidy.amount_in_original_currency = amount_in_czk
                subsidy.eu_cofinancing_amount_in_original_currency = eu_cofinancing_amount_in_czk

                subsidy.amount_in_czk = amount_in_czk
                subsidy.eu_cofinancing_amount_in_czk = eu_cofinancing_amount_in_czk

                if fond_typ_podpory == 'EZZF PP':
                    subsidy.eu_cofinancing_from_fund = 'EAGF'
                elif fond_typ_podpory == 'EAFRD 14+':
                    subsidy.eu_cofinancing_from_fund = 'EAFRD'
                elif fond_typ_podpory == 'EAFRD':
                    subsidy.eu_cofinancing_from_fund = 'EAFRD'
                elif fond_typ_podpory == 'EZZF SOT':
                    subsidy.eu_cofinancing_from_fund = 'EAGF'

                # TODO: eur

                subsidies.append(subsidy)

        return subsidies
