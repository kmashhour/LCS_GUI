from datetime import date
from repositories.studiejaar_repository import StudiejaarRepository
from repositories.periode_repository import PeriodeRepository

class PeriodeService:
    def __init__(self, studiejaar_repo=None, periode_repo=None):
        self.studiejaar_repo = studiejaar_repo or StudiejaarRepository()
        self.periode_repo = periode_repo or PeriodeRepository()

    def get_studiejaar_for_date(self, datum):
        return self.studiejaar_repo.get_studiejaar_for_date(datum)

    def get_periode_for_date(self, datum):
        return self.periode_repo.get_periode_for_date(datum)

    def get_kader_datum(self, datum):
        sj = self.get_studiejaar_for_date(datum)
        p = self.get_periode_for_date(datum)
        return {"studiejaar": sj, "periode": p}
