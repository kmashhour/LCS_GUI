import sqlite3
import hashlib
import os
from config import DATABASE_PAD


def hash_wachtwoord(wachtwoord):
    """Hash wachtwoord met SHA256 + salt (zelfde als in Gebruiker-model)."""
    salt = os.urandom(16)
    hash_value = hashlib.pbkdf2_hmac(
        "sha256",
        wachtwoord.encode("utf-8"),
        salt,
        100000
    )
    return salt.hex() + ":" + hash_value.hex()


def main():
    print("🔄 Verbinden met database:", DATABASE_PAD)
    conn = sqlite3.connect(DATABASE_PAD)
    cursor = conn.cursor()

    # Zoek alle gebruikers met wachtwoord 'test123'
    cursor.execute("""
        SELECT gebruiker_id, gebruikersnaam
        FROM Gebruiker
        WHERE wachtwoord = 'test123'
    """)

    rows = cursor.fetchall()

    if not rows:
        print("✔ Geen gebruikers gevonden met wachtwoord 'test123'.")
        conn.close()
        return

    print(f"🔍 {len(rows)} gebruikers gevonden met wachtwoord 'test123'.")

    # Hash genereren
    hashed = hash_wachtwoord("test123")

    # Update uitvoeren
    cursor.execute("""
        UPDATE Gebruiker
        SET wachtwoord = ?
        WHERE wachtwoord = 'test123'
    """, (hashed,))

    conn.commit()
    conn.close()

    print("✔ Alle wachtwoorden succesvol gehasht!")
    print("ℹ Nieuwe hash:", hashed)
    print("⚠ Let op: alle gebruikers met 'test123' hebben nu DEZELFDE hash.")


if __name__ == "__main__":
    main()
