import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QDialog, QMainWindow 
from mainpage1 import Ui_MainWindow
import mainclient
from time import sleep


class Login(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Login")

        layout = QVBoxLayout()
        self.setLayout(layout)

        #username box
        username_label = QLabel("Username:")
        self.username_edit = QLineEdit()
        layout.addWidget(username_label)
        layout.addWidget(self.username_edit)

        #password box
        password_label = QLabel("Password:")
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.Password)
        layout.addWidget(password_label)
        layout.addWidget(self.password_edit)

        #login button
        login_button = QPushButton("Login")
        login_button.clicked.connect(self.login)
        layout.addWidget(login_button)

        #sign up button
        signup_button = QPushButton("Sign up")
        signup_button.clicked.connect(self.signup)
        layout.addWidget(signup_button)

        #show error
        self.error_label = QLabel()
        self.error_label.setStyleSheet("color: red;")
        layout.addWidget(self.error_label)

    def login(self):
        username = self.username_edit.text()
        password = self.password_edit.text()

        # Check if credentials are valid
        if mainclient.main('signin', username, password):
            print("Login successful!")
            self.accept()
            self.close()

        else:
            self.error_label.setText("Invalid username or password")

    def signup(self):
        self.close()
        signup_window = Signup()
        result = signup_window.exec_()
        if result == QDialog.DialogCode.Accepted:
            self.accept()


class Signup(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sign Up")

        layout = QVBoxLayout()
        self.setLayout(layout)

        #username box
        username_label = QLabel("Choose a username:")
        self.username_edit = QLineEdit()
        layout.addWidget(username_label)
        layout.addWidget(self.username_edit)

        #password box
        password_label = QLabel("Choose a password:")
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.Password)
        layout.addWidget(password_label)
        layout.addWidget(self.password_edit)

        #confirm password box
        confirm_password_label = QLabel("Confirm password:")
        self.confirm_password_edit = QLineEdit()
        self.confirm_password_edit.setEchoMode(QLineEdit.Password)
        layout.addWidget(confirm_password_label)
        layout.addWidget(self.confirm_password_edit)

        #city box
        city_label = QLabel("enetr your city:")
        self.city_edit = QLineEdit()
        layout.addWidget(city_label)
        layout.addWidget(self.city_edit)

        #sign up button
        signup_button = QPushButton("Sign up")
        #signup_button.setStyleSheet("color: rgb(0, 0, 0);\n"
#"background-color: qconicalgradient(cx:0, cy:0, angle:135, stop:0 rgba(255, 255, 0, 69), stop:0.375 rgba(255, 255, 0, 69), stop:0.423533 rgba(251, 255, 0, 145), stop:0.45 rgba(247, 255, 0, 208), stop:0.477581 rgba(255, 244, 71, 130), stop:0.518717 rgba(255, 218, 71, 130), stop:0.55 rgba(255, 255, 0, 255), stop:0.57754 rgba(255, 203, 0, 130), stop:0.625 rgba(255, 255, 0, 69), stop:1 rgba(255, 255, 0, 69));")
        signup_button.clicked.connect(self.signup)
        layout.addWidget(signup_button)

        #show eroor
        self.error_label = QLabel()
        self.error_label.setStyleSheet("color: red;")
        layout.addWidget(self.error_label)


    def signup(self):
        username = self.username_edit.text()
        city = self.city_edit.text()
        password = self.password_edit.text()
        confirm_password = self.confirm_password_edit.text()

        # Check if passwords match
        if mainclient.main('signup', username, password, password_again = confirm_password):
            print(f"New user '{username}' created with password '{password}'")
            self.accept()
            self.close()
        else:
            self.error_label.setText("Passwords do not match")
            return
