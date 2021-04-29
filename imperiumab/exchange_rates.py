import decimal


def get_eur_to_czk_rate(year):
    rates = {
        '2021': 26.070, # Eurostat 2021Q1
        '2020': 26.455,
        '2019': 25.670,
        '2018': 25.647,
        '2017': 26.326,
        '2016': 27.034,
        '2015': 27.279,
        '2014': 27.536,
        '2013': 25.980,
        '2012': 25.149,
        '2011': 24.590,
        '2010': 26.284,
        '2009': 26.435,
        '2008': 24.946,

        '2007': 26.829,
        '2006': 28.045,
        '2005': 29.298,
        '2004': 31.126,
        '2003': 32.089,
        '2002': 30.853,
        '2001': 33.202,
        '2000': 34.911,
        '1999': 36.340,
    }

    return rates[str(year)]


def get_eur_to_czk_rate_text(year):
    eur_rate = get_eur_to_czk_rate(year)

    if year >= 2008:
        text = "Dle kurzu CZK/EUR {eur_rate:.3f} z roku {year}. Zdroj: Směnné kurzy dle jednotlivých let zveřejněné na serveru Eurostat. Dostupné z: https://ec.europa.eu/eurostat/web/exchange-and-interest-rates/data/database".format(
            eur_rate=eur_rate, year=year)
    else:
        text = "Dle kurzu CZK/EUR {eur_rate:.3f} z roku {year}. Zdroj: Devízové kurzy vedené Českou národní bankou. Dostupné z: https://www.cnb.cz/cs/financni-trhy/devizovy-trh/kurzy-devizoveho-trhu/kurzy-devizoveho-trhu/prumerne_form.html".format(
            eur_rate=eur_rate, year=year)

    return text


def fill_subsidy_eur_info(subsidy):
    if subsidy.amount_in_czk is None:
        return subsidy

    if subsidy.amount_in_czk == 0:
        subsidy.amount_in_eur = 0

        if subsidy.eu_cofinancing_amount_in_czk is not None:
            subsidy.eu_cofinancing_amount_in_eur = 0

        return subsidy

    year = subsidy.year
    if year == '2007-2013':
        year = 2017

    # Euro started on Jan 1st, 1999
    if year < 1999:
        return subsidy

    eur_rate = get_eur_to_czk_rate(year)
    eur_rate_text = get_eur_to_czk_rate_text(year)

    subsidy.amount_in_eur = round(subsidy.amount_in_czk / decimal.Decimal(eur_rate))
    subsidy.currency_exchange_to_eur = eur_rate_text

    if subsidy.eu_cofinancing_amount_in_czk is not None:
        subsidy.eu_cofinancing_amount_in_eur = round(
            subsidy.eu_cofinancing_amount_in_czk / decimal.Decimal(eur_rate))

    return subsidy
