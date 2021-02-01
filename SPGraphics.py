from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from password_strength import PasswordStats
import sys
import SPInputmanager


# // Values
_FLAGS = Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint
_TRANSLATOR = QApplication.translate
_WINDOWS = sys.platform == 'win32'
_WINDOW_SIZE = QSize(401, 161)
_SIZE21 = QSize(21, 21)
_SIZE25 = QSize(25, 25)
_SIZE41 = QSize(41, 41)
_STYLESHEET = ''
_WINDOW_TITLE = ''
_TITLE_TEXT = ''
_TITLE_FONT = QFont('Arial', 12)

LINE_EDIT_PLACEHOLDER = "Confirm your password"
LAYOUT_DIRECTION = Qt.LeftToRight


def text_ellipsis(target, mode=Qt.ElideRight, width: int = None):
    text = target.text()
    if not width:
        width = target.contentsRect().width()

    metrics = QFontMetrics(target.font())
    if metrics.width(text) > width:
        elided = metrics.elidedText(text, mode, width)
        target.setText(elided)
        target.setToolTip(text)


def smooth_scroll(target, step: int = 8):
    target.verticalScrollBar().setSingleStep(step)
    target.horizontalScrollBar().setSingleStep(step)


def combobox_style(target):
    flags = Qt.Popup | Qt.FramelessWindowHint
    list_view = QListView()
    list_view.setIconSize(_SIZE21)
    target.setView(list_view)
    target.view().window().setWindowFlags(flags)
    target.view().window().setAttribute(Qt.WA_TranslucentBackground, True)


class _Signals(QObject):
    process = pyqtSignal()
    progress = pyqtSignal(int)


class _ThreadingArea(QThread):
    def __init__(self, core, parent=None):
        super(_ThreadingArea, self).__init__(parent)

        self.issue = None
        self.core = core
        self.signal = _Signals()

    def run(self):
        try:
            self.core()
        except Exception as error:
            self.issue = error
            (_type, _value, _traceback) = sys.exc_info()
            sys.excepthook(_type, _value, _traceback)


class _Color:
    FONT = '#FFFFFF'
    INFORMATION = '#FFFFFF'
    WARNING = '#FF7676'
    SUCCESS = '#00DF6C'
    FAILED = '#FF7676'


class _Icon:
    CLOSE = str()
    ENTER = str()
    EYE_SHOW = str()
    INFORMATION = str()
    WARNING = str()
    SUCCESS = str()
    FAILED = str()


class State:
    class __SubState:
        icon = None
        color = None

    information = __SubState()
    information.icon = _Icon.INFORMATION
    information.color = _Color.INFORMATION

    warning = __SubState()
    warning.icon = _Icon.WARNING
    warning.color = _Color.WARNING

    success = __SubState()
    success.icon = _Icon.SUCCESS
    success.color = _Color.SUCCESS

    failed = __SubState()
    failed.icon = _Icon.FAILED
    failed.color = _Color.FAILED


class Setup:
    @staticmethod
    def set_icons(
            eye_show: str, eye_hide: str, enter_button: str, close_button: str,
            information_state: str, warning_state: str, success_state: str, failed_state: str
    ):
        """Set all icons as string path, EX: ':/images/icons/icon.png'"""

        SPInputmanager.Setup.set_icons(eye_show, eye_hide)

        _Icon.ENTER = enter_button
        _Icon.EYE_SHOW = eye_show
        _Icon.CLOSE = close_button
        _Icon.INFORMATION = information_state
        _Icon.WARNING = warning_state
        _Icon.SUCCESS = success_state
        _Icon.FAILED = failed_state

        State.information.icon = information_state
        State.warning.icon = warning_state
        State.success.icon = success_state
        State.failed.icon = failed_state

    @staticmethod
    def set_colors(font: str, information: str, warning: str, success: str, failed: str):
        _Color.FONT = font
        _Color.INFORMATION = information
        _Color.WARNING = warning
        _Color.SUCCESS = success
        _Color.FAILED = failed

        State.information.color = information
        State.warning.color = warning
        State.success.color = success
        State.failed.color = failed

    @staticmethod
    def set_message_box_details(
            window_title: str, title_text: str, title_font: QFont = None, stylesheet: str = None
    ):

        global _WINDOW_TITLE, _TITLE_TEXT, _TITLE_FONT, _STYLESHEET
        _WINDOW_TITLE = window_title
        _TITLE_TEXT = title_text

        if title_font:
            _TITLE_FONT = title_font

        if stylesheet:
            _STYLESHEET = stylesheet


class MessageBoxButtonObject:
    def __init__(self, *args, **kwargs):
        """MessageBox button data type"""
        pass


class Button:
    CLOSE = MessageBoxButtonObject()
    ACCEPT = MessageBoxButtonObject()
    CANCEL = MessageBoxButtonObject()


class Property:
    OPACITY = b'opacity'
    WINDOW_OPACITY = b'windowOpacity'
    MAXIMUM_SIZE = b'maximumWidth'
    GEOMETRY = b'geometry'


class OpacityMotion(QPropertyAnimation):
    def __init__(self, target, property_type: bytes = None):
        opacity = (property_type is Property.OPACITY)
        auto = (not property_type and target.parent())

        if opacity or auto:
            effect = QGraphicsOpacityEffect(target)
            target.setGraphicsEffect(effect)
            super(OpacityMotion, self).__init__(effect, Property.OPACITY)

        elif not _WINDOWS:
            effect = QGraphicsOpacityEffect()
            super(OpacityMotion, self).__init__(effect, Property.OPACITY)

        else:
            super(OpacityMotion, self).__init__(target, Property.WINDOW_OPACITY)

    def temp_show(self, duration: int = 300, finished: callable = None):
        """
        Show widget as opacity
        :param duration: int
        :param finished: callable
        :return: QPropertyAnimation
        """

        self.setDuration(duration)
        self.setStartValue(0)
        self.setEndValue(1)
        self.setEasingCurve(QEasingCurve.OutQuad)

        if callable(finished):
            self.finished.connect(finished)

        return self

    def temp_hide(self, duration: int = 500, finished: callable = None):
        """
        Hide widget as opacity
        :param duration: int
        :param finished: callable
        :return: QPropertyAnimation
        """

        self.setDuration(duration)
        self.setStartValue(1)
        self.setEndValue(0)
        self.setEasingCurve(QEasingCurve.OutQuad)

        if callable(finished):
            self.finished.connect(finished)

        return self


class GeometryMotion(QPropertyAnimation):
    def __init__(self, target):
        super(GeometryMotion, self).__init__(target, Property.GEOMETRY)
        self._target = target

    def temp_x(
            self, start_x: int = None, end_x: int = None,
            duration: int = 500, finished: callable = None
    ):
        """
        Move x widget
        :param start_x: int
        :param end_x: int
        :param duration: int
        :param finished: callable
        :return: QPropertyAnimation
        """

        rect = self._target.geometry()
        if not start_x:
            start_x = rect.x()

        self.setDuration(duration)
        self.setStartValue(QRect(start_x, rect.y(), rect.width(), rect.height()))
        self.setEndValue(QRect(end_x, rect.y(), rect.width(), rect.height()))

        if callable(finished):
            self.finished.connect(finished)

        return self

    def temp_y(
            self, start_y: int = None, end_y: int = None,
            duration: int = 500, finished: callable = None
    ):
        """
        Move y widget
        :param start_y: int
        :param end_y: int
        :param duration: int
        :param finished: callable
        :return: QPropertyAnimation
        """

        rect = self._target.geometry()
        if not start_y:
            start_y = rect.y()

        self.setDuration(duration)
        self.setStartValue(QRect(rect.x(), start_y, rect.width(), rect.height()))
        self.setEndValue(QRect(rect.x(), end_y, rect.width(), rect.height()))

        if callable(finished):
            self.finished.connect(finished)

        return self

    def temp_show(
            self, width: int, end_x: int, duration: int = 500, finished: callable = None
    ):
        """
        Show as book widget
        :param width: int
        :param end_x: int
        :param duration: int
        :param finished: callable
        :return: QPropertyAnimation
        """

        rect = self._target.geometry()
        start_x = (width - 41) + end_x

        self.setDuration(duration)
        self.setStartValue(QRect(start_x, rect.y(), 0, rect.height()))
        self.setEndValue(QRect(end_x, rect.y(), width, rect.height()))

        if callable(finished):
            self.finished.connect(finished)

        return self

    def temp_hide(self, duration: int = 250, finished: callable = None):
        """
        Hide as book widget
        :param duration: int
        :param finished: callable
        :return: QPropertyAnimation
        """

        rect = self._target.geometry()
        end_x = (rect.width() - 41) + rect.x()

        self.setDuration(duration)
        self.setStartValue(QRect(rect.x(), rect.y(), rect.width(), rect.height()))
        self.setEndValue(QRect(end_x, rect.y(), 0, rect.height()))

        if finished:
            self.finished.connect(finished)

        return self

    def temp_open(self, width: int, duration: int = 500, finished: callable = None):
        """
        Show widget from left to right
        :param width: int
        :param duration: int
        :param finished: callable
        :return: QPropertyAnimation
        """

        rect = self._target.geometry()

        self.setDuration(duration)
        self.setStartValue(QRect(rect.x(), rect.y(), 0, rect.height()))
        self.setEndValue(QRect(rect.x(), rect.y(), width, rect.height()))

        if callable(finished):
            self.finished.connect(finished)

        return self

    def temp_close(self, duration: int = 250, finished: callable = None):
        """
        Hide widget from right to left
        :param duration: int
        :param finished: callable
        :return: QPropertyAnimation
        """

        rect = self._target.geometry()

        self.setDuration(duration)
        self.setStartValue(QRect(rect.x(), rect.y(), rect.width(), rect.height()))
        self.setEndValue(QRect(rect.x(), rect.y(), 0, rect.height()))

        if callable(finished):
            self.finished.connect(finished)

        return self


class MaximumWidthMotion(QPropertyAnimation):
    def __init__(self, target):
        super(MaximumWidthMotion, self).__init__(target, Property.MAXIMUM_SIZE)
        self._target = target

    def temp_show(self, width: int, duration: int = 1000, finished: callable = None):
        """
        Show widget from left to right
        :param width: int
        :param duration: int
        :param finished: callable
        :return: QPropertyAnimation
        """

        self.setDuration(duration)
        self.setStartValue(0)
        self.setEndValue(width)

        if callable(finished):
            self.finished.connect(finished)

        return self

    def temp_hide(self, duration: int = 500, finished: callable = None):
        """
        Hide widget from right to left
        :param duration: int
        :param finished: callable
        :return: QPropertyAnimation
        """

        self.setDuration(duration)
        self.setStartValue(self._target.width())
        self.setEndValue(0)

        if callable(finished):
            self.finished.connect(finished)

        return self


class QuickShadow(QGraphicsDropShadowEffect):
    def __init__(
            self, parent=None, color: QColor = QColor(0, 0, 0, 150), radius: int = 5, offset: int = 3
    ):
        super(QuickShadow, self).__init__(parent=parent)

        self.setBlurRadius(radius)
        self.setOffset(offset)
        self.setColor(color)


class QuickWidget(QWidget):
    def __init__(
            self, parent=None,
            fixed_size: QSize = None,
            fixed_width: int = None,
            fixed_height: int = None,
            value_changed: callable = None,
            start_value: object = None,
            end_value: object = None,
            duration: int = 300
    ):
        super(QuickWidget, self).__init__(parent)

        if fixed_size:
            self.setFixedSize(fixed_size)
        else:
            if fixed_width:
                self.setFixedWidth(fixed_width)
            if fixed_height:
                self.setFixedHeight(fixed_height)

        if callable(value_changed) and start_value and end_value:
            self.__animation = QVariantAnimation(self)
            self.__animation.valueChanged.connect(value_changed)
            self.__animation.setStartValue(start_value)
            self.__animation.setEndValue(end_value)
            self.__animation.setDuration(duration)
        else:
            self.__animation = None

    def enterEvent(self, event):
        super(QuickWidget, self).enterEvent(event)

        if self.__animation:
            self.__animation.setDirection(QAbstractAnimation.Forward)
            self.__animation.start()

    def leaveEvent(self, event):
        super(QuickWidget, self).leaveEvent(event)

        if self.__animation:
            self.__animation.setDirection(QAbstractAnimation.Backward)
            self.__animation.start()


class QuickMainWidget(QWidget):
    def __init__(
            self, parent=None,
            shadow: QGraphicsDropShadowEffect = QuickShadow(),
            padding: int = 11,
            fixed_size: QSize = None,
            fixed_width: int = None,
            fixed_height: int = None
    ):
        super(QuickMainWidget, self).__init__(parent)

        self.setLayout(QGridLayout())
        self.layout().setContentsMargins(padding, padding, padding, padding)

        self.shadowWidget = QWidget(self, flags=Qt.SubWindow)
        self.shadowWidget.setGraphicsEffect(shadow)
        self.shadowWidget.setObjectName('shadowWidget')

        self.mainWidget = QWidget(self, flags=Qt.SubWindow)
        self.mainWidget.setObjectName('mainWidget')

        self.layout().addWidget(self.shadowWidget, 0, 0, 1, 1)
        self.layout().addWidget(self.mainWidget, 0, 0, 1, 1)

        if fixed_size:
            self.setFixedSize(fixed_size)
        elif fixed_width or fixed_height:
            if fixed_width:
                self.setFixedWidth(fixed_width)
            if fixed_height:
                self.setFixedHeight(fixed_height)
        else:
            self.sizeGrip = QSizeGrip(self)
            self.sizeGrip.setFixedSize(QSize(24, 24))
            self.layout().addWidget(self.sizeGrip, 0, 0, 1, 1, Qt.AlignBottom | Qt.AlignRight)


class QuickDialog(QDialog):
    def __init__(
            self, parent=None,
            shadow: QGraphicsDropShadowEffect = QuickShadow(),
            padding: int = 11,
            fixed_size: QSize = None,
            fixed_width: int = None,
            fixed_height: int = None
    ):
        super(QuickDialog, self).__init__(parent)

        self.setLayout(QGridLayout())
        self.layout().setContentsMargins(padding, padding, padding, padding)

        self.shadowWidget = QWidget(self, flags=Qt.SubWindow)
        self.shadowWidget.setGraphicsEffect(shadow)
        self.shadowWidget.setObjectName('shadowWidget')

        self.mainWidget = QWidget(self, flags=Qt.SubWindow)
        self.mainWidget.setObjectName('mainWidget')

        self.layout().addWidget(self.shadowWidget, 0, 0, 1, 1)
        self.layout().addWidget(self.mainWidget, 0, 0, 1, 1)

        if fixed_size:
            self.setFixedSize(fixed_size)
        elif fixed_width or fixed_height:
            if fixed_width:
                self.setFixedWidth(fixed_width)
            if fixed_height:
                self.setFixedHeight(fixed_height)
        else:
            self.sizeGrip = QSizeGrip(self)
            self.sizeGrip.setFixedSize(QSize(24, 24))
            self.layout().addWidget(self.sizeGrip, 0, 0, 1, 1, Qt.AlignBottom | Qt.AlignRight)


class QuickLineEdit(QLineEdit):
    def __init__(
            self, parent=None,
            text: str = None,
            placeholder_text: str = None,
            numeric: bool = False,
            writable: bool = True,
            mode: QLineEdit.EchoMode = None,
            align: Qt.AlignmentFlag = None,
            fixed_size: QSize = None,
            fixed_width: int = None,
            fixed_height: int = None,
            layout_support: bool = False,
            length: int = 64,
            value_changed: callable = None,
            start_value: object = None,
            end_value: object = None,
            duration: int = 300
    ):
        super(QuickLineEdit, self).__init__(parent)
        self.setContextMenuPolicy(Qt.NoContextMenu)

        if text:
            self.setText(text)

        if placeholder_text:
            self.setPlaceholderText(placeholder_text)

        if writable:
            self.setMaxLength(length)
            if numeric:
                self.setValidator(QRegExpValidator(QRegExp('[0-9]{%s}' % length)))
        else:
            self.setReadOnly(True)

        if mode:
            self.setEchoMode(mode)

        if align:
            self.setAlignment(align)

        if fixed_size:
            self.setFixedSize(fixed_size)
        else:
            if fixed_width:
                self.setFixedWidth(fixed_width)
            if fixed_height:
                self.setFixedHeight(fixed_height)

        if layout_support:
            self.setLayout(QHBoxLayout())
            self.layout().setContentsMargins(10, 0, 10, 0)
            self.layout().setSpacing(0)

        if callable(value_changed) and start_value and end_value:
            self.__animation = QVariantAnimation(self)
            self.__animation.valueChanged.connect(value_changed)
            self.__animation.setStartValue(start_value)
            self.__animation.setEndValue(end_value)
            self.__animation.setDuration(duration)
        else:
            self.__animation = None

    def enterEvent(self, event):
        super(QuickLineEdit, self).enterEvent(event)

        if self.__animation:
            self.__animation.setDirection(QAbstractAnimation.Forward)
            self.__animation.start()

    def leaveEvent(self, event):
        super(QuickLineEdit, self).leaveEvent(event)

        if self.__animation:
            self.__animation.setDirection(QAbstractAnimation.Backward)
            self.__animation.start()


class QuickLabel(QLabel):
    def __init__(
            self, parent=None,
            text: str = None,
            linkable: bool = False,
            scaled: bool = False,
            font_size: int = None,
            fixed_width: int = None,
            fixed_height: int = None,
            fixed_size: QSize = None,
            pixmap: QPixmap = None,
            align: Qt.AlignmentFlag = None,
            value_changed: callable = None,
            start_value: object = None,
            end_value: object = None,
            duration: int = 300
    ):
        super(QuickLabel, self).__init__(parent)
        self.setWordWrap(True)

        if linkable:
            self.setOpenExternalLinks(True)
            if text:
                syntax = f'<a href="%s" style="text-decoration: underline; color:{_Color.FONT};">%s</a>'
                self.setText(syntax % (text, text))
        elif text:
            self.setText(text)

        if font_size:
            font = self.font()
            font.setPointSize(font_size)
            self.setFont(font)

        if fixed_size:
            self.setFixedSize(fixed_size)
        else:
            if fixed_width:
                self.setFixedWidth(fixed_width)
            if fixed_height:
                self.setFixedHeight(fixed_height)

        if pixmap:
            self.setPixmap(pixmap)
            self.setScaledContents(scaled)

        if align:
            self.setAlignment(align)

        if callable(value_changed) and start_value and end_value:
            self.__animation = QVariantAnimation(self)
            self.__animation.valueChanged.connect(value_changed)
            self.__animation.setStartValue(start_value)
            self.__animation.setEndValue(end_value)
            self.__animation.setDuration(duration)
        else:
            self.__animation = None

    def enterEvent(self, event):
        super(QuickLabel, self).enterEvent(event)

        if self.__animation:
            self.__animation.setDirection(QAbstractAnimation.Forward)
            self.__animation.start()

    def leaveEvent(self, event):
        super(QuickLabel, self).leaveEvent(event)

        if self.__animation:
            self.__animation.setDirection(QAbstractAnimation.Backward)
            self.__animation.start()


class QuickPushButton(QPushButton):
    def __init__(
            self, parent=None,
            text: str = None,
            icon: QIcon = None,
            icon_size: QSize = None,
            fixed_size: QSize = None,
            fixed_width: int = None,
            fixed_height: int = None,
            font_size: int = None,
            value_changed: callable = None,
            start_value: object = None,
            end_value: object = None,
            duration: int = 300,
            cursor: Qt.CursorShape = None
    ):
        super(QuickPushButton, self).__init__(parent)
        self.setFocusPolicy(Qt.NoFocus)

        if text:
            self.setText(text)

        if icon:
            self.setIcon(icon)
            if icon_size:
                self.setIconSize(icon_size)

        if fixed_size:
            self.setFixedSize(fixed_size)
        else:
            if fixed_width:
                self.setFixedWidth(fixed_width)
            if fixed_height:
                self.setFixedHeight(fixed_height)

        if font_size:
            font = self.font()
            font.setPointSize(font_size)
            self.setFont(font)

        if cursor:
            self.setCursor(cursor)

        if callable(value_changed) and start_value and end_value:
            self.__animation = QVariantAnimation(self)
            self.__animation.valueChanged.connect(value_changed)
            self.__animation.setStartValue(start_value)
            self.__animation.setEndValue(end_value)
            self.__animation.setDuration(duration)
        else:
            self.__animation = None

    def enterEvent(self, event):
        super(QuickPushButton, self).enterEvent(event)

        if self.__animation:
            self.__animation.setDirection(QAbstractAnimation.Forward)
            self.__animation.start()

    def leaveEvent(self, event):
        super(QuickPushButton, self).leaveEvent(event)

        if self.__animation:
            self.__animation.setDirection(QAbstractAnimation.Backward)
            self.__animation.start()


class QuickRadioButton(QRadioButton):
    def __init__(
            self, parent=None,
            text: str = None,
            icon: QIcon = None,
            icon_size: QSize = None,
            fixed_size: QSize = None,
            fixed_width: int = None,
            fixed_height: int = None,
            font_size: int = None,
            checked: bool = False,
            value_changed: callable = None,
            start_value: object = None,
            end_value: object = None,
            duration: int = 300,
            cursor: Qt.CursorShape = None
    ):
        super(QuickRadioButton, self).__init__(parent)
        self.setFocusPolicy(Qt.NoFocus)

        if text:
            self.setText(text)

        if icon:
            self.setIcon(icon)
            if icon_size:
                self.setIconSize(icon_size)

        if fixed_size:
            self.setFixedSize(fixed_size)
        else:
            if fixed_width:
                self.setFixedWidth(fixed_width)
            if fixed_height:
                self.setFixedHeight(fixed_height)

        if font_size:
            font = self.font()
            font.setPointSize(font_size)
            self.setFont(font)

        if checked:
            self.setChecked(True)

        if cursor:
            self.setCursor(cursor)

        if callable(value_changed) and start_value and end_value:
            self.__animation = QVariantAnimation(self)
            self.__animation.valueChanged.connect(value_changed)
            self.__animation.setStartValue(start_value)
            self.__animation.setEndValue(end_value)
            self.__animation.setDuration(duration)
        else:
            self.__animation = None

    def enterEvent(self, event):
        super(QuickRadioButton, self).enterEvent(event)

        if self.__animation:
            self.__animation.setDirection(QAbstractAnimation.Forward)
            self.__animation.start()

    def leaveEvent(self, event):
        super(QuickRadioButton, self).leaveEvent(event)

        if self.__animation:
            self.__animation.setDirection(QAbstractAnimation.Backward)
            self.__animation.start()


class QuickCheckBox(QCheckBox):
    def __init__(
            self, parent=None,
            text: str = None,
            icon: QIcon = None,
            icon_size: QSize = None,
            fixed_size: QSize = None,
            fixed_width: int = None,
            fixed_height: int = None,
            font_size: int = None,
            checkable: bool = True,
            checked: bool = False,
            value_changed: callable = None,
            start_value: object = None,
            end_value: object = None,
            duration: int = 300,
            cursor: Qt.CursorShape = None
    ):
        super(QuickCheckBox, self).__init__(parent)
        self.setFocusPolicy(Qt.NoFocus)
        self.setCheckable(checkable)

        if text:
            self.setText(text)

        if icon:
            self.setIcon(icon)
            if icon_size:
                self.setIconSize(icon_size)

        if fixed_size:
            self.setFixedSize(fixed_size)
        else:
            if fixed_width:
                self.setFixedWidth(fixed_width)
            if fixed_height:
                self.setFixedHeight(fixed_height)

        if font_size:
            font = self.font()
            font.setPointSize(font_size)
            self.setFont(font)

        if checkable and checked:
            self.setChecked(True)

        if cursor:
            self.setCursor(cursor)

        if callable(value_changed) and start_value and end_value:
            self.__animation = QVariantAnimation(self)
            self.__animation.valueChanged.connect(value_changed)
            self.__animation.setStartValue(start_value)
            self.__animation.setEndValue(end_value)
            self.__animation.setDuration(duration)
        else:
            self.__animation = None

    def enterEvent(self, event):
        super(QuickCheckBox, self).enterEvent(event)

        if self.__animation:
            self.__animation.setDirection(QAbstractAnimation.Forward)
            self.__animation.start()

    def leaveEvent(self, event):
        super(QuickCheckBox, self).leaveEvent(event)

        if self.__animation:
            self.__animation.setDirection(QAbstractAnimation.Backward)
            self.__animation.start()


class QuickDateEdit(QDateEdit):
    def __init__(
            self, parent=None,
            text: str = None,
            writable: bool = True,
            scrollable: bool = True,
            align: Qt.AlignmentFlag = None,
            fixed_size: QSize = None,
            fixed_width: int = None,
            fixed_height: int = None,
            font_size: int = None,
            value_changed: callable = None,
            start_value: object = None,
            end_value: object = None,
            duration: int = 300,
            cursor: Qt.CursorShape = None
    ):
        super(QuickDateEdit, self).__init__(parent)
        self.setContextMenuPolicy(Qt.NoContextMenu)
        self.setCalendarPopup(True)
        self.setDisplayFormat('yyyy-MM-dd')

        if not text:
            text = f'{QDate().currentDate().year()}-01-01'
        self.setDate(QDate().fromString(text, 'yyyy-MM-dd'))

        if not writable:
            self.setReadOnly(True)
        elif not scrollable:
            self.installEventFilter(self)

        if align:
            self.setAlignment(align)

        if fixed_size:
            self.setFixedSize(fixed_size)
        else:
            if fixed_width:
                self.setFixedWidth(fixed_width)
            if fixed_height:
                self.setFixedHeight(fixed_height)

        if font_size:
            font = self.font()
            font.setPointSize(font_size)
            self.setFont(font)

        if cursor:
            self.setCursor(cursor)

        if callable(value_changed) and start_value and end_value:
            self.__animation = QVariantAnimation(self)
            self.__animation.valueChanged.connect(value_changed)
            self.__animation.setStartValue(start_value)
            self.__animation.setEndValue(end_value)
            self.__animation.setDuration(duration)
        else:
            self.__animation = None

    def enterEvent(self, event):
        super(QuickDateEdit, self).enterEvent(event)

        if self.__animation:
            self.__animation.setDirection(QAbstractAnimation.Forward)
            self.__animation.start()

    def leaveEvent(self, event):
        super(QuickDateEdit, self).leaveEvent(event)

        if self.__animation:
            self.__animation.setDirection(QAbstractAnimation.Backward)
            self.__animation.start()

    def eventFilter(self, source, event):
        if event.type() == QEvent.Wheel:
            return True
        return super(QuickDateEdit, self).eventFilter(source, event)


class QuickGroupBox(QGroupBox):
    def __init__(
            self, parent=None,
            text: str = None,
            align: Qt.AlignmentFlag = None,
            fixed_size: QSize = None,
            fixed_width: int = None,
            fixed_height: int = None,
            font_size: int = None,
            checkable: bool = False,
            checked: bool = False,
            value_changed: callable = None,
            start_value: object = None,
            end_value: object = None,
            duration: int = 300
    ):
        super(QuickGroupBox, self).__init__(parent)

        if text:
            self.setText(text)

        if align:
            self.setAlignment(align)

        if fixed_size:
            self.setFixedSize(fixed_size)
        else:
            if fixed_width:
                self.setFixedWidth(fixed_width)
            if fixed_height:
                self.setFixedHeight(fixed_height)

        if font_size:
            font = self.font()
            font.setPointSize(font_size)
            self.setFont(font)

        if checkable:
            self.setCheckable(True)
            self.setChecked(checked)

        if callable(value_changed) and start_value and end_value:
            self.__animation = QVariantAnimation(self)
            self.__animation.valueChanged.connect(value_changed)
            self.__animation.setStartValue(start_value)
            self.__animation.setEndValue(end_value)
            self.__animation.setDuration(duration)
        else:
            self.__animation = None

    def enterEvent(self, event):
        super(QuickGroupBox, self).enterEvent(event)

        if self.__animation:
            self.__animation.setDirection(QAbstractAnimation.Forward)
            self.__animation.start()

    def leaveEvent(self, event):
        super(QuickGroupBox, self).leaveEvent(event)

        if self.__animation:
            self.__animation.setDirection(QAbstractAnimation.Backward)
            self.__animation.start()


class QuickComboBox(QComboBox):
    def __init__(
            self, parent=None,
            items: list = None,
            editable: bool = False,
            current_text: str = None,
            current_index: int = None,
            max_visible_items: int = None,
            max_count: int = None,
            icon_size: QSize = None,
            fixed_size: QSize = None,
            fixed_width: int = None,
            fixed_height: int = None,
            font_size: int = None,
            value_changed: callable = None,
            start_value: object = None,
            end_value: object = None,
            duration: int = 300,
            cursor: Qt.CursorShape = None
    ):
        super(QuickComboBox, self).__init__(parent)
        self.setFocusPolicy(Qt.NoFocus)
        combobox_style(self)

        if items:
            self.addItems(items)

        if editable:
            self.setEditable(True)

        if current_text:
            self.setCurrentText(current_text)

        if current_index:
            self.setCurrentIndex(current_index)

        if max_visible_items:
            self.setMaxVisibleItems(max_visible_items)

        if max_count:
            self.setMaxCount(max_count)

        if icon_size:
            self.setIconSize(icon_size)

        if fixed_size:
            self.setFixedSize(fixed_size)
        else:
            if fixed_width:
                self.setFixedWidth(fixed_width)
            if fixed_height:
                self.setFixedHeight(fixed_height)

        if font_size:
            font = self.font()
            font.setPointSize(font_size)
            self.setFont(font)

        if cursor:
            self.setCursor(cursor)

        if callable(value_changed) and start_value and end_value:
            self.__animation = QVariantAnimation(self)
            self.__animation.valueChanged.connect(value_changed)
            self.__animation.setStartValue(start_value)
            self.__animation.setEndValue(end_value)
            self.__animation.setDuration(duration)
        else:
            self.__animation = None

    def enterEvent(self, event):
        super(QuickComboBox, self).enterEvent(event)

        if self.__animation:
            self.__animation.setDirection(QAbstractAnimation.Forward)
            self.__animation.start()

    def leaveEvent(self, event):
        super(QuickComboBox, self).leaveEvent(event)

        if self.__animation:
            self.__animation.setDirection(QAbstractAnimation.Backward)
            self.__animation.start()


class QuickNotification(QListWidget):
    class _NotificationObject(QGroupBox):
        def __init__(
                self, icon: str, text: str, font_size: int, color: str,
                item: QListWidgetItem, timeout: int, finished: callable
        ):
            QGroupBox.__init__(self)

            self.setLayout(QHBoxLayout())
            self.layout().setContentsMargins(9, 0, 9, 0)

            label_icon = QuickLabel(
                self, scaled=True, fixed_size=_SIZE25,
                pixmap=QPixmap(icon), align=Qt.AlignCenter
            )

            label_text = QuickLabel(self, text, font_size=font_size)
            if color:
                label_text.setStyleSheet('color: %s' % color)

            self.layout().addWidget(label_icon)
            self.layout().addWidget(label_text, True)

            self.item = item
            self.timeout = timeout
            self.finished = finished
            self.animation = OpacityMotion(self, Property.OPACITY)

        def showEvent(self, event):
            self.animation.temp_show(
                finished=lambda: QTimer().singleShot(self.timeout, self.close)
            ).start()

        def closeEvent(self, event):
            wait = QEventLoop()
            self.animation.finished.disconnect()
            self.animation.temp_hide(finished=wait.quit).start()
            wait.exec_()

            parent = self.parent().parent()
            index = parent.row(self.item)
            parent.removeItemWidget(self.item)
            parent.takeItem(index)

            if not parent.count():
                parent.hide()

            if callable(self.finished):
                self.finished()

    def __init__(
            self, parent, size: QSize = QSize(321, 51), stylesheet: str = '',
            top_margin: int = 31, right_margin: int = 31, bottom_margin: int = 31
    ):
        super(QuickNotification, self).__init__(parent)

        self.setStyleSheet('QWidget, QListWidget::item:hover {background: transparent; border: 0px}')
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setSpacing(18)
        self.hide()

        self.__itemSize = size
        self.__topMargin = top_margin
        self.__rightMargin = right_margin
        self.__bottomMargin = bottom_margin
        self.__style = stylesheet

    def create_new(
            self, icon: str, text: str, font_size: int = None, color: str = None,
            timeout: int = 1500, finished: callable = None
    ):
        if not self.count():
            x = self.parent().width() - self.__itemSize.width() - self.__rightMargin
            y = self.__topMargin
            width = self.__itemSize.width()
            height = self.parent().height() - self.__bottomMargin

            self.setGeometry(QRect(x, y, width, height))
            self.show()

        item = QListWidgetItem(self)
        frame = self._NotificationObject(icon, text, font_size, color, item, timeout, finished)
        frame.setLayoutDirection(LAYOUT_DIRECTION)
        frame.setStyleSheet(self.__style)
        frame.setFixedHeight(self.__itemSize.height())

        self.addItem(item)
        self.setItemWidget(item, frame)

    def information(
            self, text: str, font_size: int = None, timeout: int = 1500, finished: callable = None
    ):
        self.create_new(_Icon.INFORMATION, text, font_size, _Color.INFORMATION, timeout, finished)

    def warning(
            self, text: str, font_size: int = None, timeout: int = 1500, finished: callable = None
    ):
        self.create_new(_Icon.WARNING, text, font_size, _Color.WARNING, timeout, finished)

    def successfully(
            self, text: str, font_size: int = None, timeout: int = 1500, finished: callable = None
    ):
        self.create_new(_Icon.SUCCESS, text, font_size, _Color.SUCCESS, timeout, finished)

    def failed(
            self, text: str, font_size: int = None, timeout: int = 1500, finished: callable = None
    ):
        self.create_new(_Icon.FAILED, text, font_size, _Color.FAILED, timeout, finished)


class QLoadingEffect(QWidget):
    def __init__(
            self, parent=None, duration: float = 300, count: int = 4,
            color: str = '#9557FC', light_color: str = '#FF7676'
    ):
        super(QLoadingEffect, self).__init__(parent, flags=Qt.SubWindow)

        self.__duration = duration
        self.__count = count
        self.__color = color
        self.__light_color = light_color
        self.__points = []
        self.__currentPoint = 0
        self.__animation = None
        self.__ui()

    @property
    def __stylesheet(self):
        """
        Get stylesheet value
        :return: str
        """

        return '''
        QGroupBox {
            background: transparent;
            border: 0px;
        }
        QLabel {
            border-radius: 10px;
            background-color: %s;
        }
        QLabel::disabled {
            background-color: %s;
        }''' % (self.__light_color, self.__color)

    def __ui(self):
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setStyleSheet(self.__stylesheet)

        self.groupBox = QGroupBox(self)
        self.groupBox.setLayout(QHBoxLayout())

        for _ in range(self.__count):
            label = QLabel(self)
            label.setFixedSize(_SIZE21)
            label.setDisabled(True)
            self.groupBox.layout().addWidget(label, alignment=Qt.AlignCenter)
            self.__points.append(label)

        self.__timer = QTimer()
        self.__timer.timeout.connect(self.__next)

        self.setFixedSize(self.groupBox.sizeHint())
        self.hide()

    def __next(self):
        if self.__currentPoint:
            self.__points[self.__currentPoint - 1].setDisabled(True)
        else:
            self.__points[-1].setDisabled(True)

        self.__points[self.__currentPoint].setEnabled(True)

        if self.__currentPoint == self.__count - 1:
            self.__currentPoint = 0
        else:
            self.__currentPoint += 1

    def start(self):
        self.__animation = GeometryMotion(self.groupBox)
        self.__animation.temp_open(
            width=self.width(), finished=lambda: self.__timer.start(self.__duration)
        ).start()
        self.show()

    def stop(self):
        self.__timer.stop()
        self.__animation = GeometryMotion(self.groupBox)
        self.__animation.temp_close(duration=500, finished=self.close).start()


class QMarkNotify(QWidget):
    def __init__(self, parent):
        super(QMarkNotify, self).__init__(parent, flags=Qt.SubWindow)

        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setFixedSize(QSize(10, 10))
        super(QMarkNotify, self).hide()

        self.__animation = OpacityMotion(self, Property.OPACITY)
        self.__animation.temp_show(1000, self.__backward)

    def show(self):
        super(QMarkNotify, self).show()

        self.__animation.start()

    def hide(self):
        self.__animation.stop()

        super(QMarkNotify, self).hide()

    def __forward(self):
        self.__animation.setDirection(QPropertyAnimation.Forward)
        self.__animation.finished.disconnect()
        self.__animation.finished.connect(self.__backward)
        self.__animation.start()

    def __backward(self):
        self.__animation.setDirection(QPropertyAnimation.Backward)
        self.__animation.finished.disconnect()
        self.__animation.finished.connect(self.__forward)
        self.__animation.start()


class QBorderBottom(QWidget):
    def __init__(self, parent):
        super(QBorderBottom, self).__init__(parent, flags=Qt.SubWindow)

        self.setAttribute(Qt.WA_StyledBackground, True)
        self.__animation = GeometryMotion(self)

    def move_to_x(self, x: int):
        self.__animation.temp_x(end_x=x, duration=200)
        self.__animation.start()


class QSwitch(QAbstractButton):
    def __init__(self, parent=None, track_radius=10, thumb_radius=8):
        super(QSwitch, self).__init__(parent=parent)

        self.setCheckable(True)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setFocusPolicy(Qt.NoFocus)
        self.setCursor(Qt.PointingHandCursor)

        self._track_radius = track_radius
        self._thumb_radius = thumb_radius

        self._margin = max(0, self._thumb_radius - self._track_radius)
        self._base_offset = max(self._thumb_radius, self._track_radius)
        self._end_offset = {
            True: lambda: self.width() - self._base_offset,
            False: lambda: self._base_offset,
        }
        self._offset = self._base_offset

        palette = self.palette()
        if self._thumb_radius > self._track_radius:
            self._track_color = {
                True: palette.highlight(),
                False: palette.dark(),
            }
            self._thumb_color = {
                True: palette.highlight(),
                False: palette.light(),
            }
            self._track_opacity = 0.5
        else:
            self._thumb_color = {
                True: palette.highlightedText(),
                False: palette.light(),
            }
            self._track_color = {
                True: palette.highlight(),
                False: palette.dark(),
            }
            self._track_opacity = 1

    @pyqtProperty(int)
    def offset(self):
        return self._offset

    @offset.setter
    def offset(self, value):
        self._offset = value
        self.update()

    def sizeHint(self):
        return QSize(
            4 * self._track_radius + 2 * self._margin,
            2 * self._track_radius + 2 * self._margin,
        )

    def setChecked(self, checked):
        super(QSwitch, self).setChecked(checked)
        self.offset = self._end_offset[checked]()

    def resizeEvent(self, event):
        super(QSwitch, self).resizeEvent(event)
        self.offset = self._end_offset[self.isChecked()]()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)
        p.setPen(Qt.NoPen)

        track_opacity = self._track_opacity
        thumb_opacity = 1.0
        if self.isEnabled():
            track_brush = self._track_color[self.isChecked()]
            thumb_brush = self._thumb_color[self.isChecked()]
        else:
            track_opacity *= 0.8
            track_brush = self.palette().shadow()
            thumb_brush = self.palette().mid()

        p.setBrush(track_brush)
        p.setOpacity(track_opacity)
        p.drawRoundedRect(
            self._margin,
            self._margin,
            self.width() - 2 * self._margin,
            self.height() - 2 * self._margin,
            self._track_radius,
            self._track_radius,
        )
        p.setBrush(thumb_brush)
        p.setOpacity(thumb_opacity)
        p.drawEllipse(
            self.offset - self._thumb_radius,
            self._base_offset - self._thumb_radius,
            2 * self._thumb_radius,
            2 * self._thumb_radius,
        )

    def mouseReleaseEvent(self, event):
        super(QSwitch, self).mouseReleaseEvent(event)
        if event.button() == Qt.LeftButton:
            animation = QPropertyAnimation(self, b'offset', self)
            animation.setDuration(200)
            animation.setStartValue(self.offset)
            animation.setEndValue(self._end_offset[self.isChecked()]())
            animation.start()


class _MessageBoxKernel(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent=parent, flags=_FLAGS)
        self.clickedOn = Button.CLOSE
        self.issue = None

        self.__clickPressedX = None
        self.__clickPressedY = None
        self.__leftClickPressed = False
        self.__ui()

        self.__opacity = OpacityMotion(self, Property.WINDOW_OPACITY)
        self.__opacityMessage = OpacityMotion(self.groupBoxContent, Property.OPACITY)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            event.ignore()
            if self.pushButtonClose.isVisible():
                self.close()

    def mousePressEvent(self, event):
        super(_MessageBoxKernel, self).mousePressEvent(event)
        if event.button() == Qt.LeftButton and self.underMouse():
            self.__leftClickPressed = True
            self.__clickPressedX = event.pos().x()
            self.__clickPressedY = event.pos().y()

    def mouseReleaseEvent(self, event):
        super(_MessageBoxKernel, self).mouseReleaseEvent(event)
        self.__leftClickPressed = False

    def mouseMoveEvent(self, event):
        super(_MessageBoxKernel, self).mouseMoveEvent(event)
        if self.__leftClickPressed:
            x = event.globalPos().x() - self.__clickPressedX
            y = event.globalPos().y() - self.__clickPressedY
            self.move(x, y)

    def exec_(self):
        """Display message box"""

        self.__opacity.temp_show(duration=700).start()
        super(_MessageBoxKernel, self).exec_()

    def close(self):
        """Close message box"""

        self.__opacity.temp_hide(
            duration=400, finished=lambda: super(_MessageBoxKernel, self).close()
        ).start()

    def success(self, text: str = None, close: bool = True):
        """Success animation template"""

        self.content_update(text, _Icon.SUCCESS, _Color.SUCCESS, close)

    def failed(self, text: str = None, close: bool = True):
        """Failed animation template"""

        self.content_update(text, _Icon.FAILED, _Color.FAILED, close)

    def warning(self, text: str = None, close: bool = True):
        """Warning animation template"""

        self.content_update(text, _Icon.WARNING, _Color.WARNING, close)

    def content_update(
            self, text: str = None, icon: str = None, color: str = None, close: bool = False
    ):
        """Content update values"""

        self.__opacityMessage.temp_hide(
            300, lambda: self.__content_updating(text, icon, color, close)
        ).start()

    def __content_updating(self, text: str, icon: str, color: str, close: bool):
        self.__opacityMessage.finished.disconnect()
        self.__opacityMessage.temp_show(500, lambda: self.__content_updated(close))

        if icon:
            self.labelMessage.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            self.labelIcon.setPixmap(QPixmap(icon))
            self.labelIcon.show()
        elif icon == '':
            self.labelMessage.setAlignment(Qt.AlignCenter)
            self.labelIcon.hide()

        if color:
            self.labelMessage.setStyleSheet('color: %s;' % color)

        if text:
            self.labelMessage.setText(text)
            self.labelMessage.show()
        else:
            self.labelMessage.hide()

        self.__opacityMessage.start()

    def __content_updated(self, close: bool):
        self.__opacityMessage.finished.disconnect()
        if close:
            self.close()

    def __ui(self):
        self.setWindowTitle(_WINDOW_TITLE)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WA_DeleteOnClose, True)

        self.__frame = QFrame(self, flags=Qt.SubWindow)
        self.__frame.setStyleSheet(_STYLESHEET)

        self.frame = QFrame(self, flags=Qt.SubWindow)
        self.frame.setStyleSheet(_STYLESHEET)
        self.frame.setFocusPolicy(Qt.ClickFocus)
        self.frame.setLayout(QVBoxLayout())
        self.frame.setObjectName('frame')

        self.labelTitle = QuickLabel(
            self.frame, _TITLE_TEXT, fixed_size=QSize(221, 31), align=Qt.AlignCenter
        )
        self.labelTitle.setFont(_TITLE_FONT)
        self.labelTitle.setLayout(QHBoxLayout())
        self.labelTitle.layout().setContentsMargins(3, 0, 3, 0)
        self.labelTitle.setObjectName('labelTitle')

        self.pushButtonClose = QuickPushButton(
            self.frame, icon=QIcon(_Icon.CLOSE), icon_size=_SIZE21,
            fixed_size=_SIZE25, cursor=Qt.PointingHandCursor
        )
        self.pushButtonClose.setObjectName('pushButtonClose')

        self.groupBoxContent = QGroupBox(self.frame)
        self.groupBoxContent.setLayout(QHBoxLayout())
        self.groupBoxContent.layout().setContentsMargins(0, 0, 0, 0)
        self.groupBoxContent.setLayoutDirection(LAYOUT_DIRECTION)
        self.groupBoxContent.setObjectName('groupBoxContent')

        self.labelIcon = QLabel(self.frame)
        self.labelIcon.setStyleSheet('padding-left: 16px;')
        self.labelIcon.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred))
        self.labelIcon.setObjectName('labelIcon')

        self.labelMessage = QuickLabel(self.frame, linkable=True)
        self.labelMessage.setObjectName('labelMessage')

        self.labelTitle.layout().addWidget(self.pushButtonClose, alignment=Qt.AlignRight)
        self.groupBoxContent.layout().addWidget(self.labelIcon, True)
        self.groupBoxContent.layout().addWidget(self.labelMessage, True)
        self.frame.layout().addWidget(self.labelTitle, alignment=Qt.AlignTop | Qt.AlignHCenter)
        self.frame.layout().addWidget(self.groupBoxContent, True)

        self.pushButtonClose.clicked.connect(self.__close_click)

    @pyqtSlot()
    def __close_click(self):
        self.clickedOn = Button.CLOSE
        self.close()

    def _set(self, window_size: QSize, icon: str, text: str, font_size: int, color: str):
        self.resize(window_size.width() + 41, window_size.height() + 41)

        self.__frame.setFixedSize(window_size)
        self.__frame.move(20, 20)
        self.__frame.setGraphicsEffect(QuickShadow(self, radius=15, offset=0))

        self.frame.setFixedSize(window_size)
        self.frame.move(20, 20)

        self.labelMessage.setText(text)
        self.labelMessage.setStyleSheet('color: %s;' % color)

        if icon:
            self.labelIcon.setPixmap(QPixmap(icon))
        else:
            self.labelMessage.setAlignment(Qt.AlignCenter)
            self.labelIcon.hide()

        if font_size:
            font = QFont()
            font.setPointSize(font_size)
            self.labelMessage.setFont(font)


class _MessageBoxPasswordKernel(_MessageBoxKernel):
    def __init__(self, parent=None):
        super(_MessageBoxPasswordKernel, self).__init__(parent)

        self.groupBox = QGroupBox(self.frame)
        self.groupBox.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed))
        self.groupBox.setLayout(QGridLayout())
        self.groupBox.layout().setContentsMargins(0, 0, 0, 0)

        self.lineEdit = QuickLineEdit(
            self.frame, placeholder_text=_TRANSLATOR('Form', LINE_EDIT_PLACEHOLDER),
            mode=QLineEdit.Password, fixed_height=41
        )
        self.lineEdit.setFocusPolicy(Qt.ClickFocus)
        self.lineEdit.setObjectName('lineEdit')

        self.pushButtonEye = QuickPushButton(
            self.frame, icon=QIcon(_Icon.EYE_SHOW), icon_size=_SIZE21,
            fixed_size=_SIZE41, cursor=Qt.PointingHandCursor
        )
        self.pushButtonEye.setObjectName('pushButtonEye')

        self.pushButtonAccept = QuickPushButton(
            self.frame, icon=QIcon(_Icon.ENTER), icon_size=_SIZE21,
            fixed_size=_SIZE41, cursor=Qt.PointingHandCursor
        )
        self.pushButtonAccept.setObjectName('pushButtonAccept')

        self.strengthBar = SPInputmanager.QStrengthBar(self.frame)
        self.strengthBar.setTextHidden(True)

        self.frame.layout().addWidget(self.groupBox, True)
        self.groupBox.layout().addWidget(self.lineEdit, 0, 0, 1, 1)
        self.groupBox.layout().addWidget(self.pushButtonEye, 0, 1, 1, 1)
        self.groupBox.layout().addWidget(self.pushButtonAccept, 0, 2, 1, 1)
        self.groupBox.layout().addWidget(self.strengthBar, 1, 0, 1, 1)

        self.nptManager = SPInputmanager.InputManager(self.lineEdit)
        self.nptManager.eye_connect(self.pushButtonEye)
        self.nptManager.strength_bar_connect(self.strengthBar)

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            self.pushButtonAccept.click()


class MessageBox(_MessageBoxKernel):
    def __init__(
            self, parent, text: str, icon: str = None, font_size: int = None,
            color: str = _Color.FONT, window_size: QSize = _WINDOW_SIZE
    ):
        """Simple message display"""

        super(MessageBox, self).__init__(parent)
        self._set(window_size, icon, text, font_size, color)


class MessageBoxConfirm(_MessageBoxKernel):
    def __init__(
            self, parent, text: str, icon: str = None, font_size: int = None,
            color: str = _Color.FONT, accept: str = "Accept",
            cancel: str = "Cancel", window_size: QSize = _WINDOW_SIZE
    ):
        """Message confirmation with buttons"""

        super(MessageBoxConfirm, self).__init__(parent)
        self._set(window_size, icon, text, font_size, color)

        self.groupBox = QGroupBox(self.frame)
        self.groupBox.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed))
        self.groupBox.setLayout(QGridLayout())
        self.groupBox.layout().setContentsMargins(0, 0, 0, 0)
        self.groupBox.setObjectName('groupBox')

        self.pushButtonAccept = QuickPushButton(
            self.frame, _TRANSLATOR('Form', accept), fixed_height=41, cursor=Qt.PointingHandCursor
        )
        self.pushButtonAccept.setObjectName('pushButtonAccept')

        self.pushButtonCancel = QuickPushButton(
            self.frame, _TRANSLATOR('Form', cancel), fixed_height=41, cursor=Qt.PointingHandCursor
        )
        self.pushButtonCancel.setObjectName('pushButtonCancel')

        self.frame.layout().addWidget(self.groupBox, True)
        self.groupBox.layout().addWidget(self.pushButtonAccept, 0, 0, 1, 1)
        self.groupBox.layout().addWidget(self.pushButtonCancel, 0, 1, 1, 1)

        self.pushButtonAccept.clicked.connect(self.__accept_click)
        self.pushButtonCancel.clicked.connect(self.__cancel_click)

    @pyqtSlot()
    def __accept_click(self):
        self.clickedOn = Button.ACCEPT
        self.close()

    @pyqtSlot()
    def __cancel_click(self):
        self.clickedOn = Button.CANCEL
        self.close()


class MessageBoxPassword(_MessageBoxPasswordKernel):
    def __init__(
            self, parent, text: str, icon: str = None, font_size: int = None,
            color: str = _Color.FONT, window_size: QSize = _WINDOW_SIZE
    ):
        """Message for password input"""

        super(MessageBoxPassword, self).__init__(parent)
        self._set(window_size, icon, text, font_size, color)
        self.password = str()

        self.pushButtonAccept.clicked.connect(self.__accept_click)

    @pyqtSlot()
    def __accept_click(self):
        text = self.lineEdit.text()
        if text:
            self.password = text
            self.clickedOn = Button.ACCEPT
            self.close()


class MessageBoxPasswordConfirm(_MessageBoxPasswordKernel):
    def __init__(
            self, parent, text: str, password: str, icon: str = None, font_size: int = None,
            color: str = _Color.FONT, window_size: QSize = _WINDOW_SIZE
    ):
        """Message confirmation password"""

        super(MessageBoxPasswordConfirm, self).__init__(parent)
        self._set(window_size, icon, text, font_size, color)

        self.__passwordStored = password
        self.isVerified = False

        self.pushButtonAccept.clicked.connect(self.__accept_click)

    @pyqtSlot()
    def __accept_click(self):
        text = self.lineEdit.text()
        if text:
            self.clickedOn = Button.ACCEPT

            if text == self.__passwordStored:
                self.isVerified = True
                self.success()
            else:
                self.warning()


class MessageBoxPasswordMatching(_MessageBoxPasswordKernel):
    def __init__(
            self, parent, text: str, text_again: str, text_weak_password: str = None,
            password_score: int = 50, icon: str = None, font_size: int = None,
            color: str = _Color.FONT, window_size: QSize = _WINDOW_SIZE
    ):
        """Message match password"""

        super(MessageBoxPasswordMatching, self).__init__(parent)
        self._set(window_size, icon, text, font_size, color)

        self.__text = text_again
        self.__textWeakPassword = text_weak_password
        self.__passwordScore = password_score
        self.__passwordStored = None
        self.__isPasswordWeak = False
        self.isVerified = False
        self.password = str()

        self.pushButtonAccept.clicked.connect(self.__next)

    @pyqtSlot()
    def __next(self):
        text = self.lineEdit.text()
        if text:
            if self.__textWeakPassword:
                if int(PasswordStats(text).strength() * 100) < self.__passwordScore:
                    self.warning(self.__textWeakPassword, False)
                    self.__isPasswordWeak = True
                    self.nptManager.reset()
                    return

            self.__passwordStored = text
            self.pushButtonAccept.clicked.disconnect()
            self.pushButtonAccept.clicked.connect(self.__accept_click)
            self.nptManager.reset()
            if self.__isPasswordWeak:
                self.content_update(self.__text, icon='', color=_Color.FONT)

            else:
                self.content_update(self.__text)

    @pyqtSlot()
    def __accept_click(self):
        text = self.lineEdit.text()
        if text:
            self.clickedOn = Button.ACCEPT

            if text == self.__passwordStored:
                self.isVerified = True
                self.password = text
                self.success()
            else:
                self.warning()


class MessageBoxProgress(_MessageBoxKernel):
    def __init__(
            self, parent, text: str, core: callable, finished: callable = None,
            gui: callable = None, auto_run: bool = True, closable: bool = True,
            icon: str = None, font_size: int = None, color: str = _Color.FONT,
            window_size: QSize = _WINDOW_SIZE
    ):
        """Message for progress operation"""

        super(MessageBoxProgress, self).__init__(parent)
        self._set(window_size, icon, text, font_size, color)

        if not closable:
            self.pushButtonClose.hide()

        self.progressBar = QProgressBar(self.frame)
        self.progressBar.setFixedSize(QSize(281, 10))
        self.progressBar.setTextVisible(False)
        self.progressBar.setObjectName('progressBar')

        self.frame.layout().addWidget(self.progressBar, alignment=Qt.AlignHCenter)

        self.thread = _ThreadingArea(core)
        self.thread.signal.progress.connect(self.__progressbar)
        self.progressSignal = self.thread.signal.progress.emit

        if callable(gui):
            self.thread.signal.process.connect(gui)
            self.guiSignal = self.thread.signal.process.emit

        if callable(finished):
            self.thread.finished.connect(finished)

        if auto_run:
            self.run()

    def closeEvent(self, event):
        if self.thread.isRunning():
            if self.pushButtonClose.isVisible():
                self.thread.terminate()
                self.thread.wait()
            elif self.pushButtonClose.isHidden():
                event.ignore()
                return None

        super(MessageBoxProgress, self).closeEvent(event)

    def run(self):
        self.thread.start()

    def __progressbar(self, value: int):
        self.progressBar.setValue(value)


class MessageBoxLoading(_MessageBoxKernel):
    def __init__(
            self, parent, text: str, core: callable, finished: callable = None,
            gui: callable = None, auto_run: bool = True, closable: bool = True,
            icon: str = None, font_size: int = None, color: str = _Color.FONT,
            window_size: QSize = _WINDOW_SIZE
    ):
        """Message for loading operation"""

        super(MessageBoxLoading, self).__init__(parent)
        self._set(window_size, icon, text, font_size, color)

        if not closable:
            self.pushButtonClose.hide()

        self.__loading = QLoadingEffect(self.frame)

        self.groupBoxLoading = QuickGroupBox(self.frame, fixed_height=self.__loading.height())
        self.groupBoxLoading.setLayout(QVBoxLayout())
        self.groupBoxLoading.layout().setContentsMargins(0, 0, 0, 0)
        self.groupBoxLoading.setObjectName('groupBoxLoading')

        self.frame.layout().addWidget(self.groupBoxLoading, True)
        self.groupBoxLoading.layout().addWidget(self.__loading, alignment=Qt.AlignHCenter)

        self.thread = _ThreadingArea(core)
        self.thread.finished.connect(lambda: self.__finished(finished))

        if callable(gui):
            self.thread.signal.process.connect(gui)
            self.guiSignal = self.thread.signal.process.emit

        if auto_run:
            self.run()

    def closeEvent(self, event):
        if self.thread.isRunning():
            if self.pushButtonClose.isVisible():
                self.thread.terminate()
                self.thread.wait()
            elif self.pushButtonClose.isHidden():
                event.ignore()
                return None

        super(MessageBoxLoading, self).closeEvent(event)

    def run(self):
        self.__loading.start()
        self.thread.start()

    def __finished(self, finished: callable):
        self.__loading.stop()

        if callable(finished):
            finished()
