from repositories.cijfer_repository import CijferRepository


def test_get_by_docent_klas_studiejaar_periode_geeft_cijfers():
    repo = CijferRepository()

    cijfers = repo.get_by_docent_klas_studiejaar_periode(
        docent_id=5,
        klas="4hinf1",
        studiejaar_id="25-26",
        periode_id=4
    )

    assert len(cijfers) > 0
    assert cijfers[0].leerling.klas == "4hinf1"
    assert cijfers[0].docent.gebruiker_id == 5


def test_bestaat_cijfer_geeft_boolean():
    repo = CijferRepository()

    bestaat = repo.bestaat_cijfer(
        leerling_id=1,
        onderdeel_id=1,
        studiejaar="25-26",
        periode=4
    )

    assert isinstance(bestaat, bool)