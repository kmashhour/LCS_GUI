from datetime import date
from repositories.cijfer_repository import CijferRepository
from services.periode_service import PeriodeService
from decimal import Decimal, ROUND_HALF_UP
# hulpfunctie afronden naar boven
def naar_boven_afronden(getal):
    return float(Decimal(str(getal)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP))

class CijferManager:
    def __init__(self, cijfer_repo=None, periode_service=None):
        self.cijfer_repo = cijfer_repo or CijferRepository()
        self.periode_service = periode_service or PeriodeService()

    # afrond functie naar boven
    def naar_boven_afronden(getal):
        return float(Decimal(str(getal)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP))
    # dashboard functies
    def get_huidig_studiejaar(self, leerling_id):
        vandaag = date.today().isoformat()
        kader = self.periode_service.get_kader_datum(vandaag)
        return kader["studiejaar"]

    def get_laatste_periode(self, leerling_id):
        vandaag = date.today().isoformat()
        kader = self.periode_service.get_kader_datum(vandaag)
        return kader["periode"]

    def get_cijfers_per_leerling_per_periode(self, leerling_id, periode_obj):
        studiejaar_obj = self.periode_service.studiejaar_repo.get_by_id(periode_obj.studiejaar_id)
        studiejaar_str = studiejaar_obj.naam
        periode_nummer = periode_obj.periode_nummer

        return self.cijfer_repo.get_by_studiejaar_en_periode(
            leerling_id,
            studiejaar_str,
            periode_nummer
        )

    # kpi functies
    def bereken_po_gemiddelde(self, cijfers):
        pos = [c for c in cijfers if c.onderdeel.type == "PO"]
        if not pos:
            return None
        return sum(c.get_decimaal() for c in pos) / len(pos)

    def get_toets_cijfer(self, cijfers):
        toetsen = [c for c in cijfers if c.onderdeel.type == "Toets"]
        if not toetsen:
            return None
        return toetsen[-1].get_decimaal()

    def bereken_eindcijfer(self, cijfers):
        po_gem = self.bereken_po_gemiddelde(cijfers)
        toets = self.get_toets_cijfer(cijfers)

        if po_gem is None or toets is None:
            return None
        # eerst afronden op 1 decimaal
        po_gem = round(po_gem, 1)
        toets = round(toets, 1)
        eind = (po_gem + toets) / 2
        return naar_boven_afronden(eind)


    def tel_po_onderdelen(self, cijfers):
        return len([c for c in cijfers if c.onderdeel.type == "PO"])
