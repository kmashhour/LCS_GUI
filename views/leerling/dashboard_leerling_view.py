from PySide6.QtWidgets import QWidget, QTableWidgetItem, QTableWidget, QMessageBox
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, Qt
from datetime import datetime
from services.cijfer_manager import CijferManager
from services.authenticatie_service import AuthenticatieService

class DashboardLeerlingView(QWidget):
    def __init__(self, gebruiker):
        super().__init__()

        self.auth_service = AuthenticatieService()
        
        # UI laden
        ui_file = QFile("ui/dashboard_leerling.ui")
        ui_file.open(QFile.ReadOnly)

        loader = QUiLoader()
        self.ui = loader.load(ui_file, self)
        ui_file.close()

        # Data
        self.gebruiker = gebruiker   #leerling object
        self.cijfer_manager = CijferManager()

        # Navigatie
        self.ui.btn_dashboard.clicked.connect(
            lambda: self.ui.stacked_paginas.setCurrentIndex(0)
        )
        self.ui.btn_mijn_cijfers.clicked.connect(
            lambda: self.ui.stacked_paginas.setCurrentIndex(1)
        )
        self.ui.btn_account.clicked.connect(
            lambda: self.ui.stacked_paginas.setCurrentIndex(2)
        )
        self.ui.btn_uitloggen.clicked.connect(self.logout)
        self.ui.btn_wachtwoord_wijzigen.clicked.connect(self.wijzig_wachtwoord)

        # paginas vullen
        self.vul_dashboard()
        self.vul_mijn_cijfers()
        self.vul_account()

        # startpagina = dashboard
        self.ui.stacked_paginas.setCurrentIndex(0)

    # pagina 0 is = dashboard
    def vul_dashboard(self):
        # Studiejaar + laatste periode ophalen via CijferManager
        studiejaar = self.cijfer_manager.get_huidig_studiejaar(self.gebruiker.gebruiker_id)
        periode = self.cijfer_manager.get_laatste_periode(self.gebruiker.gebruiker_id)

        # Labels vullen
        if studiejaar:
            self.ui.lbl_dashboard_studiejaar.setText(f"Studiejaar: {studiejaar.naam}")
        else:
            self.ui.lbl_dashboard_studiejaar.setText("Studiejaar: onbekend")

        if periode:
            self.ui.lbl_dashboard_periode.setText(f"Periode: {periode.periode_nummer}")
        else:
            self.ui.lbl_dashboard_periode.setText("Periode: onbekend")

        # cijfers ophalen voor deze periode
        if periode and studiejaar:
            cijfers = self.cijfer_manager.get_cijfers_per_leerling_per_periode(
                leerling_id=self.gebruiker.gebruiker_id,
                periode_obj=periode
            )
        else:
            cijfers = []

        # KPIs
        po_gem = self.cijfer_manager.bereken_po_gemiddelde(cijfers)
        toets = self.cijfer_manager.get_toets_cijfer(cijfers)
        eind = self.cijfer_manager.bereken_eindcijfer(cijfers)
        po_aantal = self.cijfer_manager.tel_po_onderdelen(cijfers)

        self.ui.lbl_po_gemiddelde_waarde.setText(
            "-" if po_gem is None else f"{po_gem:.1f}"
        )
        self.ui.lbl_toets_waarde.setText(
            "-" if toets is None else f"{toets:.1f}"
        )
        self.ui.lbl_eindcijfer_waarde.setText(
            "-" if eind is None else f"{eind:.1f}"
        )
        self.ui.lbl_po_aantal_waarde.setText(str(po_aantal))

        # tabel vullen
        self.vul_dashboard_tabel(cijfers)
        #print("DEBUG leerling_id =", self.gebruiker.gebruiker_id)
        #print("DEBUG periode_id =", periode.periode_id if periode else None)
        #print("DEBUG aantal cijfers =", len(cijfers))

    def vul_dashboard_tabel(self, cijfers):
        tabel = self.ui.tabel_dashboard_cijfers
        tabel.setRowCount(len(cijfers))

        tabel.setEditTriggers(QTableWidget.NoEditTriggers)
        tabel.verticalHeader().setVisible(False)
        tabel.horizontalHeader().setDefaultAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        tabel.setColumnWidth(4, 200)

        for rij, cijfer in enumerate(cijfers):
            datum_nl = datetime.strptime(cijfer.datum, "%Y-%m-%d").strftime("%d-%m-%Y")
            tabel.setItem(rij, 0, QTableWidgetItem(cijfer.onderdeel.naam))
            tabel.setItem(rij, 1, QTableWidgetItem(f"{cijfer.get_decimaal():.1f}"))
            tabel.setItem(rij, 2, QTableWidgetItem(str(cijfer.onderdeel.weging)))
            tabel.setItem(rij, 3, QTableWidgetItem(datum_nl))
            tabel.setItem(rij, 4, QTableWidgetItem(cijfer.docent.volledige_naam()))

    # pagina 1 = mijn cijfers
    def vul_mijn_cijfers(self):
        self.vul_mijn_cijfers_studiejaren()
        self.vul_mijn_cijfers_periodes()
        self.vul_mijn_cijfers_tabel()
        self.vul_mijn_cijfers_waarschuwingen()

    def vul_mijn_cijfers_studiejaren(self):
        self.ui.cmb_mijncijfers_studiejaar.clear()

        alle_sj = self.cijfer_manager.periode_service.studiejaar_repo.get_all()
        for sj in alle_sj:
            self.ui.cmb_mijncijfers_studiejaar.addItem(sj.naam, sj.studiejaar_id)

        self.ui.cmb_mijncijfers_studiejaar.currentIndexChanged.connect(
            self._on_studiejaar_gewijzigd
        )

    def _on_studiejaar_gewijzigd(self, index):
        self.vul_mijn_cijfers_periodes()
        self.vul_mijn_cijfers_tabel()
        self.vul_mijn_cijfers_waarschuwingen()

    def vul_mijn_cijfers_periodes(self):
        self.ui.cmb_mijncijfers_periode.clear()

        studiejaar_id = self.ui.cmb_mijncijfers_studiejaar.currentData()
        if studiejaar_id is None:
            return

        periodes = self.cijfer_manager.periode_service.periode_repo.get_by_studiejaar(studiejaar_id)
        for p in periodes:
            self.ui.cmb_mijncijfers_periode.addItem(f"Periode {p.periode_nummer}", p)

        self.ui.cmb_mijncijfers_periode.currentIndexChanged.connect(
            self._on_periode_gewijzigd
        )

    def _on_periode_gewijzigd(self, index):
        self.vul_mijn_cijfers_tabel()
        self.vul_mijn_cijfers_waarschuwingen()

    def vul_mijn_cijfers_tabel(self):
        periode_obj = self.ui.cmb_mijncijfers_periode.currentData()
        if periode_obj is None:
            self.ui.tabel_mijn_cijfers.setRowCount(0)
            return

        cijfers = self.cijfer_manager.get_cijfers_per_leerling_per_periode(
            leerling_id=self.gebruiker.gebruiker_id,
            periode_obj=periode_obj
        )

        tabel = self.ui.tabel_mijn_cijfers
        tabel.setRowCount(len(cijfers))

        tabel.setEditTriggers(QTableWidget.NoEditTriggers)
        tabel.verticalHeader().setVisible(False)
        tabel.horizontalHeader().setDefaultAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        tabel.setColumnWidth(4, 200)

        for rij, cijfer in enumerate(cijfers):
            datum_nl = datetime.strptime(cijfer.datum, "%Y-%m-%d").strftime("%d-%m-%Y")
            tabel.setItem(rij, 0, QTableWidgetItem(cijfer.onderdeel.naam))
            tabel.setItem(rij, 1, QTableWidgetItem(f"{cijfer.get_decimaal():.1f}"))
            tabel.setItem(rij, 2, QTableWidgetItem(str(cijfer.onderdeel.weging)))
            tabel.setItem(rij, 3, QTableWidgetItem(datum_nl))
            tabel.setItem(rij, 4, QTableWidgetItem(cijfer.docent.volledige_naam()))

    def vul_mijn_cijfers_waarschuwingen(self):
        periode_obj = self.ui.cmb_mijncijfers_periode.currentData()
        if periode_obj is None:
            self.ui.lbl_waarschuwing_po.setVisible(False)
            self.ui.lbl_waarschuwing_toets.setVisible(False)
            return

        cijfers = self.cijfer_manager.get_cijfers_per_leerling_per_periode(
            leerling_id=self.gebruiker.gebruiker_id,
            periode_obj=periode_obj
        )

        po_gem = self.cijfer_manager.bereken_po_gemiddelde(cijfers)
        toets = self.cijfer_manager.get_toets_cijfer(cijfers)

        self.ui.lbl_waarschuwing_po.setVisible(po_gem is not None and po_gem < 5.5)
        self.ui.lbl_waarschuwing_toets.setVisible(toets is None)

    #pagina 2 = account instellingen
    def vul_account(self):
        self.ui.lbl_account_gebruiker_waarde.setText(self.gebruiker.gebruikersnaam)
        self.ui.lbl_account_email_waarde.setText(self.gebruiker.email)

    #wachtwoord wijzigen
    def wijzig_wachtwoord(self):
        oud = self.ui.txt_oud_wachtwoord.text().strip()
        nieuw = self.ui.txt_nieuw_wachtwoord.text().strip()
        herhaal = self.ui.txt_nieuw_wachtwoord_herhaal.text().strip()

        if not oud or not nieuw or not herhaal:
            self.ui.lbl_wachtwoord_melding.setText("Vul alle velden in.")
            return

        if nieuw != herhaal:
            self.ui.lbl_wachtwoord_melding.setText("Nieuwe wachtwoorden zijn niet gelijk.")
            return

        if len(nieuw) < 7:
            self.ui.lbl_wachtwoord_melding.setText("Nieuw wachtwoord moet minimaal 7 tekens zijn.")
            return

        succes, melding = self.auth_service.wijzig_wachtwoord(
            gebruiker_id=self.gebruiker.gebruiker_id,
            oud_wachtwoord=oud,
            nieuw_wachtwoord=nieuw
        )

        self.ui.lbl_wachtwoord_melding.setText(melding)

        if succes:
            self.ui.txt_oud_wachtwoord.clear()
            self.ui.txt_nieuw_wachtwoord.clear()
            self.ui.txt_nieuw_wachtwoord_herhaal.clear()

    # afmelden
    def logout(self):
        from views.login_view import LoginView
        self.login = LoginView()
        self.login.show()
        self.close()
