import psycopg2


class KokesOdDbAres:
    def __init__(self, connstring):
        self.conn = psycopg2.connect(connstring, options='-c search_path=ares')

    def find_info_for_company_identifier(self, company_identifier):
        info = None

        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT
                    "obchodni_firma",
                    "datum_zapisu",
                    "datum_vymazu",
                    "sidlo"
                FROM firmy
                WHERE "ico" = %(identifier)s
                """,
                        {'identifier': company_identifier})

            firmy_records = list(cur.fetchall())

            for firmy_record in firmy_records:
                (
                    obchodni_firma,
                    datum_zapisu,
                    datum_vymazu,
                    sidlo
                ) = firmy_record

                address = ''

                if 'text' in sidlo:
                    address += sidlo['text']

                if 'ulice' in sidlo:
                    address += sidlo['ulice']
                if 'ulice' not in sidlo and 'obec' in sidlo and ('cisloTxt' in sidlo or 'cisloPop' in sidlo or 'cisloOr' in sidlo):
                    address += sidlo['obec']

                if 'cisloTxt' in sidlo:
                    address += ' ' + sidlo['cisloTxt']
                if 'cisloPop' in sidlo:
                    address += ' ' + sidlo['cisloPop']
                if 'cisloOr' in sidlo:
                    address += '/' + sidlo['cisloOr']

                if ('obec' in sidlo or 'psc' in sidlo) and address != '':
                    address += ', '

                if 'obec' in sidlo and 'psc' in sidlo:
                    address += sidlo['psc'] + ' ' + sidlo['obec']
                if 'obec' in sidlo and 'psc' not in sidlo:
                    address += sidlo['obec']
                if 'obec' not in sidlo and 'psc' in sidlo:
                    address += sidlo['psc']

                address += ', Česká republika'

                info = {
                    'name': obchodni_firma,
                    'address': address,
                    'exists_since': datum_zapisu,
                    'exists_until': datum_vymazu
                }

        return info
