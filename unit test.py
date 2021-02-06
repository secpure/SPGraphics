from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import SPGraphics


style = '''
#mainWidget,
#shadowWidget
{
    background-color: white;
}

QMarkNotify
{
    background-color: red;
    border-radius: 5px;
}

QMenu
{
    background: transparent;
}

QuickToolTip #mainWidget
{
    background: rgba(0, 0, 0, 150);
    border-radius: 10px;
    border: 0px solid black;
}
QuickToolTip QLabel
{
    color: white;
}
'''


class Main(SPGraphics.QuickMainWidget):
    def __init__(self, parent):
        super(Main, self).__init__(parent)

        self.resize(400, 400)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet(style)
        self.mainWidget.setLayout(QVBoxLayout())
        self.mainWidget.layout().setAlignment(Qt.AlignTop)

        self.__leftClickPressed = None
        self.__clickPressedX = None
        self.__clickPressedY = None

        self.tooltip = SPGraphics.QuickToolTip(
            parent=self,
            text='Hello World!\nHello World!\nHello World!Hello World!Hello World!Hello World!',
            pixmap=QPixmap('icon.png'),
            align=Qt.AlignLeft,
            arrow_size=QSize(8, 15),
            arrow_padding=15,
            margin=20,
            arrow_align=Qt.AlignCenter
        )

        self.pushButton = SPGraphics.QuickPushButton(
            parent=self.mainWidget,
            text='Push Button',
            icon=QIcon('icon.png'),
            icon_size=QSize(24, 24),
            value_changed=self.animate,
            start_value=QColor(Qt.white),
            end_value=QColor(Qt.yellow),
            cursor=Qt.PointingHandCursor,
            tooltip=self.tooltip
        )
        self.pushButton.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))

        self.dialog = SPGraphics.QuickDialog(self, fixed_size=QSize(401, 201))

        self.tooltip2 = SPGraphics.QuickToolTip(
            parent=self,
            text='Hello World!',
            pixmap=QPixmap('icon.png'),
            align=Qt.AlignLeft,
            arrow_size=QSize(8, 15),
            arrow_padding=15,
            margin=20,
            arrow_align=Qt.AlignTop
        )

        self.pushButton2 = SPGraphics.QuickPushButton(
            parent=self.mainWidget,
            text='Push Button',
            icon=QIcon('icon.png'),
            icon_size=QSize(24, 24),
            cursor=Qt.PointingHandCursor,
            tooltip=self.tooltip2
        )
        self.pushButton2.setLayout(QHBoxLayout())
        self.pushButton2.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))

        self.mark = SPGraphics.QMarkNotify(self.mainWidget)
        self.mark.show()

        self.menu = SPGraphics.QuickMenu(
            parent=self.mainWidget,
            shadow=SPGraphics.QuickShadow(radius=20, offset=0),
            margin=20,
            margin_top=0,
            margin_left=0
        )
        self.menu.mainWidget.setLayout(QVBoxLayout())

        for i in range(5):
            button = SPGraphics.QuickPushButton(
                parent=self.mainWidget,
                text='Push Button',
                icon=QIcon('icon.png'),
                icon_size=QSize(24, 24),
                fixed_size=QSize(151, 41),
                value_changed=self.animate,
                start_value=QColor(Qt.white),
                end_value=QColor(Qt.yellow),
                cursor=Qt.PointingHandCursor
            )
            button.clicked.connect(self.push_button_animated_click)
            self.menu.mainWidget.layout().addWidget(button)

        self.tooltip3 = SPGraphics.QuickToolTip(
            parent=self,
            text='Hello World! Hello World!\nHello World!',
            pixmap=QPixmap('icon.png'),
            align=Qt.AlignLeft,
            arrow_size=QSize(50, 10),
            arrow_padding=10,
            margin=80,
            arrow_align=Qt.AlignBottom,
            timeout=1000
        )

        self.pushButton3 = SPGraphics.QuickPushButton(
            parent=self.mainWidget,
            text='Push Button',
            icon=QIcon('icon.png'),
            icon_size=QSize(24, 24),
            cursor=Qt.PointingHandCursor,
            tooltip=self.tooltip3
        )
        self.pushButton3.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))

        self.mainWidget.layout().addWidget(self.pushButton)
        self.mainWidget.layout().addWidget(self.pushButton2)
        self.mainWidget.layout().addWidget(self.pushButton3)
        self.pushButton2.layout().addWidget(self.mark, alignment=Qt.AlignTop | Qt.AlignRight)

        self.pushButton.clicked.connect(self.dialog.exec_)
        self.pushButton2.clicked.connect(self.push_button)

    def mousePressEvent(self, event):
        super(Main, self).mousePressEvent(event)

        if event.button() == Qt.LeftButton and self.underMouse():
            self.__clickPressedX = event.pos().x()
            self.__clickPressedY = event.pos().y()
            self.__leftClickPressed = True

    def mouseReleaseEvent(self, event):
        super(Main, self).mouseReleaseEvent(event)

        self.__leftClickPressed = False

    def mouseMoveEvent(self, event):
        super(Main, self).mouseMoveEvent(event)

        if self.__leftClickPressed:
            x = event.globalPos().x() - self.__clickPressedX
            y = event.globalPos().y() - self.__clickPressedY
            self.move(x, y)

    def animate(self, value):
        sender = self.sender()
        if not isinstance(sender, QVariantAnimation):
            return

        css = 'background-color: rgba%s;' % str(value.getRgb())
        sender.parent().setStyleSheet(css)

    def push_button(self):
        pos = self.sender().mapToGlobal(QPoint())
        self.menu.exec_()

    def push_button_animated_click(self):
        count = self.menu.mainWidget.layout().count()
        widget = self.menu.mainWidget.layout().itemAt(count - 1).widget()

        self.menu.mainWidget.layout().removeWidget(widget)
        self.menu.mainWidget.layout().takeAt(count - 1)

        # Add/Remove live use below adjust method
        self.menu.mainWidget.adjustSize()
        self.menu.adjustSize()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main(None)
    main.show()
    app.exec_()
