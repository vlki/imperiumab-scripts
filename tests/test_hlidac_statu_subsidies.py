from datetime import date
import decimal
import json

from imperiumab.company import Company
from imperiumab import hlidac_statu_subsidies


def test_map_subsidy_cedr_agri():
    com = Company()
    com.name = '1. Hradecká zemědělská a.s.'

    hs_subsidy = json.loads(
        '{"IdDotace":"cedr-df72bb1f69ef6e091995f9678ff4f48c31a4df60","DatumPodpisu":"2000-07-27T00:00:00Z","DatumAktualizace":"2000-12-31T00:00:00Z","KodProjektu":"347/2000-2163","Zdroj":{"Nazev":"cedr","Url":"http://cedropendata.mfcr.cz/c3lod/cedr/resource/Dotace/DF72BB1F69EF6E091995F9678FF4F48C31A4DF60"},"Prijemce":{"Ico":"63479401","ObchodniJmeno":"1. Hradecká zemědělská a.s.","HlidacJmeno":"1. Hradecká zemědělská a.s.","Obec":"Hradec nad Moravicí","Okres":"Opava","PSC":"74741"},"DotaceCelkem":389250.0,"PujckaCelkem":0.0,"Rozhodnuti":[{"CastkaPozadovana":389250.0,"CastkaRozhodnuta":389250.0,"CerpanoCelkem":389250.0,"JePujcka":false,"IcoPoskytovatele":"00020478","Poskytovatel":"Ministerstvo zemědělství","Rok":2000,"ZdrojFinanci":"Ministerstvo zemědělství","Cerpani":[{"CastkaSpotrebovana":389250.0,"Rok":2000,"GuessedYear":2000}]}],"Chyba":[]}')

    s = hlidac_statu_subsidies.map_hlidac_statu_subsidy_to_subsidy(com, hs_subsidy, today_date=date(2021, 4, 1))

    assert s.id == 'CEDR-df72bb1f69ef6e091995f9678ff4f48c31a4df60'
    assert s.beneficiary == '1. Hradecká zemědělská a.s.'
    assert s.beneficiary_original_name == '1. Hradecká zemědělská a.s.'
    assert s.country_code == 'CZ'

    assert s.project_code == '347/2000-2163'
    assert s.project_name == None
    assert s.programme_code == None
    assert s.programme_name == None

    assert s.signed_on == date(2000, 7, 27)
    assert s.year == 2000

    assert s.amount_in_original_currency == 389250.0
    assert s.amount_in_czk == 389250.0
    assert s.amount_in_eur == 11150.0

    assert s.currency_exchange_to_czk == None
    assert s.currency_exchange_to_eur == 'Dle kurzu CZK/EUR 34.911 z roku 2000. Zdroj: Devízové kurzy vedené Českou národní bankou. Dostupné z: https://www.cnb.cz/cs/financni-trhy/devizovy-trh/kurzy-devizoveho-trhu/kurzy-devizoveho-trhu/prumerne_form.html'

    assert s.eu_cofinancing_from_fund == None
    assert s.eu_cofinancing_from_period == None

    assert s.source == 'Záznam dotace cedr-df72bb1f69ef6e091995f9678ff4f48c31a4df60 v databázi Hlídač státu. Dostupné z: https://www.hlidacstatu.cz/Dotace/Detail/cedr-df72bb1f69ef6e091995f9678ff4f48c31a4df60 [Cit. 2021-04-01]'


def test_map_subsidy_szif():
    com = Company()
    com.name = '1. Hradecká zemědělská a.s.'

    hs_subsidy = json.loads(
        '{"IdDotace":"szif-spd2017-10","NazevProjektu":"Dojnice (VCS)","Zdroj":{"Nazev":"szif 2017","Url":"https://www.szif.cz/cs"},"Prijemce":{"Ico":"63479401","ObchodniJmeno":"1. Hradecká zemědělská a.s.","HlidacJmeno":"1. Hradecká zemědělská a.s.","Obec":"Hradec nad Moravicí","Okres":"Opava"},"Program":{"Nazev":"Dojnice (VCS)"},"DotaceCelkem":2000909.66,"PujckaCelkem":0.0,"Rozhodnuti":[{"CastkaRozhodnuta":0.0,"CerpanoCelkem":0.0,"Poskytovatel":"CZ","Rok":2017,"Cerpani":[{"CastkaSpotrebovana":0.0,"GuessedYear":2017}]},{"CastkaRozhodnuta":0.0,"CerpanoCelkem":2000909.66,"Poskytovatel":"EU","Rok":2017,"Cerpani":[{"CastkaSpotrebovana":2000909.66,"GuessedYear":2017}]}],"Chyba":[]}')

    s = hlidac_statu_subsidies.map_hlidac_statu_subsidy_to_subsidy(com, hs_subsidy, today_date=date(2021, 4, 1))

    assert s.id == 'SZIF-spd2017-10'
    assert s.beneficiary == '1. Hradecká zemědělská a.s.'
    assert s.beneficiary_original_name == '1. Hradecká zemědělská a.s.'
    assert s.country_code == 'CZ'

    assert s.project_code == None
    assert s.project_name == 'Dojnice (VCS)'
    assert s.programme_code == None
    assert s.programme_name == 'Dojnice (VCS)'

    assert s.signed_on == None
    assert s.year == 2017

    assert s.amount_in_original_currency == decimal.Decimal('2000909.66')
    assert s.amount_in_czk == decimal.Decimal('2000909.66')
    assert s.amount_in_eur == decimal.Decimal('76005')

    assert s.currency_exchange_to_czk == None
    assert s.currency_exchange_to_eur == 'Dle kurzu CZK/EUR 26.326 z roku 2017. Zdroj: Směnné kurzy dle jednotlivých let zveřejněné na serveru Eurostat. Dostupné z: https://ec.europa.eu/eurostat/web/exchange-and-interest-rates/data/database'

    assert s.eu_cofinancing_from_fund == None
    assert s.eu_cofinancing_from_period == None

    assert s.source == 'Záznam dotace szif-spd2017-10 v databázi Hlídač státu. Dostupné z: https://www.hlidacstatu.cz/Dotace/Detail/szif-spd2017-10 [Cit. 2021-04-01]'


def test_map_subsidy_dotinfo():
    com = Company()
    com.name = '1. Hradecká zemědělská a.s.'

    hs_subsidy = json.loads(
        '{"IdDotace":"dotinfo-e329456a-9d2d-4f80-938a-0d4a5322c302","KodProjektu":"115D212001182","NazevProjektu":"CZ.1.02/2.2.00/12.15774 Nákup technologie pro snížení emisí čpavku","Zdroj":{"Nazev":"dotinfo","Url":"https://www.dotinfo.cz/dotace/e329456a-9d2d-4f80-938a-0d4a5322c302"},"Prijemce":{"Ico":"63479401","ObchodniJmeno":"1. Hradecká zemědělská a.s.","HlidacJmeno":"1. Hradecká zemědělská a.s.","Obec":"Hradec nad Moravicí","Okres":"","PSC":"74741"},"Program":{"Nazev":"CZ.1.02/2.2.00/12.15774","Kod":"Nákup technologie pro snížení emisí čpavku"},"DotaceCelkem":0.0,"PujckaCelkem":0.0,"Rozhodnuti":[{"CastkaPozadovana":0.0,"CastkaRozhodnuta":183750.0,"JePujcka":false,"IcoPoskytovatele":"00164801","Poskytovatel":"Ministerstvo životního prostředí","Cerpani":[]}],"Chyba":[]}')

    s = hlidac_statu_subsidies.map_hlidac_statu_subsidy_to_subsidy(com, hs_subsidy, today_date=date(2021, 4, 1))

    assert s.id == 'DOTINFO-e329456a-9d2d-4f80-938a-0d4a5322c302'
    assert s.beneficiary == '1. Hradecká zemědělská a.s.'
    assert s.beneficiary_original_name == '1. Hradecká zemědělská a.s.'
    assert s.country_code == 'CZ'

    assert s.project_code == '115D212001182'
    assert s.project_name == 'CZ.1.02/2.2.00/12.15774 Nákup technologie pro snížení emisí čpavku'
    assert s.programme_code == 'Nákup technologie pro snížení emisí čpavku'
    assert s.programme_name == 'CZ.1.02/2.2.00/12.15774'

    assert s.signed_on == None
    assert s.year == '2007-2013'

    assert s.amount_in_original_currency == decimal.Decimal(0)
    assert s.amount_in_czk == decimal.Decimal(0)
    assert s.amount_in_eur == decimal.Decimal(0)

    assert s.currency_exchange_to_czk == None
    assert s.currency_exchange_to_eur == None

    assert s.eu_cofinancing_from_fund == None
    assert s.eu_cofinancing_from_period == None

    assert s.source == 'Záznam dotace dotinfo-e329456a-9d2d-4f80-938a-0d4a5322c302 v databázi Hlídač státu. Dostupné z: https://www.hlidacstatu.cz/Dotace/Detail/dotinfo-e329456a-9d2d-4f80-938a-0d4a5322c302 [Cit. 2021-04-01]'


def test_map_subsidy_eufondy():
    com = Company()
    com.name = 'Lovochemie, a.s.'

    hs_subsidy = json.loads(
        '{"IdDotace":"eufondy-07-13-cz-1-02-5-1-00-13-20380","DatumPodpisu":"2014-10-03T00:00:00","KodProjektu":"CZ.1.02/5.1.00/13.20380","NazevProjektu":"Zvýšení provozní bezpečnosti páteřního rozvodu kapalného čpavku","Zdroj":{"Nazev":"eufondy 2007-2013","Url":"https://dotaceeu.cz/cs/evropske-fondy-v-cr/programove-obdobi-2007-2013/cerpani-v-obdobi-2007-2013"},"Prijemce":{"Ico":"49100262","ObchodniJmeno":"Lovochemie, a.s.","HlidacJmeno":"Lovochemie, a.s.","Obec":"Lovosice","PSC":"41002"},"Program":{"Nazev":"OP Životní prostředí","Kod":"CZ.1.02"},"DotaceCelkem":9429927.5,"PujckaCelkem":0.0,"Rozhodnuti":[{"CastkaRozhodnuta":0.0,"Poskytovatel":"CZ","Cerpani":[]},{"CastkaRozhodnuta":9444750.0,"CerpanoCelkem":9429927.5,"Poskytovatel":"EU","Cerpani":[{"CastkaSpotrebovana":9429927.5,"GuessedYear":2014}]}],"Duplicita":"cedr-003F3E688055492BA591F2E6D98B1BC5E7A503AF","Chyba":[]}')

    s = hlidac_statu_subsidies.map_hlidac_statu_subsidy_to_subsidy(com, hs_subsidy, today_date=date(2021, 4, 1))

    assert s.id == 'EUFONDY-07-13-cz-1-02-5-1-00-13-20380'
    assert s.beneficiary == 'Lovochemie, a.s.'
    assert s.beneficiary_original_name == 'Lovochemie, a.s.'
    assert s.country_code == 'CZ'

    assert s.project_code == 'CZ.1.02/5.1.00/13.20380'
    assert s.project_name == 'Zvýšení provozní bezpečnosti páteřního rozvodu kapalného čpavku'
    assert s.programme_code == 'CZ.1.02'
    assert s.programme_name == 'OP Životní prostředí'

    assert s.signed_on == date(2014, 10, 3)
    assert s.year == 2014

    assert s.amount_in_original_currency == decimal.Decimal('9429927.5')
    assert s.amount_in_czk == decimal.Decimal('9429927.5')
    assert s.amount_in_eur == decimal.Decimal('342458')

    assert s.currency_exchange_to_czk == None
    assert s.currency_exchange_to_eur == 'Dle kurzu CZK/EUR 27.536 z roku 2014. Zdroj: Směnné kurzy dle jednotlivých let zveřejněné na serveru Eurostat. Dostupné z: https://ec.europa.eu/eurostat/web/exchange-and-interest-rates/data/database'

    assert s.eu_cofinancing_from_fund == None
    assert s.eu_cofinancing_from_period == None
