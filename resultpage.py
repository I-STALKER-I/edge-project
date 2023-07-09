import typing
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QDialog, QMainWindow 

class SingleResultWidget(QWidget):
    def __init__(self, SingleRow):  # SingleRow: 0 -> image , 1 -> descrip , 2 -> price , 3 -> link , 4 -> market , 5 -> Name
        super().__init__()

class ResultDialog(QDialog):
    def __init__(self, data):
        super().__init__()

        self.setWindowTitle("Results")
        self.widgets_list = [] # this contain a list of SingleResultWidget

        layout = QVBoxLayout()
        self.setLayout(layout)

        if len(data) < 1:
            #show error
            self.error_label = QLabel()
            self.error_label.setStyleSheet("color: red;")
            layout.addWidget(self.error_label)
            self.error_label.setText("there is no result for your search")
        else :
            for r in data:
                w = SingleResultWidget(r)
                layout.addWidget(w)
                self.widgets_list.append(w)


        #login button
        login_button = QPushButton("Close")
        login_button.clicked.connect(self.closing)
        layout.addWidget(login_button)


    def closing(self):
        print("result Page Closed")
        self.accept()
        self.close()


