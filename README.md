Leerlingen cijfer systeem Vakgroep Informatica
Dit project is ontwikkeld voor de vakgroep Informatica en ondersteunt het beheren, registreren en analyseren van cijfers voor leerlingen. Cijfers worden gekoppeld aan PO‑onderdelen, toetsen, periodes en studiejaren. Het systeem is ontworpen om overzichtelijk, betrouwbaar en uitbreidbaar te zijn.

Functionaliteit
Leerlingen kunnen hun eigen cijfers bekijken per periode, PO‑onderdeel en toets.

Docenten kunnen cijfers invoeren, wijzigen en bekijken.

Analisten kunnen overzichten en rapportages genereren.

Het systeem bepaalt automatisch bij welke periode een datum hoort.

Ondersteuning voor studiejaar en periode‑beheer.

Gelaagde architectuur: Presentation → Services → Repository → Domain.

Projectstructuur
/modellen        # Domeinobjecten (Leerling, Docent, Cijfer, Onderdeel, Periode, Studiejaar)
 /services       # Logica (CijferManager, PeriodeService)
 /repositories   # Databasecommunicatie (SQLite)
 main.py         # Startpunt van de applicatie
 requirements.txt
 README.md

Database
Het project gebruikt SQLite.
De repositories lezen en schrijven direct naar de database via SQL‑queries.

1. Installatie
Maak een virtual environment:

python -m venv venv
2. Activeer de venv:

Windows:
venv\Scripts\activate
Mac/Linux:
source venv/bin/activate

3. Installeer dependencies:

pip install -r requirements.txt
(requirements.txt is leeg omdat het project geen externe libraries gebruikt)

Starten
python main.py

Rollen
Leerling: cijfers bekijken
Docent: cijfers invoeren en beheren
Analist: rapportages en overzichten
