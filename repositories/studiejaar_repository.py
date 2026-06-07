import sqlite3
from datetime import datetime
from modellen.studiejaar import Studiejaar

class StudiejaarRepository:
    def __init__(self, db_pad):
        self.db_pad = db_pad

    def _connect(self):
        return sqlite3.connect(self.db_pad)

    # Haal alle studijaren
    def get_all(self):
        conn = self._connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT studiejaar_id, naam, startdatum, einddatum
            FROM Studiejaar
            ORDER BY startdatum ASC
        """)

        rows = cursor.fetchall()
        conn.close()

        return [
            Studiejaar(
                studiejaar_id=row[0],
                naam=row[1],
                startdatum=row[2],
                einddatum=row[3]
            )
            for row in rows
        ]

    # Haal een studiejaar op basis van ID
    def get_by_id(self, studiejaar_id):
        conn = self._connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT studiejaar_id, naam, startdatum, einddatum
            FROM Studiejaar
            WHERE studiejaar_id = ?
        """, (studiejaar_id,))

        row = cursor.fetchone()
        conn.close()

        if row:
            return Studiejaar(
                studiejaar_id=row[0],
                naam=row[1],
                startdatum=row[2],
                einddatum=row[3]
            )
        return None

    # Bepalen studiejaar obv datum
    def get_studiejaar_for_date(self, datum):
        """
        datum: string 'yyyy-mm-dd'
        """
        conn = self._connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT studiejaar_id, naam, startdatum, einddatum
            FROM Studiejaar
            WHERE startdatum <= ? AND einddatum >= ?
        """, (datum, datum))

        row = cursor.fetchone()
        conn.close()

        if row:
            return Studiejaar(
                studiejaar_id=row[0],
                naam=row[1],
                startdatum=row[2],
                einddatum=row[3]
            )
        return None
