class Periode:
    def __init__(self, periode_id, studiejaar_id, periode_nummer, startdatum, einddatum):
        self.periode_id = periode_id
        self.studiejaar_id = studiejaar_id
        self.periode_nummer = periode_nummer
        self.startdatum = startdatum
        self.einddatum = einddatum

    def __repr__(self):
        return f"Periode({self.periode_nummer}, studiejaar_id={self.studiejaar_id})"