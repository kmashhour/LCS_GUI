class Studiejaar:
    def __init__(self, studiejaar_id, naam, startdatum, einddatum):
        self.studiejaar_id = studiejaar_id
        self.naam = naam
        self.startdatum = startdatum
        self.einddatum = einddatum

    def __repr__(self):
        return f"Studiejaar({self.naam}, {self.startdatum} t/m {self.einddatum})"
