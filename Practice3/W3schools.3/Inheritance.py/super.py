class Sport:
    def __init__(self, country):
        self.country = country

class Football(Sport):
    def __init__(self, country, team):
        super().__init__(country)
        self.team = team

fc = Football("France", "PSG")
print(fc.country)
print(fc.team)