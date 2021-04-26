from datetime import datetime
import decimal
import psycopg2
from pprint import pprint

from imperiumab.subsidy import Subsidy
from imperiumab.exchange_rates import get_eur_to_czk_rate, get_eur_to_czk_rate_text

eu_finance_sources_names = [
    'Evropský sociální fond',
    'Evropský fond pro regionální rozvoj',
    'Evropský zemědělský fond pro rozvoj venkova',
    'Evropský rybářský fond',
    'Evropský zemědělský orientační a záruční fond'
]

eu_finance_source_name_to_fund = {
    'Evropský sociální fond': 'ESF',
    'Evropský fond pro regionální rozvoj': 'ERDF',
    'Evropský zemědělský fond pro rozvoj venkova': 'EAFRD',
    'Evropský rybářský fond': 'EMFF',
    'Evropský zemědělský orientační a záruční fond': 'EAGF'
}


class KokesOdDbCedr:
    def __init__(self, connstring):
        self.conn = psycopg2.connect(connstring, options='-c search_path=cedr')

    def search_subsidies_of_company(self, company):
        today_date = datetime.now().date()
        subsidies = []

        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT
                    "idDotace",
                    "iriOperacniProgram",
                    "iriProgram",
                    "projektIdentifikator",
                    "projektNazev",
                    "podpisDatum"
                FROM dotace
                WHERE "idPrijemce" = %(identifier)s
                """,
                        {'identifier': company.identifier})

            dotace_records = list(cur.fetchall())

            for dotace_record in dotace_records:
                (
                    idDotace,
                    iriOperacniProgram,
                    iriProgram,
                    projektIdentifikator,
                    projektNazev,
                    podpisDatum
                ) = dotace_record

                subsidy = Subsidy()

                subsidy.id = 'CEDR-' + projektIdentifikator.strip()
                subsidy.beneficiary = company.name
                subsidy.country_code = 'CZ'

                subsidy.project_code = projektIdentifikator.strip()
                subsidy.project_name = projektNazev

                if iriProgram != None:
                    subsidy.programme_name = iriProgram
                if subsidy.programme_name == None and iriOperacniProgram != None:
                    subsidy.programme_name = iriOperacniProgram

                subsidy.signed_on = podpisDatum.date()
                subsidy.year = podpisDatum.year
                subsidy.original_currency = 'CZK'

                subsidy.source = 'Záznam dotace {idDotace} v Centrální evidenci dotací z rozpočtu (CEDR) spravované Generálním finančním ředitelstvím. Dostupné z: http://cedropendata.mfcr.cz/c3lod/cedr/resource/Dotace/{idDotace} [Cit. {today_date}]'.format(
                    idDotace=idDotace, today_date=today_date)

                amount_in_czk = 0
                eu_cofinancing_amount_in_czk = 0
                eu_fund = None

                cur.execute("""
                    SELECT
                        "idRozhodnuti",
                        "castkaPozadovana",
                        "castkaRozhodnuta",
                        "rokRozhodnuti",
                        "iriFinancniZdroj"
                    FROM rozhodnuti
                    WHERE "idDotace" = %(idDotace)s
                    """,
                            {'idDotace': idDotace})

                rozhodnuti_records = list(cur.fetchall())

                for rozhodnuti_record in rozhodnuti_records:
                    (
                        idRozhodnuti,
                        castkaPozadovana,
                        castkaRozhodnuta,
                        rokRozhodnuti,
                        iriFinancniZdroj
                    ) = rozhodnuti_record

                    cur.execute("""
                        SELECT
                            "idObdobi",
                            "castkaCerpana",
                            "castkaUvolnena",
                            "castkaSpotrebovana",
                            "rozpoctoveObdobi"
                        FROM rozpoctoveobdobi
                        WHERE "idRozhodnuti" = %(idRozhodnuti)s
                        """,
                                {'idRozhodnuti': idRozhodnuti})

                    rozpoctoveobdobi_records = list(cur.fetchall())

                    for rozpoctoveobdobi_record in rozpoctoveobdobi_records:
                        (idObdobi, castkaCerpana, castkaUvolnena, castkaSpotrebovana,
                         rozpoctoveObdobi) = rozpoctoveobdobi_record

                        amount_in_czk += castkaCerpana

                        if iriFinancniZdroj in eu_finance_sources_names:
                            eu_cofinancing_amount_in_czk += castkaCerpana
                            eu_fund = eu_finance_source_name_to_fund[iriFinancniZdroj]

                subsidy.amount_in_original_currency = amount_in_czk
                subsidy.eu_cofinancing_amount_in_original_currency = eu_cofinancing_amount_in_czk

                subsidy.amount_in_czk = amount_in_czk
                subsidy.eu_cofinancing_amount_in_czk = eu_cofinancing_amount_in_czk

                if int(subsidy.year) >= 1999:
                    eur_rate = get_eur_to_czk_rate(subsidy.year)

                    subsidy.currency_exchange_to_eur = get_eur_to_czk_rate_text(subsidy.year)
                    subsidy.amount_in_eur = round(amount_in_czk / decimal.Decimal(eur_rate))
                    subsidy.eu_cofinancing_amount_in_eur = round(
                        eu_cofinancing_amount_in_czk / decimal.Decimal(eur_rate))

                subsidy.eu_cofinancing_from_fund = eu_fund

                subsidies.append(subsidy)

        return subsidies
