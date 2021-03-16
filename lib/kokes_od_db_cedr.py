import psycopg2
from pprint import pprint

from lib.subsidy import Subsidy

class KokesOdDbCedr:
    def __init__(self, connstring):
        self.conn = psycopg2.connect(connstring, options='-c search_path=cedr')

    def search_subsidies_of_company(self, company):
        subsidies = []

        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT
                    "idDotace",
                    "projektIdentifikator",
                    "podpisDatum"
                FROM dotace
                WHERE "idPrijemce" = %(identifier)s
                """,
                {'identifier': company.identifier})

            dotace_records = list(cur.fetchall())

            for dotace_record in dotace_records:
                (idDotace, projektIdentifikator, podpisDatum) = dotace_record
                # pprint(podpisDatum.year)

                subsidy = Subsidy()
                subsidy.id = projektIdentifikator.strip()
                subsidy.amount_in_czk = 0

                # TODO: is ok to use date of sign?
                subsidy.year = podpisDatum.year

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
                    (idRozhodnuti, castkaPozadovana, castkaRozhodnuta, rokRozhodnuti, iriFinancniZdroj) = rozhodnuti_record
                    # pprint(rozhodnuti_record)

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
                        (idObdobi, castkaCerpana, castkaUvolnena, castkaSpotrebovana, rozpoctoveObdobi) = rozpoctoveobdobi_record

                        subsidy.amount_in_czk += castkaCerpana

                        # pprint(rozpoctoveobdobi_record)

                subsidies.append(subsidy)

        return subsidies
