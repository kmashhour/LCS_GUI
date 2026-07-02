from PySide6.QtWidgets import QWidget
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile

from services.authenticatie_service import AuthenticatieService
from views.leerling.dashboard_leerling_view import DashboardLeerlingView
from views.docent.dashboard_docent_view import DashboardDocentView


class LoginView(QWidget):
    def __init__(self):
        super().__init__()

        # UI laden
        ui_file = QFile("ui/login.ui")
        ui_file.open(QFile.ReadOnly)

        loader = QUiLoader()
        self.ui = loader.load(ui_file)
        ui_file.close()

        # UI instellen
        self.setWindowTitle(self.ui.windowTitle())
        self.setFixedSize(self.ui.size())
        self.setLayout(self.ui.layout())

        #service
        self.auth = AuthenticatieService()

        # events
        self.ui.btn_login.clicked.connect(self.handle_login)

    def handle_login(self):
        username = self.ui.input_username.text().strip()
        password = self.ui.input_password.text().strip()

        gebruiker = self.auth.login(username, password)

        if gebruiker is None:
            self.ui.lbl_error.setText("Gebruikersnaam of wachtwoord onjuist")
            return

        self.open_dashboard(gebruiker)

    def open_dashboard(self, gebruiker):
        rol = gebruiker.rol.lower()

        if rol == "leerling":
            self.dashboard = DashboardLeerlingView(gebruiker)
            self.close()
        elif rol == "docent":
            self.dashboard = DashboardDocentView(gebruiker)
            self.dashboard.show()
            self.close()
        else:
            self.ui.lbl_error.setText(f"Onbekende rol: {rol}")
            return

        self.dashboard.show()
        self.close()
