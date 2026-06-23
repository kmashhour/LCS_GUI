import hashlib
import os

class Gebruiker:
    TOEGESTANE_ROLLEN = ["leerling", "docent", "analist"]

    def __init__(
        self,
        gebruiker_id,
        gebruikersnaam,
        voornaam,
        tussenvoegsels,
        achternaam,
        email,
        wachtwoord,
        rol,
        wachtwoord_is_gehasht=False
    ):
        # validatie
        if not gebruikersnaam:
            raise ValueError("gebruikersnaam mag niet leeg zijn")
        if not voornaam:
            raise ValueError("voornaam mag niet leeg zijn")
        if not achternaam:
            raise ValueError("achternaam mag niet leeg zijn")
        if "@" not in email:
            raise ValueError("email is ongeldig")
        if rol not in self.TOEGESTANE_ROLLEN:
            raise ValueError(f"rol moet één van {self.TOEGESTANE_ROLLEN} zijn")

        self.gebruiker_id = gebruiker_id
        self.gebruikersnaam = gebruikersnaam
        self.voornaam = voornaam
        self.tussenvoegsels = tussenvoegsels
        self.achternaam = achternaam
        self.email = email
        self.rol = rol

        # Wachtwoord veilig met hash opslaan
        if wachtwoord_is_gehasht:
            self.__wachtwoord_hash = wachtwoord
        else:
            self.__wachtwoord_hash = self._hash_wachtwoord(wachtwoord)

    # ww hashing
    @staticmethod
    def _hash_wachtwoord(wachtwoord):
        salt = os.urandom(16)
        hash_value = hashlib.pbkdf2_hmac(
            "sha256",
            wachtwoord.encode("utf-8"),
            salt,
            100000
        )
        return salt.hex() + ":" + hash_value.hex()

    def verify_wachtwoord(self, wachtwoord):
        salt_hex, hash_hex = self.__wachtwoord_hash.split(":")
        salt = bytes.fromhex(salt_hex)
        hash_value = hashlib.pbkdf2_hmac(
            "sha256",
            wachtwoord.encode("utf-8"),
            salt,
            100000
        )
        return hash_value.hex() == hash_hex

    @property
    def wachtwoord_hash(self):
        return self.__wachtwoord_hash

    # naam
    def volledige_naam(self):
        if self.tussenvoegsels:
            return f"{self.voornaam} {self.tussenvoegsels} {self.achternaam}"
        return f"{self.voornaam} {self.achternaam}"

    def __str__(self):
        return f"{self.gebruikersnaam} ({self.volledige_naam()}) - rol: {self.rol}"
