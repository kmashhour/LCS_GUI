import sqlite3
from modellen.onderdeel import Onderdeel

class OnderdeelRepository:
    def __init__(self, database_pad):
        self.database_pad = database_pad

    def _connect(self):
        conn = sqlite3.connect(self.database_pad)
        conn.row_factory = sqlite3.Row
        return conn

    def get_all(self):
        conn = self._connect()
        cursor = conn.cursor()

        query = "SELECT * FROM Onderdeel"

        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()

        onderdelen = []
        for row in rows:
            onderdeel = Onderdeel(
                onderdeel_id=row["onderdeel_id"],
                naam=row["naam"],
                weging=row["weging"],
                type=row["type"]
            )
            onderdelen.append(onderdeel)

        return onderdelen

    def get_by_id(self, onderdeel_id):
        conn = self._connect()
        cursor = conn.cursor()

        query = "SELECT * FROM Onderdeel WHERE onderdeel_id = ?"

        cursor.execute(query, (onderdeel_id,))
        row = cursor.fetchone()
        conn.close()

        if row is None:
            return None

        return Onderdeel(
            onderdeel_id=row["onderdeel_id"],
            naam=row["naam"],
            weging=row["weging"],
            type=row["type"]
        )
