from PyQt5.QtWidgets import QMainWindow, QLabel
from PyQt5.QtGui import QPixmap
import requests

coordinates = ['37.541676', '55.706857']


# def request(**kwargs):



class Map(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(600, 450)
        self.setWindowTitle('Карта')

        self.label = QLabel(self)
        self.label.resize(600, 450)