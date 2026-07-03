from types import SimpleNamespace
from services.cijfer_manager import CijferManager


def cijfer(waarde, type_onderdeel):
    return SimpleNamespace(
        waarde=waarde,
        onderdeel=SimpleNamespace(type=type_onderdeel),
        get_decimaal=lambda: waarde / 10
    )


def test_bereken_po_gemiddelde():
    manager = CijferManager()

    cijfers = [
        cijfer(70, "PO"),
        cijfer(80, "PO"),
        cijfer(60, "Toets"),
    ]

    assert manager.bereken_po_gemiddelde(cijfers) == 7.5


def test_get_toets_cijfer():
    manager = CijferManager()

    cijfers = [
        cijfer(70, "PO"),
        cijfer(65, "Toets"),
    ]

    assert manager.get_toets_cijfer(cijfers) == 6.5


def test_bereken_eindcijfer():
    manager = CijferManager()

    cijfers = [
        cijfer(70, "PO"),
        cijfer(80, "PO"),
        cijfer(60, "Toets"),
    ]

    assert manager.bereken_eindcijfer(cijfers) == 6.8


def test_bereken_eindcijfer_zonder_toets_geeft_none():
    manager = CijferManager()

    cijfers = [
        cijfer(70, "PO"),
        cijfer(80, "PO"),
    ]

    assert manager.bereken_eindcijfer(cijfers) is None