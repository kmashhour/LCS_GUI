from repositories.cijfer_repository import CijferRepository
from services.periode_service import PeriodeService
from modellen.cijfer import Cijfer

class CijferManager:
    def __init__(self, db_pad):
        self.cijfer_repo = CijferRepository(db_pad)
        self.periode_service = PeriodeService(db_pad)

    # Nieuw cijfer opslaan
    def voeg_cijfer_toe(self, leerling_id, onderdeel_id, docent_id, waarde, afnamedatum):
        """
        afnamedatum: 'yyyy-mm-dd'
        """

        # Bepalen studiejaar + periode obv afnamedatum
        kader = self.periode_service.get_kader_datum(afnamedatum)

        studiejaar = kader["studiejaar"]
        periode = kader["periode"]

        # Maak Cijfer-domeinobject
        cijfer = Cijfer(
            cijfer_id=None,
            leerling_id=leerling_id,
            onderdeel_id=onderdeel_id,
            docent_id=docent_id,
            waarde=waarde,
            datum=afnamedatum,
            studiejaar=studiejaar,
            periode=periode
        )

        # Opslaan in database
        return self.cijfer_repo.insert(cijfer)

    # Cijfer wijzigen(studiejar/periode opnieuw bepalen)
    def wijzig_cijfer(self, cijfer_id, nieuwe_waarde, nieuwe_afnamedatum):
        kader = self.periode_service.get_kader_datum(nieuwe_afnamedatum)

        studiejaar = kader["studiejaar"]
        periode = kader["periode"]

        return self.cijfer_repo.update(
            cijfer_id=cijfer_id,
            waarde=nieuwe_waarde,
            datum=nieuwe_afnamedatum,
            studiejaar=studiejaar,
            periode=periode
        )
    
    # cijfers per leerling ophalen
    def get_cijfers_leerling(self, leerling_id):
        return self.cijfer_repo.get_by_leerling(leerling_id)

    # cijfers per studiejaar ophlen
    def get_cijfers_studiejaar(self, leerling_id, studiejaar):
        return self.cijfer_repo.get_by_studiejaar(leerling_id, studiejaar)

    # cijfers per periode ophalen
    def get_cijfers_periode(self, leerling_id, studiejaar, periode):
        return self.cijfer_repo.get_by_studiejaar_en_periode(leerling_id, studiejaar, periode)

    # Gemiddelde per periode
    def bereken_gemiddelde_per_periode(self, leerling_id, studiejaar, periode):
        cijfers = self.get_cijfers_periode(leerling_id, studiejaar, periode)
        if not cijfers:
            return None
        return sum(c.waarde for c in cijfers) / len(cijfers)

    # Gemiddelde per studiejaar
    def bereken_gemiddelde_per_studiejaar(self, leerling_id, studiejaar):
        cijfers = self.get_cijfers_studiejaar(leerling_id, studiejaar)
        if not cijfers:
            return None
        return sum(c.waarde for c in cijfers) / len(cijfers)
