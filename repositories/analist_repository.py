import sqlite3
from modellen.analist import Analist

class AnalistRepository:
    def __init__(self, database_pad):
        self.database_pad = database_pad

    def _connect(self):
        conn = sqlite3.connect(self.database_pad)
        conn.row_factory = sqlite3.Row   # kolomnamen
        return conn

    def get_all(self):
        conn = self._connect()
        cursor = conn.cursor()

        query = """
        SELECT *
        FROM Gebruiker
        WHERE rol = 'analist'
        """

        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()

        analisten = []
        for row in rows:
            analist = Analist(
                gebruiker_id=row["gebruiker_id"],
                gebruikersnaam=row["gebruikersnaam"],
                voornaam=row["voornaam"],
                tussenvoegsels=row["tussenvoegsels"],
                achternaam=row["achternaam"],
                email=row["email"],
                wachtwoord=row["wachtwoord"]
            )
            analisten.append(analist)

        return analisten

    def get_by_id(self, analist_id):
        conn = self._connect()
        cursor = conn.cursor()

        query = """
        SELECT *
        FROM Gebruiker
        WHERE gebruiker_id = ? AND rol = 'analist'
        """

        cursor.execute(query, (analist_id,))
        row = cursor.fetchone()
        conn.close()

        if row is None:
            return None

        return Analist(
            gebruiker_id=row["gebruiker_id"],
            gebruikersnaam=row["gebruikersnaam"],
            voornaam=row["voornaam"],
            tussenvoegsels=row["tussenvoegsels"],
            achternaam=row["achternaam"],
            email=row["email"],
            wachtwoord=row["wachtwoord"]
        )
