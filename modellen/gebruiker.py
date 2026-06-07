class Gebruiker:
    def __init__(self, gebruiker_id, gebruikersnaam, voornaam,
                 tussenvoegsels, achternaam, email, wachtwoord, rol):

        if not gebruikersnaam:
            raise ValueError("gebruikersnaam mag niet leeg zijn")
        if not voornaam:
            raise ValueError("voornaam mag niet leeg zijn")
        if not achternaam:
            raise ValueError("achternaam mag niet leeg zijn")
        if "@" not in email:
            raise ValueError("email is ongeldig")
        if rol not in ["leerling", "docent", "analist"]:
            raise ValueError("rol moet leerling, docent of analist zijn")

        self.gebruiker_id = gebruiker_id
        self.gebruikersnaam = gebruikersnaam
        self.voornaam = voornaam
        self.tussenvoegsels = tussenvoegsels
        self.achternaam = achternaam
        self.email = email
        self.__wachtwoord = wachtwoord   # PRIVATE
        self.rol = rol

    def volledige_naam(self):
        if not self.tussenvoegsels:
            return f"{self.voornaam} {self.achternaam}"
        return f"{self.voornaam} {self.tussenvoegsels} {self.achternaam}"

    def __str__(self):
        return f"{self.gebruikersnaam} ({self.volledige_naam()}) - rol: {self.rol}"
