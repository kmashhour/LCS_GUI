from PySide6.QtCore import QFile, Qt, QDate, QTimer
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QWidget, QTableWidgetItem, QTableWidget
from datetime import datetime

from services.cijfer_manager import CijferManager
from services.authenticatie_service import AuthenticatieService
from repositories.leerling_repository import LeerlingRepository
from repositories.onderdeel_repository import OnderdeelRepository

class DashboardDocentView(QWidget):
    def __init__(self, gebruiker):
        super().__init__()

        self.gebruiker = gebruiker
        self.cijfer_manager = CijferManager()
        self.auth_service = AuthenticatieService()
        self.leerling_repo = LeerlingRepository()
        self.onderdeel_repo = OnderdeelRepository()

        self.dashboard_studiejaar = None
        self.dashboard_periode = None
        self.dashboard_klas = None

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
        self.ui.btn_wachtwoord_wijzigen.clicked.connect(self.wijzig_wachtwoord)
        self.ui.tabel_dashboard_cijfers.cellDoubleClicked.connect(
            self.open_cijferoverzicht_van_dashboard
        )
        self.ui.btn_cijfer_opslaan.clicked.connect(self.sla_cijfer_op)

        self.toon_accountgegevens()
        self.vul_dashboard()
        self.vul_cijferoverzicht()
        self.vul_cijfer_invoer()

        self.toon_dashboard()

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
        self.ui.lbl_account_gebruiker_waarde.setText(self.gebruiker.gebruikersnaam)
        self.ui.lbl_account_email_waarde.setText(self.gebruiker.email)

    def vul_dashboard(self):
        studiejaar = self.cijfer_manager.get_huidig_studiejaar(self.gebruiker.gebruiker_id)
        periode = self.cijfer_manager.get_laatste_periode(self.gebruiker.gebruiker_id)
        klas = self.cijfer_manager.get_laatste_klas_van_docent(self.gebruiker.gebruiker_id)

        self.dashboard_studiejaar = studiejaar
        self.dashboard_periode = periode
        self.dashboard_klas = klas

        self.ui.lbl_dashboard_studiejaar.setText(
            f"Studiejaar: {studiejaar.naam}" if studiejaar else "Studiejaar: onbekend"
        )

        self.ui.lbl_dashboard_periode.setText(
            f"Periode: {periode.periode_nummer}" if periode else "Periode: onbekend"
        )

        self.ui.lbl_dashboard_klas.setText(
            f"Klas: {klas}" if klas else "Klas: onbekend"
        )

        overzicht = []
        if periode and klas:
            overzicht = self.cijfer_manager.get_docent_dashboard_overzicht(
                docent_id=self.gebruiker.gebruiker_id,
                klas=klas,
                periode_obj=periode
            )

        self.vul_dashboard_kpis(overzicht)
        self.vul_dashboard_tabel(overzicht)

    def vul_dashboard_kpis(self, overzicht):
        eindcijfers = [
            item["eindcijfer"]
            for item in overzicht
            if item["eindcijfer"] is not None
        ]

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
        self.ui.lbl_aantal_leerlingen_waarde.setText(str(len(overzicht)))

    def vul_dashboard_tabel(self, overzicht):
        tabel = self.ui.tabel_dashboard_cijfers
        tabel.setRowCount(len(overzicht))
        tabel.setEditTriggers(QTableWidget.NoEditTriggers)
        tabel.verticalHeader().setVisible(False)
        tabel.horizontalHeader().setDefaultAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        for rij, item in enumerate(overzicht):
            leerling = item["leerling"]

            item_naam = QTableWidgetItem(leerling.volledige_naam())
            item_naam.setData(Qt.UserRole, leerling)
            tabel.setItem(rij, 0, item_naam)
            tabel.setItem(
                rij,
                1,
                QTableWidgetItem(
                    "-" if item["po_gemiddelde"] is None else f"{item['po_gemiddelde']:.1f}"
                )
            )
            tabel.setItem(
                rij,
                2,
                QTableWidgetItem(
                    "-" if item["toets"] is None else f"{item['toets']:.1f}"
                )
            )
            tabel.setItem(
                rij,
                3,
                QTableWidgetItem(
                    "-" if item["eindcijfer"] is None else f"{item['eindcijfer']:.1f}"
                )
            )
            tabel.setItem(rij, 4, QTableWidgetItem(str(item["aantal_cijfers"])))

    def open_cijferoverzicht_van_dashboard(self, row, column):
        item = self.ui.tabel_dashboard_cijfers.item(row, 0)

        if item is None:
            return

        leerling = item.data(Qt.UserRole)

        if leerling is None:
            return

        self.zet_dashboard_studiejaar_en_periode_actief()
        self.zet_klas_actief(leerling.klas)
        self.vul_overzicht_leerlingen()
        self.zet_leerling_actief(leerling.gebruiker_id)

        self.toon_cijferoverzicht()
        self.vul_overzicht_tabel()
        self.vul_overzicht_kpis()

    def vul_cijferoverzicht(self):
        self.vul_overzicht_studiejaren()
        self.zet_dashboard_studiejaar_en_periode_actief()
        self.vul_overzicht_klassen()
        self.zet_klas_actief(self.dashboard_klas)
        self.vul_overzicht_leerlingen()

        self.ui.cmb_overzicht_studiejaar.currentIndexChanged.connect(
            self._on_overzicht_studiejaar_gewijzigd
        )
        self.ui.cmb_overzicht_periode.currentIndexChanged.connect(
            self._on_overzicht_filter_gewijzigd
        )
        self.ui.cmb_overzicht_klas.currentIndexChanged.connect(
            self._on_overzicht_klas_gewijzigd
        )
        self.ui.cmb_overzicht_leerling.currentIndexChanged.connect(
            self._on_overzicht_filter_gewijzigd
        )

        self.vul_overzicht_tabel()
        self.vul_overzicht_kpis()

    def vul_overzicht_studiejaren(self):
        self.ui.cmb_overzicht_studiejaar.clear()

        studiejaren = self.cijfer_manager.periode_service.studiejaar_repo.get_all()

        for sj in studiejaren:
            self.ui.cmb_overzicht_studiejaar.addItem(sj.naam, sj.studiejaar_id)

    def vul_overzicht_periodes(self):
        self.ui.cmb_overzicht_periode.clear()

        studiejaar_id = self.ui.cmb_overzicht_studiejaar.currentData()

        if studiejaar_id is None:
            return

        periodes = self.cijfer_manager.periode_service.periode_repo.get_by_studiejaar(
            studiejaar_id
        )

        for periode in periodes:
            self.ui.cmb_overzicht_periode.addItem(
                f"Periode {periode.periode_nummer}",
                periode
            )

    def vul_overzicht_klassen(self):
        self.ui.cmb_overzicht_klas.clear()

        klassen = self.leerling_repo.get_klassen()

        for klas in klassen:
            self.ui.cmb_overzicht_klas.addItem(klas, klas)

    def vul_overzicht_leerlingen(self):
        self.ui.cmb_overzicht_leerling.clear()

        klas = self.ui.cmb_overzicht_klas.currentText()

        if not klas:
            return

        leerlingen = self.leerling_repo.get_by_klas(klas)

        for leerling in leerlingen:
            self.ui.cmb_overzicht_leerling.addItem(
                leerling.volledige_naam(),
                leerling
            )

    def _on_overzicht_studiejaar_gewijzigd(self, index):
        self.vul_overzicht_periodes()
        self.vul_overzicht_tabel()
        self.vul_overzicht_kpis()

    def _on_overzicht_klas_gewijzigd(self, index):
        self.vul_overzicht_leerlingen()
        self.vul_overzicht_tabel()
        self.vul_overzicht_kpis()

    def _on_overzicht_filter_gewijzigd(self, index):
        self.vul_overzicht_tabel()
        self.vul_overzicht_kpis()

    def zet_dashboard_studiejaar_en_periode_actief(self):
        studiejaar = self.dashboard_studiejaar
        periode = self.dashboard_periode

        if studiejaar:
            index = self.ui.cmb_overzicht_studiejaar.findData(studiejaar.studiejaar_id)
            if index >= 0:
                self.ui.cmb_overzicht_studiejaar.setCurrentIndex(index)

        self.vul_overzicht_periodes()

        if periode:
            for i in range(self.ui.cmb_overzicht_periode.count()):
                periode_obj = self.ui.cmb_overzicht_periode.itemData(i)

                if periode_obj and periode_obj.periode_nummer == periode.periode_nummer:
                    self.ui.cmb_overzicht_periode.setCurrentIndex(i)
                    break

    def zet_klas_actief(self, klas):
        if not klas:
            return

        index = self.ui.cmb_overzicht_klas.findText(klas)

        if index >= 0:
            self.ui.cmb_overzicht_klas.setCurrentIndex(index)

    def zet_leerling_actief(self, leerling_id):
        for i in range(self.ui.cmb_overzicht_leerling.count()):
            leerling = self.ui.cmb_overzicht_leerling.itemData(i)

            if leerling and leerling.gebruiker_id == leerling_id:
                self.ui.cmb_overzicht_leerling.setCurrentIndex(i)
                break

    def vul_overzicht_tabel(self):
        leerling = self.ui.cmb_overzicht_leerling.currentData()
        periode_obj = self.ui.cmb_overzicht_periode.currentData()

        if leerling is None or periode_obj is None:
            self.ui.tabel_overzicht_cijfers.setRowCount(0)
            return

        cijfers = self.cijfer_manager.get_cijfers_per_leerling_per_periode(
            leerling_id=leerling.gebruiker_id,
            periode_obj=periode_obj
        )

        tabel = self.ui.tabel_overzicht_cijfers
        tabel.setColumnCount(5)
        tabel.setHorizontalHeaderLabels([
            "Onderdeel",
            "Type",
            "Cijfer",
            "Weging",
            "Datum"
        ])
        tabel.setRowCount(len(cijfers))
        tabel.setEditTriggers(QTableWidget.NoEditTriggers)
        tabel.verticalHeader().setVisible(False)
        tabel.horizontalHeader().setDefaultAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        for rij, cijfer in enumerate(cijfers):
            datum_nl = datetime.strptime(cijfer.datum, "%Y-%m-%d").strftime("%d-%m-%Y")
            tabel.setItem(rij, 0, QTableWidgetItem(cijfer.onderdeel.naam))
            tabel.setItem(rij, 1, QTableWidgetItem(cijfer.onderdeel.type))
            tabel.setItem(rij, 2, QTableWidgetItem(f"{cijfer.get_decimaal():.1f}"))
            tabel.setItem(rij, 3, QTableWidgetItem(str(cijfer.onderdeel.weging)))
            tabel.setItem(rij, 4, QTableWidgetItem(datum_nl))

    def vul_overzicht_kpis(self):
        leerling = self.ui.cmb_overzicht_leerling.currentData()
        periode_obj = self.ui.cmb_overzicht_periode.currentData()

        if leerling is None or periode_obj is None:
            return

        cijfers = self.cijfer_manager.get_cijfers_per_leerling_per_periode(
            leerling_id=leerling.gebruiker_id,
            periode_obj=periode_obj
        )

        cijferwaarden = [c.get_decimaal() for c in cijfers]

        if cijferwaarden:
            gemiddelde = sum(cijferwaarden) / len(cijferwaarden)
            laagste = min(cijferwaarden)
            hoogste = max(cijferwaarden)
        else:
            gemiddelde = None
            laagste = None
            hoogste = None

        eind = self.cijfer_manager.bereken_eindcijfer(cijfers)

        self.ui.lbl_leerling_gemiddelde_waarde.setText(
            "-" if gemiddelde is None else f"{gemiddelde:.1f}"
        )
        self.ui.lbl_leerling_aantal_cijfers_waarde.setText(
            "-" if eind is None else f"{eind:.1f}"
        )
        self.ui.lbl_leerling_laagste_waarde.setText(
            "-" if laagste is None else f"{laagste:.1f}"
        )
        self.ui.lbl_leerling_hoogste_waarde.setText(
            "-" if hoogste is None else f"{hoogste:.1f}"
        )

    def vul_cijfer_invoer(self):
        self.vul_invoer_studiejaren()
        self.vul_invoer_periodes()
        self.vul_invoer_klassen()
        self.vul_invoer_leerlingen()
        self.vul_invoer_onderdelen()
        self.ui.date_invoer_datum.setDate(QDate.currentDate())

        self.ui.cmb_invoer_studiejaar.currentIndexChanged.connect(
            self._on_invoer_studiejaar_gewijzigd
        )
        self.ui.cmb_invoer_klas.currentIndexChanged.connect(
            self._on_invoer_klas_gewijzigd
        )

    def vul_invoer_studiejaren(self):
        self.ui.cmb_invoer_studiejaar.clear()

        studiejaren = self.cijfer_manager.periode_service.studiejaar_repo.get_all()

        for sj in studiejaren:
            self.ui.cmb_invoer_studiejaar.addItem(sj.naam, sj)

    def vul_invoer_periodes(self):
        self.ui.cmb_invoer_periode.clear()

        studiejaar = self.ui.cmb_invoer_studiejaar.currentData()

        if studiejaar is None:
            return

        periodes = self.cijfer_manager.periode_service.periode_repo.get_by_studiejaar(
            studiejaar.studiejaar_id
        )

        for periode in periodes:
            self.ui.cmb_invoer_periode.addItem(
                f"Periode {periode.periode_nummer}",
                periode
            )

    def vul_invoer_klassen(self):
        self.ui.cmb_invoer_klas.clear()

        klassen = self.leerling_repo.get_klassen()

        for klas in klassen:
            self.ui.cmb_invoer_klas.addItem(klas, klas)

    def vul_invoer_leerlingen(self):
        self.ui.cmb_invoer_leerling.clear()

        klas = self.ui.cmb_invoer_klas.currentText()

        if not klas:
            return

        leerlingen = self.leerling_repo.get_by_klas(klas)

        for leerling in leerlingen:
            self.ui.cmb_invoer_leerling.addItem(
                leerling.volledige_naam(),
                leerling
            )

    def vul_invoer_onderdelen(self):
        self.ui.cmb_invoer_onderdeel.clear()

        onderdelen = self.onderdeel_repo.get_all()

        for onderdeel in onderdelen:
            self.ui.cmb_invoer_onderdeel.addItem(
                onderdeel.naam,
                onderdeel
            )

    def _on_invoer_klas_gewijzigd(self, index):
        self.vul_invoer_leerlingen()

    def _on_invoer_studiejaar_gewijzigd(self, index):
        self.vul_invoer_periodes()

    #opslaan
    def sla_cijfer_op(self):
        leerling = self.ui.cmb_invoer_leerling.currentData()
        onderdeel = self.ui.cmb_invoer_onderdeel.currentData()
        studiejaar = self.ui.cmb_invoer_studiejaar.currentData()
        periode = self.ui.cmb_invoer_periode.currentData()
        tekst = self.ui.txt_invoer_cijfer.text().strip().replace(",", ".")
        try:
            waarde = float(tekst)
        except ValueError:
            self.ui.lbl_invoer_melding.setStyleSheet("color: red;")
            self.ui.lbl_invoer_melding.setText("Voer een geldig cijfer in.")
            return
        datum = self.ui.date_invoer_datum.date().toString("yyyy-MM-dd")

        if leerling is None or onderdeel is None or studiejaar is None or periode is None:
            self.ui.lbl_invoer_melding.setStyleSheet("color: red;")
            self.ui.lbl_invoer_melding.setText("Selecteer studiejaar, periode, leerling en onderdeel.")
            return

        if waarde < 1 or waarde > 10:
            self.ui.lbl_invoer_melding.setStyleSheet("color: red;")
            self.ui.lbl_invoer_melding.setText("Cijfer moet tussen 1 en 10 liggen.")
            return
        waarde_db = int(round(waarde * 10))

        #controle
        bestaat_al = self.cijfer_manager.cijfer_repo.bestaat_cijfer(
            leerling_id=leerling.gebruiker_id,
            onderdeel_id=onderdeel.onderdeel_id,
            studiejaar=studiejaar.naam,
            periode=periode.periode_nummer
        )

        if bestaat_al:
            self.ui.lbl_invoer_melding.setStyleSheet("color: red;")
            self.ui.lbl_invoer_melding.setText(
                "Voor deze leerling bestaat al een cijfer voor dit onderdeel in deze periode."
            )
            return

        try:
            self.cijfer_manager.sla_cijfer_op(
                leerling=leerling,
                onderdeel=onderdeel,
                docent=self.gebruiker,
                waarde=waarde_db,
                datum=datum,
                studiejaar=studiejaar,
                periode=periode
            )
            self.ui.lbl_invoer_melding.setStyleSheet("color: green;")
            self.ui.lbl_invoer_melding.setText("Cijfer is opgeslagen.")

            self.reset_invoerformulier()

            self.vul_dashboard()
            self.vul_overzicht_tabel()
            self.vul_overzicht_kpis()

            QTimer.singleShot(
                3000,
                lambda: self.ui.lbl_invoer_melding.clear()
            )

        except Exception as fout:
            self.ui.lbl_invoer_melding.setStyleSheet("color: red;")
            self.ui.lbl_invoer_melding.setText("Cijfer kon niet worden opgeslagen.")
            print("FOUT bij opslaan cijfer:", fout)

    def reset_invoerformulier(self):
        self.ui.cmb_invoer_klas.setCurrentIndex(0)

        self.vul_invoer_leerlingen()

        self.ui.cmb_invoer_leerling.setCurrentIndex(0)
        self.ui.cmb_invoer_onderdeel.setCurrentIndex(0)

        self.ui.txt_invoer_cijfer.clear()

        self.ui.date_invoer_datum.setDate(QDate.currentDate())
        
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