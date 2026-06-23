import sqlite3
from config import DATABASE_PAD

from modellen.cijfer import Cijfer
from repositories.leerling_repository import LeerlingRepository
from repositories.onderdeel_repository import OnderdeelRepository
from repositories.docent_repository import DocentRepository
from repositories.studiejaar_repository import StudiejaarRepository
from repositories.periode_repository import PeriodeRepository


class CijferRepository:
    def __init__(self, database_pad=DATABASE_PAD):
        self.database_pad = database_pad

        # Repositorys voor het bouwen objecten
        self.leerling_repo = LeerlingRepository(database_pad)
        self.onderdeel_repo = OnderdeelRepository(database_pad)
        self.docent_repo = DocentRepository(database_pad)
        self.studiejaar_repo = StudiejaarRepository(database_pad)
        self.periode_repo = PeriodeRepository(database_pad)

    def _connect(self):
        conn = sqlite3.connect(self.database_pad)
        conn.row_factory = sqlite3.Row
        return conn


    # Helper cijfer bouw
    def _build_cijfer(self, row):
        leerling = self.leerling_repo.get_by_id(row["leerling_id"])
        onderdeel = self.onderdeel_repo.get_by_id(row["onderdeel_id"])
        docent = self.docent_repo.get_by_id(row["docent_id"])
        studiejaar = self.studiejaar_repo.get_by_id(row["studiejaar"])
        periode = self.periode_repo.get_by_id(row["periode"])

        cijfer = Cijfer(
            cijfer_id=row["cijfer_id"],
            leerling=leerling,
            onderdeel=onderdeel,
            docent=docent,
            waarde=row["waarde"],
            datum=row["datum"]
        )

        # kopelingen
        cijfer.studiejaar = studiejaar
        cijfer.periode = periode

        return cijfer

    # crud
    def insert(self, cijfer: Cijfer):
        conn = self._connect()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO Cijfer (leerling_id, onderdeel_id, docent_id, waarde, datum, studiejaar, periode)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            cijfer.leerling.gebruiker_id,
            cijfer.onderdeel.onderdeel_id,
            cijfer.docent.gebruiker_id,
            cijfer.waarde,
            cijfer.datum,
            cijfer.studiejaar.studiejaar_id,
            cijfer.periode.periode_id
        ))

        conn.commit()
        nieuw_id = cursor.lastrowid
        conn.close()
        return nieuw_id

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

    #select querys
    def get_by_id(self, cijfer_id):
        conn = self._connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM Cijfer
            WHERE cijfer_id = ?
        """, (cijfer_id,))

        row = cursor.fetchone()
        conn.close()

        return self._build_cijfer(row) if row else None

    def get_by_leerling(self, leerling_id):
        conn = self._connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM Cijfer
            WHERE leerling_id = ?
            ORDER BY datum ASC
        """, (leerling_id,))

        rows = cursor.fetchall()
        conn.close()

        return [self._build_cijfer(r) for r in rows]

    def get_by_studiejaar(self, leerling_id, studiejaar_id):
        conn = self._connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM Cijfer
            WHERE leerling_id = ? AND studiejaar = ?
            ORDER BY datum ASC
        """, (leerling_id, studiejaar_id))

        rows = cursor.fetchall()
        conn.close()

        return [self._build_cijfer(r) for r in rows]

    def get_by_studiejaar_en_periode(self, leerling_id, studiejaar_id, periode_id):
        conn = self._connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM Cijfer
            WHERE leerling_id = ? AND studiejaar = ? AND periode = ?
            ORDER BY datum ASC
        """, (leerling_id, studiejaar_id, periode_id))

        rows = cursor.fetchall()
        conn.close()

        return [self._build_cijfer(r) for r in rows]
