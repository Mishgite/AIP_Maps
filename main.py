from PyQt5.QtWidgets import QMainWindow, QLabel, QApplication, QComboBox
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from map_scale_utils import get_scale_params
import requests
import os

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
        self.l = 'map'
        self.degr = 0.005

        self.label = QLabel(self)
        self.label.resize(600, 450)
        self.update()

        self.combo = QComboBox(self)
        self.combo.setGeometry(520, 10, 70, 20)
        self.combo.addItems(['схема', 'спутник', 'гибрид'])
        self.combo.currentTextChanged.connect(self.set_layer)

    def update(self):
        params = get_scale_params(coordinates[0], coordinates[1], self.z, self.l)
        file = request_image(**params)
        pixmap = QtGui.QPixmap(file)
        os.remove(file)
        self.label.setPixmap(pixmap)

    def set_layer(self, l):
        if l == 'схема':
            self.l = 'map'
        if l == 'спутник':
            self.l = 'sat'
        if l == 'гибрид':
            self.l = 'skl'
        self.label.setFocus()
        self.update()


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
