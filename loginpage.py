import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton
from time import sleep

class Login(QWidget):
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

        #show the page
        self.show()


    def login(self):
        username = self.username_edit.text()
        password = self.password_edit.text()

        # Check if credentials are valid
        if username == "admin" and password == "password123":
            print("Login successful!")
            self.close()
        else:
            self.error_label.setText("Invalid username or password")

    def signup(self):
        signup_window = Signup()
        signup_window.exec_()

class Signup(QWidget):
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

        #city box
        city_label = QLabel("enetr your city:")
        self.city_edit = QLineEdit()
        layout.addWidget(city_label)
        layout.addWidget(self.city_edit)

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

        #sign up button
        signup_button = QPushButton("Sign up")
        signup_button.clicked.connect(self.signup)
        layout.addWidget(signup_button)

        #show eroor
        self.error_label = QLabel()
        self.error_label.setStyleSheet("color: red;")
        layout.addWidget(self.error_label)

        #show the page
        self.show()

    def signup(self):
        username = self.username_edit.text()
        city = self.city_edit.text()
        password = self.password_edit.text()
        confirm_password = self.confirm_password_edit.text()

        # Check if passwords match
        if password != confirm_password:
            self.error_label.setText("Passwords do not match")
            return

        # Store username and password in database
        print(f"New user '{username}' created with password '{password}'")
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_window = Login()
    sys.exit(app.exec_())
