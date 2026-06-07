import sqlite3
from modellen.docent import Docent

class DocentRepository:
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
        SELECT 
            g.gebruiker_id,
            g.gebruikersnaam,
            g.voornaam,
            g.tussenvoegsels,
            g.achternaam,
            g.email,
            g.wachtwoord,
            d.vakgebied
        FROM Gebruiker g
        JOIN Docent d ON g.gebruiker_id = d.docent_id
        """

        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()

        docenten = []
        for row in rows:
            docent = Docent(
                gebruiker_id=row["gebruiker_id"],
                gebruikersnaam=row["gebruikersnaam"],
                voornaam=row["voornaam"],
                tussenvoegsels=row["tussenvoegsels"],
                achternaam=row["achternaam"],
                email=row["email"],
                wachtwoord=row["wachtwoord"],
                vakgebied=row["vakgebied"]
            )
            docenten.append(docent)

        return docenten

    def get_by_id(self, docent_id):
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
            d.vakgebied
        FROM Gebruiker g
        JOIN Docent d ON g.gebruiker_id = d.docent_id
        WHERE g.gebruiker_id = ?
        """

        cursor.execute(query, (docent_id,))
        row = cursor.fetchone()
        conn.close()

        if row is None:
            return None

        return Docent(
            gebruiker_id=row["gebruiker_id"],
            gebruikersnaam=row["gebruikersnaam"],
            voornaam=row["voornaam"],
            tussenvoegsels=row["tussenvoegsels"],
            achternaam=row["achternaam"],
            email=row["email"],
            wachtwoord=row["wachtwoord"],
            vakgebied=row["vakgebied"]
        )
