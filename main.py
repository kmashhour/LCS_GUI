# Tijdelijke startfile totdat de GUI is gebouwd.

#def main():
#    print("Project LCS_GUI")
#    print("GUI wordt later toegevoegd.")

#if __name__ == "__main__":
#    main()
from PySide6.QtWidgets import QApplication
from views.login_view import LoginView

def main():
    app = QApplication([])

    login = LoginView()
    login.show()

    app.exec()

if __name__ == "__main__":
    main()