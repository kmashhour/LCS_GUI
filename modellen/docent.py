from .gebruiker import Gebruiker

class Docent(Gebruiker):
    def __init__(self, gebruiker_id, gebruikersnaam, voornaam,
                 tussenvoegsels, achternaam, email, wachtwoord,
                 vakgebied):

        # constructor van Gebruiker aanroepen
        super().__init__(
            gebruiker_id=gebruiker_id,
            gebruikersnaam=gebruikersnaam,
            voornaam=voornaam,
            tussenvoegsels=tussenvoegsels,
            achternaam=achternaam,
            email=email,
            wachtwoord=wachtwoord,     #hash uit database
            rol="docent",
            wachtwoord_is_gehasht=True
        )

        # docent eigenschap
        self.vakgebied = vakgebied

    def __str__(self):
        return f"{self.volledige_naam()} - Docent ({self.vakgebied})"
