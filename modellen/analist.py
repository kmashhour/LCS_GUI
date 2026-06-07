from .gebruiker import Gebruiker

class Analist(Gebruiker):
    def __init__(self, gebruiker_id, gebruikersnaam, voornaam,
                 tussenvoegsels, achternaam, email, wachtwoord):

        # constructor van Gebruiker aanroepen
        super().__init__(
            gebruiker_id,
            gebruikersnaam,
            voornaam,
            tussenvoegsels,
            achternaam,
            email,
            wachtwoord,
            rol="analist"
        )

    def __str__(self):
        return f"{self.volledige_naam()} - Analist"
