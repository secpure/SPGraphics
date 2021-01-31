from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from password_strength import PasswordStats
import SPSecurity
import time


SPSecurity.License(
    path=(
        83, 69, 67, 80, 117, 114, 101, 46,
        109, 97, 110, 105, 102, 101, 115, 116
    ),
    checksum=(
        100, 52, 97, 101, 100, 50, 55, 52, 48, 99, 99,
        57, 99, 97, 100, 56, 55, 99, 52, 56, 51, 53,
        51, 56, 56, 57, 52, 102, 48, 97, 52, 52
    )
).check()


# // Values
_EYE_RULES = {}
_TRANSLATOR = QApplication.translate
_WAITING_MESSAGE = "Try again in {} seconds."


# // Action data type
class ActionType:
    def __init__(self, *args, **kwargs):
        """Action object type"""
        pass


# // Actions properties
class Action:
    SHOW = ActionType()
    HIDE = ActionType()
    ENABLED = ActionType()
    DISABLED = ActionType()


# // Strength state properties
class StrengthState:
    """Password strength values as text and color"""

    class __SubState:
        text = None
        color = None

    excellent = __SubState()
    excellent.text = "Excellent"
    excellent.color = '#00DF6C'

    good = __SubState()
    good.text = "Good"
    good.color = '#90FF00'

    average = __SubState()
    average.text = "Average"
    average.color = '#FF7000'

    weak = __SubState()
    weak.text = "Weak"
    weak.color = '#FF4000'

    veryWeak = __SubState()
    veryWeak.text = "Very Weak"
    veryWeak.color = '#FF0000'

    rate = {
        75: excellent,
        50: good,
        30: average,
        10: weak,
        0: veryWeak
    }


# // StrengthBar object
class QStrengthBar(QWidget):
    def __init__(self, parent=None):
        super(QStrengthBar, self).__init__(parent, Qt.SubWindow)

        # // Layout configuration
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)

        # // ProgressBar create
        self.__progressBar = QProgressBar(self)
        self.__progressBar.setTextVisible(False)
        self.__progressBar.setFixedHeight(6)

        # // Label create
        self.__label = QLabel(self)

        # // Motion bar create
        self.__animation = QVariantAnimation()
        self.__animation.valueChanged.connect(self.__progressBar.setValue)
        self.__animation.setDuration(200)

        # // Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.timerEvent)

        # // Other values
        self.__state = None
        self.__backgroundColor = None
        self.__radius = 3
        self.__currentValue = 0
        self.__lastTime = 0

        # // Add widgets to layout
        self.setTextBottom()

    def showEvent(self, event):
        super(QStrengthBar, self).showEvent(event)

        self.timer.start(500)

    def hideEvent(self, event):
        super(QStrengthBar, self).hideEvent(event)

        self.timer.stop()

    def timerEvent(self):
        # // Get last value to use as start point
        current = self.__progressBar.value()
        if current == self.__currentValue or (time.time() - self.__lastTime) < 0.3:
            return

        # // Set points and start
        self.__animation.setStartValue(current)
        self.__animation.setEndValue(self.__currentValue)
        self.__animation.start()

        # // Get strength state and use it
        for num, sub in StrengthState.rate.items():
            if self.__currentValue >= num:
                self.setEasyStyleSheet(sub.color, self.__backgroundColor, self.__radius)

                if not self.isTextHidden():
                    if self.__currentValue == 0:
                        self.setText('')
                    else:
                        self.setText(sub.text)

                self.__state = sub
                return None

    def text(self):
        return self.__label.text()

    def setText(self, p_str):
        self.__label.setText(_TRANSLATOR('Form', p_str))

    def setFontSize(self, p_int):
        font = QFont()
        font.setPointSize(p_int)
        self.__label.setFont(font)

    def setTextTop(self):
        self.layout().insertWidget(0, self.__label)
        self.layout().insertWidget(1, self.__progressBar)

    def setTextBottom(self):
        self.layout().insertWidget(0, self.__progressBar)
        self.layout().insertWidget(1, self.__label)

    def setAlignment(self, union):
        self.__label.setAlignment(union)

    def setTextHidden(self, bool):
        self.__label.setHidden(bool)

    def isTextHidden(self):
        return self.__label.isHidden()

    def alignment(self):
        return self.__label.alignment()

    def state(self):
        return self.__state

    def value(self):
        self.__progressBar.value()

    def setValue(self, p_int):
        self.__currentValue = p_int
        self.__lastTime = time.time()

    def setBarHeight(self, p_int):
        self.__progressBar.setFixedHeight(p_int)

    def setBarHidden(self, bool):
        self.__progressBar.setHidden(bool)

    def isBarHidden(self):
        return self.__progressBar.isHidden()

    def setEasyStyleSheet(self, color: str, background_color: str = None, radius: int = 0):
        style = 'QProgressBar::chunk {background-color: %s; border-radius: %spx;}' % (
            color, radius)
        if background_color:
            style += 'QProgressBar {background-color: %s; border-radius: %spx;}' % (
                background_color, radius)

        self.__backgroundColor = background_color
        self.__radius = radius

        self.__label.setStyleSheet('color: %s;' % color)
        self.__progressBar.setStyleSheet(style)


# // Setup required value
class Setup:
    @staticmethod
    def set_icons(eye_show: str, eye_hide: str):
        """Set all icons as string path, EX: ':/images/icons/icon.png'"""

        class __Eye:
            icon = None
            mode = None
            state = None

        # // Show eye configuration
        show = __Eye()
        show.icon = eye_hide
        show.mode = QLineEdit.Normal
        show.state = True

        # // Hide eye configuration
        hide = __Eye()
        hide.icon = eye_show
        hide.mode = QLineEdit.Password
        hide.state = False

        # // Set configured
        _EYE_RULES[True] = hide
        _EYE_RULES[False] = show

    @staticmethod
    def set_waiting_message(text: str):
        """
        Set a message display when attempts is execute, Example : 'Try again in {} seconds.'
        Note: Don't forget this {} symbols with your new message
        """

        global _WAITING_MESSAGE
        _WAITING_MESSAGE = text


# // Eye button clicked
def _eye_clicked(editor: QLineEdit, eye: callable):
    """Eye click signal"""

    try:
        rule = _EYE_RULES[eye.state]
        eye.widget.setIcon(QIcon(rule.icon))
        editor.setEchoMode(rule.mode)
        eye.state = rule.state
    except KeyError:
        raise ValueError('Please setup icons')


# // LineEdit's signal for textChanged
def _strength_watcher(editor: QLineEdit, strength_bar: callable):
    if isinstance(editor, QLineEdit):
        text = editor.text()
    else:
        text = editor.toPlainText()

    try:
        percent = int(PasswordStats(text).strength() * 100)
    except Exception:
        percent = 0

    strength_bar.widget.setValue(percent)


# // Actions controller
def _set_action(widget, action: ActionType):
    """Set action"""

    if action is Action.DISABLED:
        widget.setDisabled(True)

    elif action is Action.ENABLED:
        widget.setEnabled(True)

    elif action is Action.HIDE:
        widget.hide()

    elif action is Action.SHOW:
        widget.show()


# // Input manager object
class InputManager:

    class __SubWidget:
        widget = None
        action = None
        actionBack = None
        state = None

    def __init__(
            self, editor: QLineEdit, failure_max: int = 5, seconds_wait: int = 60
    ):

        # // User values
        self.__editor = editor
        self.__maxAttempts = failure_max
        self.__secondsWait = seconds_wait

        # // Objects
        self.__eye = None
        self.__enter = None
        self.__strengthBar = None
        self.__placeholder = None
        self.__otherWidgets = list()
        self.__timerCalc = seconds_wait
        self.__timer = QTimer()
        self.__timer.timeout.connect(self.__lock_timer)

        # // Other values
        self.attempts = 0
        self.isLocked = False

    def eye_connect(
            self, button: QPushButton, action: ActionType = Action.DISABLED,
            action_back: ActionType = Action.ENABLED, one_click: bool = True
    ):
        """Define eye button"""

        self.__eye = self.__SubWidget()
        self.__eye.widget = button
        self.__eye.action = action
        self.__eye.actionBack = action_back
        self.__eye.state = False

        if one_click:
            button.pressed.connect(lambda: _eye_clicked(self.__editor, self.__eye))
            button.released.connect(lambda: _eye_clicked(self.__editor, self.__eye))
        else:
            button.clicked.connect(lambda: _eye_clicked(self.__editor, self.__eye))

    def strength_bar_connect(
            self, strength_bar: QStrengthBar, action: ActionType = Action.DISABLED,
            action_back: ActionType = Action.ENABLED
    ):
        """Define strength bar"""

        self.__strengthBar = self.__SubWidget()
        self.__strengthBar.widget = strength_bar
        self.__strengthBar.action = action
        self.__strengthBar.actionBack = action_back

        self.__editor.textChanged.connect(
            lambda: _strength_watcher(self.__editor, self.__strengthBar)
        )

    def enter_connect(
            self, button: QPushButton, action: ActionType = Action.DISABLED,
            action_back: ActionType = Action.ENABLED
    ):
        """Define enter button"""

        self.__enter = self.__SubWidget()
        self.__enter.widget = button
        self.__enter.action = action
        self.__enter.actionBack = action_back

    def other_widgets_connect(
            self, widgets: list, action: ActionType = Action.DISABLED,
            action_back: ActionType = Action.ENABLED
    ):
        """Define other widgets for action apply"""

        self.__otherWidgets.clear()

        for widget in widgets:
            obj = self.__SubWidget()
            obj.widget = widget
            obj.action = action
            obj.actionBack = action_back

            self.__otherWidgets.append(obj)

    def reset(self):
        self.__editor.clear()
        self.attempts = 0

        if self.__eye and self.__eye.state:
            self.__eye.widget.click()

    def attempts_check(self):
        """Check that attempts to make actions"""

        self.attempts += 1
        self.__editor.clear()

        if self.attempts >= self.__maxAttempts:
            self.__placeholder = self.__editor.placeholderText()
            self.__set_action()
            self.__timer.timeout.emit()
            self.__timer.start(1000)
            self.isLocked = True

    def __lock_timer(self):
        # // Waiting
        if self.__timerCalc:
            self.__timerCalc -= 1
            message = _TRANSLATOR('Form', _WAITING_MESSAGE).format(self.__timerCalc)
            self.__editor.setPlaceholderText(message)

        # // Finished and stop
        else:
            self.attempts = 0
            self.isLocked = False
            self.__timerCalc = self.__secondsWait
            self.__editor.setPlaceholderText(_TRANSLATOR('Form', self.__placeholder))
            self.__set_action_back()
            self.__timer.stop()

    def __set_action(self):
        """Set actions configured"""

        _set_action(self.__editor, Action.DISABLED)

        if self.__eye:
            _set_action(self.__eye.widget, self.__eye.action)

        if self.__strengthBar:
            _set_action(self.__strengthBar.widget, self.__strengthBar.action)

        if self.__enter:
            _set_action(self.__enter.widget, self.__enter.action)

        if self.__otherWidgets:
            for obj in self.__otherWidgets:
                _set_action(obj.widget, obj.action)

    def __set_action_back(self):
        """Set actions back configured"""

        _set_action(self.__editor, Action.ENABLED)

        if self.__eye:
            _set_action(self.__eye.widget, self.__eye.actionBack)

        if self.__strengthBar:
            _set_action(self.__strengthBar.widget, self.__strengthBar.actionBack)

        if self.__enter:
            _set_action(self.__enter.widget, self.__enter.actionBack)

        if self.__otherWidgets:
            for obj in self.__otherWidgets:
                _set_action(obj.widget, obj.actionBack)
