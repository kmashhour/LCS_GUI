from datetime import date
from repositories.studiejaar_repository import StudiejaarRepository
from repositories.periode_repository import PeriodeRepository

class PeriodeService:
    def __init__(self, db_pad):
        self.studiejaar_repo = StudiejaarRepository(db_pad)
        self.periode_repo = PeriodeRepository(db_pad)

    # Datum format: yyyy-mm-dd 
    def _vandaag(self):
        return date.today().strftime("%Y-%m-%d")

    # Bepal huidig studiejaar obv huidig datum
    def get_huidig_studiejaar(self):
        vandaag = self._vandaag()
        return self.studiejaar_repo.get_studiejaar_for_date(vandaag)

    # Bepaal huidige periode obv vandaag
    def get_huidige_periode(self):
        vandaag = self._vandaag()
        return self.periode_repo.get_periode_for_date(vandaag)

    # Bepalen studiejaar obv een datum
    def get_studiejaar_voor_datum(self, datum):
        return self.studiejaar_repo.get_studiejaar_for_date(datum)

    # Bepaal periode obv een datum
    def get_periode_voor_datum(self, datum):
        return self.periode_repo.get_periode_for_date(datum)

    # kader voor een datum
    def get_kader_datum(self, datum):
        studiejaar = self.get_studiejaar_voor_datum(datum)
        periode = self.get_periode_voor_datum(datum)

        return {
            "studiejaar": studiejaar.naam if studiejaar else None,
            "studiejaar_id": studiejaar.studiejaar_id if studiejaar else None,
            "periode": periode.periode_nummer if periode else None,
            "periode_id": periode.periode_id if periode else None
        }

    # kader voor vandaag
    def get_datum_kader(self):
        vandaag = self._vandaag()
        return self.get_kader_datum(vandaag)
