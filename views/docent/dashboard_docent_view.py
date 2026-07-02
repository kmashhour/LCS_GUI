from PySide6.QtCore import QFile, Qt
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QWidget, QTableWidgetItem, QTableWidget

from services.cijfer_manager import CijferManager
from services.authenticatie_service import AuthenticatieService


class DashboardDocentView(QWidget):
    def __init__(self, gebruiker):
        super().__init__()

        self.gebruiker = gebruiker
        self.cijfer_manager = CijferManager()
        self.auth_service = AuthenticatieService()

        loader = QUiLoader()
        ui_file = QFile("ui/dashboard_docent.ui")
        ui_file.open(QFile.OpenModeFlag.ReadOnly)
        self.ui = loader.load(ui_file, self)
        ui_file.close()

        self.ui.btn_dashboard.clicked.connect(self.toon_dashboard)
        self.ui.btn_cijferoverzicht.clicked.connect(self.toon_cijferoverzicht)
        self.ui.btn_cijfer_invoeren.clicked.connect(self.toon_cijfer_invoeren)
        self.ui.btn_account.clicked.connect(self.toon_account)
        self.ui.btn_uitloggen.clicked.connect(self.close)

        self.toon_accountgegevens()
        self.toon_dashboard()
        self.vul_dashboard()

    def toon_dashboard(self):
        self.ui.stacked_paginas.setCurrentWidget(self.ui.pagina_dashboard)

    def toon_cijferoverzicht(self):
        self.ui.stacked_paginas.setCurrentWidget(self.ui.pagina_cijferoverzicht)

    def toon_cijfer_invoeren(self):
        self.ui.stacked_paginas.setCurrentWidget(self.ui.pagina_cijfer_invoeren)

    def toon_account(self):
        self.ui.stacked_paginas.setCurrentWidget(self.ui.pagina_account)

    def toon_accountgegevens(self):
        self.ui.lbl_gebruiker_rol.setText("Docent")

        if hasattr(self.gebruiker, "gebruikersnaam"):
            self.ui.lbl_account_gebruiker_waarde.setText(self.gebruiker.gebruikersnaam)

        if hasattr(self.gebruiker, "email"):
            self.ui.lbl_account_email_waarde.setText(self.gebruiker.email)

    def vul_dashboard(self):
        studiejaar = self.cijfer_manager.get_huidig_studiejaar(self.gebruiker.gebruiker_id)
        periode = self.cijfer_manager.get_laatste_periode(self.gebruiker.gebruiker_id)

        if studiejaar:
            self.ui.lbl_dashboard_studiejaar.setText(f"Studiejaar: {studiejaar.naam}")
        else:
            self.ui.lbl_dashboard_studiejaar.setText("Studiejaar: onbekend")

        if periode:
            self.ui.lbl_dashboard_periode.setText(f"Periode: {periode.periode_nummer}")
        else:
            self.ui.lbl_dashboard_periode.setText("Periode: onbekend")

        klas = "4hinf1" #harde code om te testen

        self.ui.lbl_dashboard_klas.setText(f"Klas: {klas}")

        if periode is None:
            overzicht = []
        else:
            overzicht = self.cijfer_manager.get_docent_dashboard_overzicht(
                docent_id=self.gebruiker.gebruiker_id,
                klas=klas,
                periode_obj=periode
            )

        self.vul_dashboard_kpis(overzicht)
        self.vul_dashboard_tabel(overzicht)

        print("DEBUG docent_id =", self.gebruiker.gebruiker_id)
        print("DEBUG klas =", klas)
        print("DEBUG studiejaar_id =", periode.studiejaar_id if periode else None)
        print("DEBUG periode_id =", periode.periode_id if periode else None)
        print("DEBUG aantal leerlingen in overzicht =", len(overzicht))
        print("DEBUG overzicht =", overzicht)

    def vul_dashboard_kpis(self, overzicht):
        eindcijfers = [
            item["eindcijfer"]
            for item in overzicht
            if item["eindcijfer"] is not None
        ]

        aantal_leerlingen = len(overzicht)

        if eindcijfers:
            klas_gemiddelde = sum(eindcijfers) / len(eindcijfers)
            hoogste = max(eindcijfers)
            laagste = min(eindcijfers)
        else:
            klas_gemiddelde = None
            hoogste = None
            laagste = None

        self.ui.lbl_klas_gemiddelde_waarde.setText(
            "-" if klas_gemiddelde is None else f"{klas_gemiddelde:.1f}"
        )
        self.ui.lbl_hoogste_eindcijfer_waarde.setText(
            "-" if hoogste is None else f"{hoogste:.1f}"
        )
        self.ui.lbl_laagste_eindcijfer_waarde.setText(
            "-" if laagste is None else f"{laagste:.1f}"
        )
        self.ui.lbl_aantal_leerlingen_waarde.setText(str(aantal_leerlingen))

    def vul_dashboard_tabel(self, overzicht):
        tabel = self.ui.tabel_dashboard_cijfers
        tabel.setRowCount(len(overzicht))

        tabel.setEditTriggers(QTableWidget.NoEditTriggers)
        tabel.verticalHeader().setVisible(False)
        tabel.horizontalHeader().setDefaultAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        for rij, item in enumerate(overzicht):
            leerling = item["leerling"]

            naam = leerling.volledige_naam()
            po = item["po_gemiddelde"]
            toets = item["toets"]
            eind = item["eindcijfer"]
            aantal = item["aantal_cijfers"]

            tabel.setItem(rij, 0, QTableWidgetItem(naam))
            tabel.setItem(rij, 1, QTableWidgetItem("-" if po is None else f"{po:.1f}"))
            tabel.setItem(rij, 2, QTableWidgetItem("-" if toets is None else f"{toets:.1f}"))
            tabel.setItem(rij, 3, QTableWidgetItem("-" if eind is None else f"{eind:.1f}"))
            tabel.setItem(rij, 4, QTableWidgetItem(str(aantal)))        