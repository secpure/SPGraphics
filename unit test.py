from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import SPGraphics


class Main(QWidget):
    def __init__(self, parent):
        super(Main, self).__init__(parent)

        self.resize(400, 400)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main(None)
    main.show()
    app.exec_()
