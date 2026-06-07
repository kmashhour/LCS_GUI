class Onderdeel:
    def __init__(self, onderdeel_id, naam, weging, type):
        # validatie
        if not naam:
            raise ValueError("naam mag niet leeg zijn")

        if type not in ["PO", "Toets"]:
            raise ValueError("type moet 'PO' of 'Toets' zijn")

        if weging < 0 or weging > 1:
            raise ValueError("weging moet tussen 0 en 1 liggen")

        self.onderdeel_id = onderdeel_id
        self.naam = naam
        self.weging = weging
        self.type = type

    def __str__(self):
        return f"{self.naam} ({self.type}, weging {self.weging})"
