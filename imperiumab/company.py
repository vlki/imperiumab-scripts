class Company:
    def __init__(self):
        self.name = None
        self.country_code = None
        self.identifier = None
        self.address = None
        self.exists_since = None
        self.exists_until = None

    def __str__(self):
        return 'Company {self.name} ({self.country_code}, {self.identifier})'.format(self=self)
