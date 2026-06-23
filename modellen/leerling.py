from .gebruiker import Gebruiker

class Leerling(Gebruiker):
    def __init__(self, gebruiker_id, gebruikersnaam, voornaam,
                 tussenvoegsels, achternaam, email, wachtwoord,
                 klas, leerjaar, mentor):

        # constructor van Gebruiker aanroep
        super().__init__(
            gebruiker_id=gebruiker_id,
            gebruikersnaam=gebruikersnaam,
            voornaam=voornaam,
            tussenvoegsels=tussenvoegsels,
            achternaam=achternaam,
            email=email,
            wachtwoord=wachtwoord, #hash uit database
            rol="leerling",
            wachtwoord_is_gehasht=True
        )

        # leerling gegevens
        self.klas = klas
        self.leerjaar = leerjaar
        self.mentor = mentor

    def __str__(self):
        return f"{self.volledige_naam()} - Leerling {self.klas} (jaar {self.leerjaar})"
