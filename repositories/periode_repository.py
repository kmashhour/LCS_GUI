import sqlite3
from config import DATABASE_PAD
from modellen.periode import Periode

class PeriodeRepository:
    def __init__(self, database_pad=DATABASE_PAD):
        self.database_pad = database_pad

    def _connect(self):
        conn = sqlite3.connect(self.database_pad)
        conn.row_factory = sqlite3.Row
        return conn

    # Haal alle perioden op
    def get_all(self):
        conn = self._connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT periode_id, studiejaar_id, periode_nummer, startdatum, einddatum
            FROM Periode
            ORDER BY studiejaar_id ASC, periode_nummer ASC
        """)

        rows = cursor.fetchall()
        conn.close()

        return [
            Periode(
                periode_id=row[0],
                studiejaar_id=row[1],
                periode_nummer=row[2],
                startdatum=row[3],
                einddatum=row[4]
            )
            for row in rows
        ]
    # periode bij id
    def get_by_id(self, periode_id):
        conn = self._connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM Periode
            WHERE periode_id = ?
        """, (periode_id,))

        row = cursor.fetchone()
        conn.close()

        if row is None:
         return None

        return Periode(
            periode_id=row["periode_id"],
            studiejaar_id=row["studiejaar_id"],
            periode_nummer=row["periode_nummer"],
            startdatum=row["startdatum"],
            einddatum=row["einddatum"]
        )
    
    # Haal periodes van een studiejaar
    def get_by_studiejaar(self, studiejaar_id):
        conn = self._connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT periode_id, studiejaar_id, periode_nummer, startdatum, einddatum
            FROM Periode
            WHERE studiejaar_id = ?
            ORDER BY periode_nummer ASC
        """, (studiejaar_id,))

        rows = cursor.fetchall()
        conn.close()

        return [
            Periode(
                periode_id=row[0],
                studiejaar_id=row[1],
                periode_nummer=row[2],
                startdatum=row[3],
                einddatum=row[4]
            )
            for row in rows
        ]

    # Bepalen periode obv datum
    def get_periode_for_date(self, datum):
        """
        datum: string 'yyyy-mm-dd'
        """
        conn = self._connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT periode_id, studiejaar_id, periode_nummer, startdatum, einddatum
            FROM Periode
            WHERE startdatum <= ? AND einddatum >= ?
        """, (datum, datum))

        row = cursor.fetchone()
        conn.close()

        if row:
            return Periode(
                periode_id=row[0],
                studiejaar_id=row[1],
                periode_nummer=row[2],
                startdatum=row[3],
                einddatum=row[4]
            )
        return None
