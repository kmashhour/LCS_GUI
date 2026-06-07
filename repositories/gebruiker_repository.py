import sqlite3
from modellen.gebruiker import Gebruiker

class GebruikerRepository:
    def __init__(self, database_pad):
        self.database_pad = database_pad

    def _connect(self):
        conn = sqlite3.connect(self.database_pad)
        conn.row_factory = sqlite3.Row
        return conn

    def get_all(self):
        conn = self._connect()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Gebruiker")
        rows = cursor.fetchall()
        conn.close()

        gebruikers = []
        for row in rows:
            gebruiker = Gebruiker(
                gebruiker_id=row["gebruiker_id"],
                gebruikersnaam=row["gebruikersnaam"],
                voornaam=row["voornaam"],
                tussenvoegsels=row["tussenvoegsels"],
                achternaam=row["achternaam"],
                email=row["email"],
                wachtwoord=row["wachtwoord"],
                rol=row["rol"]
            )
            gebruikers.append(gebruiker)

        return gebruikers

    def get_by_id(self, gebruiker_id):
        conn = self._connect()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Gebruiker WHERE gebruiker_id = ?", (gebruiker_id,))
        row = cursor.fetchone()
        conn.close()

        if row is None:
            return None

        return Gebruiker(
            gebruiker_id=row["gebruiker_id"],
            gebruikersnaam=row["gebruikersnaam"],
            voornaam=row["voornaam"],
            tussenvoegsels=row["tussenvoegsels"],
            achternaam=row["achternaam"],
            email=row["email"],
            wachtwoord=row["wachtwoord"],
            rol=row["rol"]
        )
