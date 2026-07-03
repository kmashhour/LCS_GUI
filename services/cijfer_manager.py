from datetime import date
from repositories.cijfer_repository import CijferRepository
from modellen.cijfer import Cijfer
from services.periode_service import PeriodeService
from decimal import Decimal, ROUND_HALF_UP
# hulpfunctie afronden naar boven
def naar_boven_afronden(getal):
    return float(Decimal(str(getal)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP))

class CijferManager:
    def __init__(self, cijfer_repo=None, periode_service=None):
        self.cijfer_repo = cijfer_repo or CijferRepository()
        self.periode_service = periode_service or PeriodeService()

    # afrond functie naar boven overbodig hier staat twee keer in.
    #def naar_boven_afronden(getal):
        #return float(Decimal(str(getal)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP))
        
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
    
    # maakt van losse Cijfer objecten een overzicht per leerling
    def get_docent_dashboard_overzicht(self, docent_id, klas, periode_obj):
        studiejaar_obj = self.periode_service.studiejaar_repo.get_by_id(
            periode_obj.studiejaar_id
        )
        studiejaar_str = studiejaar_obj.naam
        periode_nummer = periode_obj.periode_nummer
        cijfers = self.cijfer_repo.get_by_docent_klas_studiejaar_periode(
            docent_id=docent_id,
            klas=klas,
            studiejaar_id=studiejaar_str,
            periode_id=periode_nummer
        )

        overzicht = {}

        for cijfer in cijfers:
            leerling_id = cijfer.leerling.gebruiker_id

            if leerling_id not in overzicht:
                overzicht[leerling_id] = {
                    "leerling": cijfer.leerling,
                    "cijfers": []
                }

            overzicht[leerling_id]["cijfers"].append(cijfer)

        resultaten = []

        for data in overzicht.values():
            leerling = data["leerling"]
            leerling_cijfers = data["cijfers"]

            po_gem = self.bereken_po_gemiddelde(leerling_cijfers)
            toets = self.get_toets_cijfer(leerling_cijfers)
            eind = self.bereken_eindcijfer(leerling_cijfers)
            aantal = len(leerling_cijfers)

            resultaten.append({
                "leerling": leerling,
                "po_gemiddelde": po_gem,
                "toets": toets,
                "eindcijfer": eind,
                "aantal_cijfers": aantal
            })

        return resultaten
    
    def get_laatste_klas_van_docent(self, docent_id):
        return self.cijfer_repo.get_laatste_klas_van_docent(docent_id)
    
    def sla_cijfer_op(self, leerling, onderdeel, docent, waarde, datum, studiejaar, periode):
        cijfer = Cijfer(
            cijfer_id=None,
            leerling=leerling,
            onderdeel=onderdeel,
            docent=docent,
            waarde=waarde,
            datum=datum
        )

        cijfer.studiejaar = studiejaar
        cijfer.periode = periode

        return self.cijfer_repo.insert(cijfer)
