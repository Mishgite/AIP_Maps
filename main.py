from PyQt5.QtWidgets import QMainWindow, QLabel, QApplication
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from map_scale_utils import get_scale_params
import requests
import os
import math

coordinates = ['37.541776', '55.706857']
base_url = 'https://static-maps.yandex.ru/1.x/'


def request_image(**kwargs):
    response = requests.get(base_url, params=kwargs)
    print(kwargs)
    if response:
        datafile = 'img.jpg'

        with open(datafile, 'wb') as data:
            data.write(response.content)

        return datafile
    else:
        print('Неверный запрос')


class Map(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(300, 300, 600, 450)
        self.setWindowTitle('Карта')
        self.z = 15
        self.degr = 0.005

        self.label = QLabel(self)
        self.label.resize(600, 450)
        self.update()

    def update(self):
        params = get_scale_params(coordinates[0], coordinates[1], self.z)
        file = request_image(**params)
        pixmap = QtGui.QPixmap(file)
        os.remove(file)
        self.label.setPixmap(pixmap)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            if self.z != 21:
                self.z += 1
                self.degr /= 2.5
        elif event.key() == Qt.Key_PageDown:
            if self.z != 1:
                self.z -= 1
                self.degr *= 2.5
        elif event.key() == Qt.Key_Left:
            cord = float(coordinates[0])
            cord -= self.degr
            coordinates[0] = str(cord)
        elif event.key() == Qt.Key_Right:
            cord = float(coordinates[0])
            cord += self.degr
            coordinates[0] = str(cord)
        elif event.key() == Qt.Key_Up:
            cord = float(coordinates[1])
            cord += self.degr
            coordinates[1] = str(cord)
        elif event.key() == Qt.Key_Down:
            cord = float(coordinates[1])
            cord -= self.degr
            coordinates[1] = str(cord)
        self.update()


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    ex = Map()
    ex.show()
    sys.exit(app.exec_())
