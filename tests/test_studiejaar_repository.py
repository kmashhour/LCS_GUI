from repositories.studiejaar_repository import StudiejaarRepository


def test_get_all_studiejaren():
    repo = StudiejaarRepository()

    studiejaren = repo.get_all()

    assert len(studiejaren) > 0


def test_get_studiejaar_for_date():
    repo = StudiejaarRepository()

    studiejaar = repo.get_studiejaar_for_date("2026-06-25")

    assert studiejaar is not None
    assert studiejaar.naam == "25-26"