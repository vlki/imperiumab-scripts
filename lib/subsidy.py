class Subsidy:
    def __init__(self):
        self.id = None
        self.beneficiary = None
        self.beneficiary_original_name = None
        self.country_code = None
        self.project_code = None
        self.project_name = None
        self.programme_code = None
        self.programme_name = None
        self.signed_on = None
        self.year = None
        
        self.original_currency = None        
        self.amount_in_original_currency = None
        self.eu_cofinancing_amount_in_original_currency = None
        
        self.currency_exchange_to_eur = None
        self.amount_in_eur = None
        self.eu_cofinancing_amount_in_eur = None

        self.currency_exchange_to_czk = None
        self.amount_in_czk = None
        self.eu_cofinancing_amount_in_czk = None

        self.eu_cofinancing_from_fund = None
        self.eu_cofinancing_from_period = None

        self.source = None

    def __str__(self):
        return 'Subsidy {self.id}, {self.amount_in_czk} CZK to {self.beneficiary} in {self.year}, for {self.project_name}'.format(self=self)
