import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog
from loginpage import Login, Signup
from mainpage1 import Ui_MainWindow

def main():
    app = QApplication(sys.argv)
    login_diolog = Login()
    result = login_diolog.exec_()

    if result == QDialog.DialogCode.Accepted:
        MainWindow = QMainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(MainWindow)
        MainWindow.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()