LCS GUI - Leerling Cijfer Systeem
Een desktopapplicatie gebouwd in Python 3.13.3 met PySide6, ontworpen voor leerlingen om cijfers, periodes en studievoortgang te bekijken.
De applicatie gebruikt SQLite als lokale database en volgt een duidelijke MVC‑achtige structuur met services, views en UI‑bestanden.
Functionaliteiten
Login‑systeem met rollen (leerling)

Leerling‑dashboard met:

Overzicht van vakken

Periodes

Cijfers

Automatische berekening van eindcijfers

SQLite‑database voor opslag van gebruikers en cijfers

PySide6 GUI met .ui‑bestanden (Qt Designer)

Duidelijke projectstructuur:
data/
views/
services/
modellen/
repositories/
ui/

Installatie
1. Python‑versie
Dit project gebruikt:
Python 3.13.3
Deze versie is gekozen vanwege PySide6‑compatibiliteit.

2. Virtuele omgeving aanmaken
python -m venv venv
Activeren:
Windows:
venv\Scripts\activate

3. Dependencies installeren
pip install -r requirements.txt

4. Database
Het project gebruikt SQLite.

De database bevindt zich in:
/database/lcs.db

5. Applicatie starten
Start de GUI via:
python main.py