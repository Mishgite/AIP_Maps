from PyQt5.QtWidgets import QMainWindow, QLabel, QApplication
from PyQt5.QtGui import QPixmap
from map_scale_utils import get_scale_params
import requests
import os

coordinates = ['37.541676', '55.706857']
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

        self.label = QLabel(self)
        self.label.resize(600, 450)

        params = get_scale_params(coordinates[0], coordinates[1])
        file = request_image(**params)
        pixmap = QPixmap(file)
        os.remove(file)
        self.label.setPixmap(pixmap)


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    ex = Map()
    ex.show()
    sys.exit(app.exec_())
