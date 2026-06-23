import sqlite3
from config import DATABASE_PAD
from modellen.gebruiker import Gebruiker
from modellen.leerling import Leerling
from modellen.docent import Docent

class GebruikerRepository:
    def __init__(self, database_pad=DATABASE_PAD):
        self.database_pad = database_pad

    def _connect(self):
        conn = sqlite3.connect(self.database_pad)
        conn.row_factory = sqlite3.Row
        return conn

    #alle gebruikers ophalen 
    def get_all(self):
        conn = self._connect()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Gebruiker")
        rows = cursor.fetchall()
        conn.close()

        gebruikers = []
        for row in rows:
            gebruikers.append(
                Gebruiker(
                    gebruiker_id=row["gebruiker_id"],
                    gebruikersnaam=row["gebruikersnaam"],
                    voornaam=row["voornaam"],
                    tussenvoegsels=row["tussenvoegsels"],
                    achternaam=row["achternaam"],
                    email=row["email"],
                    wachtwoord=row["wachtwoord"],
                    rol=row["rol"],
                    wachtwoord_is_gehasht=True
                )
            )
        return gebruikers

    #ophalen via id hier maak ik subklasen
    def get_by_id(self, gebruiker_id):
        conn = self._connect()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Gebruiker WHERE gebruiker_id = ?", (gebruiker_id,))
        row = cursor.fetchone()
        conn.close()

        if row is None:
            return None

        rol = row["rol"]

        # leerling
        if rol == "leerling":
            from repositories.leerling_repository import LeerlingRepository
            return LeerlingRepository().get_by_id(gebruiker_id)

        #docent
        if rol == "docent":
            from repositories.docent_repository import DocentRepository
            return DocentRepository().get_by_id(gebruiker_id)

        # andere rollen zoals analist of later admin
        return Gebruiker(
            gebruiker_id=row["gebruiker_id"],
            gebruikersnaam=row["gebruikersnaam"],
            voornaam=row["voornaam"],
            tussenvoegsels=row["tussenvoegsels"],
            achternaam=row["achternaam"],
            email=row["email"],
            wachtwoord=row["wachtwoord"],
            rol=row["rol"],
            wachtwoord_is_gehasht=True
        )

    # ophalen via gebruikersnaam voor login
    def get_by_gebruikersnaam(self, gebruikersnaam):
        conn = self._connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM Gebruiker
            WHERE gebruikersnaam = ?
        """, (gebruikersnaam,))

        row = cursor.fetchone()
        conn.close()

        if row is None:
            return None

        rol = row["rol"]

        # leerling
        if rol == "leerling":
            from repositories.leerling_repository import LeerlingRepository
            return LeerlingRepository().get_by_id(row["gebruiker_id"])

        # docent
        if rol == "docent":
            from repositories.docent_repository import DocentRepository
            return DocentRepository().get_by_id(row["gebruiker_id"])

        #ander rollen
        return Gebruiker(
            gebruiker_id=row["gebruiker_id"],
            gebruikersnaam=row["gebruikersnaam"],
            voornaam=row["voornaam"],
            tussenvoegsels=row["tussenvoegsels"],
            achternaam=row["achternaam"],
            email=row["email"],
            wachtwoord=row["wachtwoord"],   # HASH uit database
            rol=row["rol"],
            wachtwoord_is_gehasht=True      # BELANGRIJK
        )
    
    def update_wachtwoord(self, gebruiker_id, nieuw_hash):
        conn = self._connect()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE Gebruiker
            SET wachtwoord = ?
            WHERE gebruiker_id = ?
        """, (nieuw_hash, gebruiker_id))
        conn.commit()
        conn.close()

