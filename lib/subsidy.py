class Subsidy:
    def __init__(self):
        self.id = None
        self.year = None
        self.amount_in_czk = None

    def __str__(self):
        return 'Subsidy {self.id} ({self.year}, {self.amount_in_czk} CZK)'.format(self=self)
