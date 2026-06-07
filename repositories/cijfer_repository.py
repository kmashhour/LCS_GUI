import sqlite3
from modellen.cijfer import Cijfer

class CijferRepository:
    def __init__(self, db_pad):
        self.db_pad = db_pad

    def _connect(self):
        return sqlite3.connect(self.db_pad)

    # nieuwe cijfer opslaan
    def insert(self, cijfer: Cijfer):
        conn = self._connect()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO Cijfer (leerling_id, onderdeel_id, docent_id, waarde, datum, studiejaar, periode)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            cijfer.leerling_id,
            cijfer.onderdeel_id,
            cijfer.docent_id,
            cijfer.waarde,
            cijfer.datum,
            cijfer.studiejaar,
            cijfer.periode
        ))

        conn.commit()
        nieuw_id = cursor.lastrowid
        conn.close()
        return nieuw_id

    # Cijfer wijzigen
    def update(self, cijfer_id, waarde, datum, studiejaar, periode):
        conn = self._connect()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE Cijfer
            SET waarde = ?, datum = ?, studiejaar = ?, periode = ?
            WHERE cijfer_id = ?
        """, (waarde, datum, studiejaar, periode, cijfer_id))

        conn.commit()
        conn.close()

    # haal éen cijfer op
    def get_by_id(self, cijfer_id):
        conn = self._connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT cijfer_id, leerling_id, onderdeel_id, docent_id, waarde, datum, studiejaar, periode
            FROM Cijfer
            WHERE cijfer_id = ?
        """, (cijfer_id,))

        row = cursor.fetchone()
        conn.close()

        if row:
            return Cijfer(*row)
        return None

    # Ophalen cijfers per leerling
    def get_by_leerling(self, leerling_id):
        conn = self._connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT cijfer_id, leerling_id, onderdeel_id, docent_id, waarde, datum, studiejaar, periode
            FROM Cijfer
            WHERE leerling_id = ?
            ORDER BY datum ASC
        """, (leerling_id,))

        rows = cursor.fetchall()
        conn.close()

        return [Cijfer(*row) for row in rows]

    # Ophalen per studiejaar
    def get_by_studiejaar(self, leerling_id, studiejaar):
        conn = self._connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT cijfer_id, leerling_id, onderdeel_id, docent_id, waarde, datum, studiejaar, periode
            FROM Cijfer
            WHERE leerling_id = ? AND studiejaar = ?
            ORDER BY datum ASC
        """, (leerling_id, studiejaar))

        rows = cursor.fetchall()
        conn.close()

        return [Cijfer(*row) for row in rows]

    # Ophalen per studijaar en periode
    def get_by_studiejaar_en_periode(self, leerling_id, studiejaar, periode):
        conn = self._connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT cijfer_id, leerling_id, onderdeel_id, docent_id, waarde, datum, studiejaar, periode
            FROM Cijfer
            WHERE leerling_id = ? AND studiejaar = ? AND periode = ?
            ORDER BY datum ASC
        """, (leerling_id, studiejaar, periode))

        rows = cursor.fetchall()
        conn.close()

        return [Cijfer(*row) for row in rows]

    # Ophalen per docent
    def get_by_docent(self, docent_id):
        conn = self._connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT cijfer_id, leerling_id, onderdeel_id, docent_id, waarde, datum, studiejaar, periode
            FROM Cijfer
            WHERE docent_id = ?
            ORDER BY datum ASC
        """, (docent_id,))

        rows = cursor.fetchall()
        conn.close()

        return [Cijfer(*row) for row in rows]

    # Ophalen per onderdeel
    def get_by_onderdeel(self, onderdeel_id):
        conn = self._connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT cijfer_id, leerling_id, onderdeel_id, docent_id, waarde, datum, studiejaar, periode
            FROM Cijfer
            WHERE onderdeel_id = ?
            ORDER BY datum ASC
        """, (onderdeel_id,))

        rows = cursor.fetchall()
        conn.close()

        return [Cijfer(*row) for row in rows]
