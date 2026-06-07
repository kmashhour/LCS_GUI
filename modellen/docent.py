from .gebruiker import Gebruiker

class Docent(Gebruiker):
    def __init__(self, gebruiker_id, gebruikersnaam, voornaam,
                 tussenvoegsels, achternaam, email, wachtwoord,
                 vakgebied):

        # constructor van Gebruiker aanroepen
        super().__init__(
            gebruiker_id,
            gebruikersnaam,
            voornaam,
            tussenvoegsels,
            achternaam,
            email,
            wachtwoord,
            rol="docent"
        )

        # docent eigenschap
        self.vakgebied = vakgebied

    def __str__(self):
        return f"{self.volledige_naam()} - Docent ({self.vakgebied})"
