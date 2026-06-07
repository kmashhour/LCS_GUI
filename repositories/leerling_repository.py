import sqlite3
from modellen.leerling import Leerling

class LeerlingRepository:
    def __init__(self, database_pad):
        self.database_pad = database_pad

    def _connect(self):
        conn = sqlite3.connect(self.database_pad)
        conn.row_factory = sqlite3.Row   # vooe kolomnamen
        return conn

    def get_all(self):
        conn = self._connect()
        cursor = conn.cursor()

        query = """
        SELECT 
            g.gebruiker_id,
            g.gebruikersnaam,
            g.voornaam,
            g.tussenvoegsels,
            g.achternaam,
            g.email,
            g.wachtwoord,
            l.klas,
            l.leerjaar,
            l.mentor
        FROM Gebruiker g
        JOIN Leerling l ON g.gebruiker_id = l.leerling_id
        """

        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()

        leerlingen = []
        for row in rows:
            leerling = Leerling(
                gebruiker_id=row["gebruiker_id"],
                gebruikersnaam=row["gebruikersnaam"],
                voornaam=row["voornaam"],
                tussenvoegsels=row["tussenvoegsels"],
                achternaam=row["achternaam"],
                email=row["email"],
                wachtwoord=row["wachtwoord"],
                klas=row["klas"],
                leerjaar=row["leerjaar"],
                mentor=row["mentor"]
            )
            leerlingen.append(leerling)

        return leerlingen

    def get_by_id(self, leerling_id):
        conn = self._connect()
        cursor = conn.cursor()

        query = """
        SELECT 
            g.gebruiker_id,
            g.gebruikersnaam,
            g.voornaam,
            g.tussenvoegsels,
            g.achternaam,
            g.email,
            g.wachtwoord,
            l.klas,
            l.leerjaar,
            l.mentor
        FROM Gebruiker g
        JOIN Leerling l ON g.gebruiker_id = l.leerling_id
        WHERE g.gebruiker_id = ?
        """

        cursor.execute(query, (leerling_id,))
        row = cursor.fetchone()
        conn.close()

        if row is None:
            return None

        return Leerling(
            gebruiker_id=row["gebruiker_id"],
            gebruikersnaam=row["gebruikersnaam"],
            voornaam=row["voornaam"],
            tussenvoegsels=row["tussenvoegsels"],
            achternaam=row["achternaam"],
            email=row["email"],
            wachtwoord=row["wachtwoord"],
            klas=row["klas"],
            leerjaar=row["leerjaar"],
            mentor=row["mentor"]
        )
