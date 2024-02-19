from PyQt5.QtWidgets import QMainWindow, QLabel, QApplication, QComboBox, QLineEdit, QPushButton, QRadioButton, QButtonGroup
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from map_scale_utils import get_scale_params
import requests
import pprint
import os


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
        self.delta = 0.004
        self.degr = self.delta / 2
        self.l = 'map'
        self.pt = None
        self.postcode = ''
        self.coordinates = ['37.541776', '55.706857']

        self.label = QLabel(self)
        self.label.resize(600, 450)
        self.update()

        self.combo = QComboBox(self)
        self.combo.setGeometry(520, 10, 70, 20)
        self.combo.addItems(['схема', 'спутник', 'гибрид'])
        self.combo.currentTextChanged.connect(self.set_layer)
        self.coordinates_input = QLineEdit(self)
        self.coordinates_input.setGeometry(10, 10, 80, 20)

        self.btn = QPushButton('Искать', self)
        self.btn.resize(self.btn.sizeHint())
        self.btn.setGeometry(90, 10, 80, 20)
        self.btn.clicked.connect(self.coordinates_place)

        self.clear = QPushButton('Сброс поискового результата', self)
        self.clear.move(175, 10)
        self.clear.resize(self.clear.sizeHint())
        self.clear.setFixedHeight(20)
        self.clear.clicked.connect(self.clear_pos)

        self.label1 = QLabel(self)
        self.label1.setText("")
        self.label1.move(10, 30)
        self.label1.resize(590, 10)

        self.label2 = QLabel(self)
        self.label2.setText("Почтовый индекс")
        self.label2.move(10, 50)
        self.label2.resize(590, 10)

        self.text = QRadioButton('Вкл', self)
        self.text.setChecked(True)
        self.text.move(10, 60)

        self.text1 = QRadioButton('Выкл', self)
        self.text1.move(10, 80)

        self.color_group_1 = QButtonGroup(self)
        self.color_group_1.addButton(self.text)
        self.color_group_1.addButton(self.text1)
        self.color_group_1.buttonClicked.connect(self.change_lbl)

        self.label.setFocus()

    def update(self):
        params = get_scale_params(
            self.coordinates[0], self.coordinates[1], self.delta, self.delta * 0.75, self.l, self.pt
        )
        file = request_image(**params)
        pixmap = QtGui.QPixmap(file)
        os.remove(file)
        self.label.setPixmap(pixmap)

    def change_lbl(self, button: QRadioButton):
        if self.postcode:
            if button.text() == 'Вкл':
                self.label1.setText(self.label1.text() + f', {self.postcode}')
            else:
                text = self.label1.text()
                self.label1.setText(text[:text.rfind(',')])

    def clear_pos(self):
        self.pt = None
        self.label.setFocus()
        self.label1.setText("")
        self.postcode = ''
        self.update()

    def set_layer(self, l):
        if l == 'схема':
            self.l = 'map'
        if l == 'спутник':
            self.l = 'sat'
        if l == 'гибрид':
            self.l = 'skl'
        self.label.setFocus()
        self.update()

    def coordinates_place(self):
        if self.coordinates_input.text() != '':
            geocoder_request = f"http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={self.coordinates_input.text()}&format=json"
            response = requests.get(geocoder_request)
            if response:
                json_response = response.json()
                toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
                toponym_coodrinates = toponym["Point"]["pos"].split()
                toponym_address = toponym["metaDataProperty"]["GeocoderMetaData"]["text"]
                self.postcode = toponym["metaDataProperty"]["GeocoderMetaData"]['Address']['postal_code']
                if self.color_group_1.checkedButton().text() == 'Вкл':
                    a = self.postcode
                    self.label1.setText(f'{toponym_address}, {a}')
                else:
                    self.label1.setText(toponym_address)
                self.coordinates = toponym_coodrinates
                self.pt = self.coordinates[:]
                print(toponym_address)
                self.label.setFocus()
            else:
                self.label1.setText('Неправильный формат запроса')
        self.update()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            self.delta /= 2
            self.degr /= 2
        elif event.key() == Qt.Key_PageDown:
            self.delta *= 2
            self.degr *= 2
        elif event.key() == Qt.Key_Left:
            cord = float(self.coordinates[0])
            cord -= self.degr
            self.coordinates[0] = str(cord)
        elif event.key() == Qt.Key_Right:
            cord = float(self.coordinates[0])
            cord += self.degr
            self.coordinates[0] = str(cord)
        elif event.key() == Qt.Key_Up:
            cord = float(self.coordinates[1])
            cord += self.degr
            self.coordinates[1] = str(cord)
        elif event.key() == Qt.Key_Down:
            cord = float(self.coordinates[1])
            cord -= self.degr
            self.coordinates[1] = str(cord)

        self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            print(f"Координаты:{event.x()}, {event.y()}")


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    ex = Map()
    ex.show()
    sys.exit(app.exec_())