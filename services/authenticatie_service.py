from repositories.gebruiker_repository import GebruikerRepository

class AuthenticatieService:
    def __init__(self):
        self.repo = GebruikerRepository()

    def login(self, gebruikersnaam, wachtwoord_plain):
        gebruiker = self.repo.get_by_gebruikersnaam(gebruikersnaam)
        if gebruiker is None:
            return None

        # gebruik ingebouwde methode van model
        if not gebruiker.verify_wachtwoord(wachtwoord_plain):
            return None

        return gebruiker

    def wijzig_wachtwoord(self, gebruiker_id, oud_wachtwoord, nieuw_wachtwoord):
        gebruiker = self.repo.get_by_id(gebruiker_id)
        if gebruiker is None:
            return False, "Gebruiker bestaat niet"

        #controleer oud wachtwoord via model
        if not gebruiker.verify_wachtwoord(oud_wachtwoord):
            return False, "Oud wachtwoord is onjuist"

        # model maakt zelf een nieuwe hash
        nieuw_hash = gebruiker._hash_wachtwoord(nieuw_wachtwoord)

        # opslaan in database
        self.repo.update_wachtwoord(gebruiker_id, nieuw_hash)

        return True, "Wachtwoord succesvol gewijzigd"
