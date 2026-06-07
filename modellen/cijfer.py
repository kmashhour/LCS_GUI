class Cijfer:
    def __init__(self, cijfer_id, leerling, onderdeel, docent, waarde, datum):
        # Validatie
        if waarde < 0 or waarde > 100:
            raise ValueError("waarde moet tussen 0 en 100 liggen (bijv. 72 = 7.2)")

        if leerling is None:
            raise ValueError("leerling mag niet leeg zijn")

        if onderdeel is None:
            raise ValueError("onderdeel mag niet leeg zijn")

        if docent is None:
            raise ValueError("docent mag niet leeg zijn")

        self.cijfer_id = cijfer_id
        self.leerling = leerling
        self.onderdeel = onderdeel
        self.docent = docent
        self.waarde = waarde      # opgeslagen als int (72 = 7.2)
        self.datum = datum

    def get_decimaal(self):
        """het cijfer terug als int 72 wordt 7.2"""
        return self.waarde / 10

    def __str__(self):
        return f"{self.leerling.volledige_naam()} - {self.onderdeel.naam}: {self.get_decimaal()}"
