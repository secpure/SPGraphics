# SPGraphics
SPGraphics is designed to use PyQt5 with ease

## Requirements:
>sys\
PyQt5\
PasswordStats\
SPInputmanager\
SPSecurity\
SECPure.manifest

## How to [Setup](#Setup-methods):
- Set all icons as string path, EX: *':/images/icons/icon.png'* ( **Required** )
  >Setup.set_icons
- Set colors you want to use ( **Optional** )
  >Setup.set_colors
- Set message box details ( **Required** )
  >Setup.set_message_box_details

## All Methods:
| Return | Method | Description |
| --- | --- | --- |
| str | `LINE_EDIT_PLACEHOLDER` | The message box placeholder **Confirm your password** by default |
| None | [`text_ellipsis`](#text_ellipsis-Function) | Make ellipsis effect for any object text supported like QLabel |
| None | [`smooth_scroll`](#smooth_scroll-Function) | Make smooth scrolling for any object scroll supported like QListWidget |
| None | [`combobox_style`](#combobox_style-Function) | Make new combobox style |
| State | [`State`](#State-Properties) | Status of message display |
| Setup | [`Setup`](#Setup-Methods) | Setup required |
| MessageBoxButtonObject | `MessageBoxButtonObject` | Messagebox button data type |
| Button | [`Button`](#Button-Properties) | Buttons types for clicks |
| Property | [`Property`](#Property-Properties) | The property for Animation objects |
| QPropertyAnimation | [`OpacityMotion`](#OpacityMotion-Methods) | Opacity motion graphics |
| QPropertyAnimation | [`GeometryMotion`](#GeometryMotion-Methods) | Geometry motion graphics |
| QPropertyAnimation | [`MaximumWidthMotion`](#MaximumWidthMotion-Methods) | Maximum width motion graphics |
| QGraphicsDropShadowEffect | [`QuickShadow`](#QuickShadow-Methods) | Set shadow effect on window |
| QLineEdit | [`QuickLineEdit`](#QuickLineEdit-Methods) | Quick to create QlineEdit object, Set Qt.NoContextMenu by default |
| QLabel | [`QuickLabel`](#QuickLabel-Methods) | Quick to create QLabel object, Set `setWordWrap(True)` by default |
| QPushButton | [`QuickPushButton`](#QuickPushButton-Methods) | Quick to create QPushButton object, Set `setFocusPolicy(Qt.NoFocus)` by default |
| QRadioButton | [`QuickRadioButton`](#QuickRadioButton-Methods) | Quick to create QRadioButton object, Set `setFocusPolicy(Qt.NoFocus)` by default |
| QCheckBox | [`QuickCheckBox`](#QuickCheckBox-Methods) | Quick to create QCheckBox object, Set `setFocusPolicy(Qt.NoFocus)` by default |
| QDateEdit | [`QuickDateEdit`](#QuickDateEdit-Methods) | Quick to create QDateEdit object, Set `setContextMenuPolicy(Qt.NoContextMenu), setCalendarPopup(True)` by default |
| QGroupBox | [`QGroupBox`](#QGroupBox-Methods) | Quick to create QGroupBox object |
| QComboBox | [`QuickComboBox`](#QuickComboBox-Methods) | Quick to create QComboBox object, Set `setFocusPolicy(Qt.NoFocus)`, `combobox_style(self)` by default |
| QListWidget | [`QuickNotification`](#QuickNotification-Methods) | Notifications object |
| QWidget | [`QLoadingEffect`](#QLoadingEffect-Methods) | Loading motion effect |
| QLabel | [`QMarkNotify`](#QMarkNotify-Methods) | Mark point |
| QLabel | [`QBorderBottom`](#QBorderBottom-Methods) | Border bottom animated |
| QSwitch | [`QSwitch`](#QSwitch-Methods) | Switch button to check or no check |
| QDialog | [`MessageBox`](#MessageBox-Methods) | MessageBox for text display only |
| QDialog | [`MessageBoxConfirm`](#MessageBoxConfirm-Methods) | MessageBox for actions |
| QDialog | [`MessageBoxPassword`](#MessageBoxPassword-Methods) | MessageBox for get a password |
| QDialog | [`MessageBoxPasswordConfirm`](#MessageBoxPasswordConfirm-Methods) | MessageBox for confirm the password |
| QDialog | [`MessageBoxPasswordMatching`](#MessageBoxPasswordMatching-Methods) | MessageBox for get password and matching |
| QDialog | [`MessageBoxProgress`](#MessageBoxProgress-Methods) | MessageBox for processing with progressbar |
| QDialog | [`MessageBoxLoading`](#MessageBoxLoading-Methods) | MessageBox for processing with loading effect |

## text_ellipsis Function:
>Make ellipsis effect for any object text supported like QLabel
```py
None    text_ellipsis(
          QObject target,
          Qt.TextElideMode mode=Qt.ElideRight,
          int width=None
        )
```

## smooth_scroll Function:
>Make smooth scrolling for any object scroll supported like QListWidget
```py
None    smooth_scroll(
          QObject target,
          int step=8
        )
```

## combobox_style Function:
>Make new combobox style
```py
None    combobox_style(
          QComboBox target
        )
```

## State Properties:
>Use with MessageBox and QuickNotification\
Note : This object changeable
```py
object      State.information
str         State.information.icon
str         State.information.color
object      State.warning
str         State.warning.icon
str         State.warning.color
object      State.success
str         State.success.icon
str         State.success.color
object      State.failed
str         State.failed.icon
str         State.failed.color
```
| State | Default Color |
| --- | --- |
| information | #FFFFFF |
| warning | #FF7676 |
| success | #00DF6C |
| failed | #FF7676 |

## Button Properties:
>MessageBox's buttons type
```py
MessageBoxButtonObject    Button.ACCEPT
MessageBoxButtonObject    Button.CANCEL
MessageBoxButtonObject    Button.CLOSE
```

## Property Properties:
>QPropertyAnimation's property, Use with OpacityMotion
```py
bytes   Property.OPACITY
bytes   Property.WINDOW_OPACITY
bytes   Property.MAXIMUM_SIZE
bytes   Property.GEOMETRY
```

## Setup Methods:
>Set all icons as string path
```py
None    set_icons(
          str eye_show,
          str eye_hide,
          str enter_button,
          str close_button,
          str information_state,
          str warning_state,
          str success_state,
          str failed_state
        )
```
>Set colors you want to use
```py
None    set_colors(
          str font,
          str information,
          str warning,
          str success,
          str failed
        )
```
>Set message box details
```py
None    set_message_box_details(
          str window_title,
          str title_text,
          QFont title_font=None,
          str stylesheet=None
        )
```

## OpacityMotion Methods:
>Opacity motion graphics
```py
QPropertyAnimation    OpacityMotion(
                        QObject target,
                        bytes property_type=None
                      )
```
>Show widget as opacity
```py
QPropertyAnimation    temp_show(
                        int duration=300,
                        callable finished=None
                      )
```
>Hide widget as opacity
```py
QPropertyAnimation    temp_hide(
                        int duration=300,
                        callable finished=None
                      )
```
>Start motion
```py
None                  OpacityMotion.start()
```

## GeometryMotion Methods:
>Geometry motion graphics
```py
QPropertyAnimation    GeometryMotion(
                        QObject target
                      )
```
>Move widget as x
```py
QPropertyAnimation    temp_x(
                        int start_x,
                        int end_x,
                        int duration=500,
                        callable finished=None
                      )
```
>Move widget as y
```py
QPropertyAnimation    temp_y(
                        int start_y,
                        int end_y,
                        int duration=500,
                        callable finished=None
                      )
```
>Show widget as book
```py
QPropertyAnimation    temp_show(
                        int width,
                        int end_x,
                        int duration=500,
                        callable finished=None
                      )
```
>Hide widget as book
```py
QPropertyAnimation    temp_hide(
                        int duration=250,
                        callable finished=None
                      )
```
>Show widget from left to right
```py
QPropertyAnimation    temp_open(
                        int width,
                        int duration=500,
                        callable finished=None
                      )
```
>Hide widget from right to left
```py
QPropertyAnimation    temp_close(
                        int duration=250,
                        callable finished=None
                      )
```
>Start motion
```py
None                  start()
```

## MaximumWidthMotion Methods:
>Maximum width motion graphics
```py
QPropertyAnimation    MaximumWidthMotion(
                        QObject target
                      )
```
>Show widget with set width
```py
QPropertyAnimation    temp_show(
                        int width,
                        int duration=1000,
                        callable finished=None
                      )
```
>Hide widget with set width
```py
QPropertyAnimation    temp_hide(
                        int duration=500,
                        callable finished=None
                      )
```
>Start motion
```py
None                  start()
```

## QuickLineEdit Methods:
>Quick to create QlineEdit object, Set `Qt.NoContextMenu by` default
```py
QLineEdit   QuickLineEdit(
              QObject parent=None,
              str text=None,
              str placeholder_text=None,
              bool numeric=False,
              bool writable=True,
              QLineEdit.EchoMode mode=None,
              Qt.AlignmentFlag align=None,
              QSize fixed_size=None,
              int fixed_width=None,
              int fixed_height=None,
              bool layout_support=False,
              int length=64,
              callable value_changed=None,
              object start_value=None,
              object end_value=None,
              int duration=300
            )
```

## QuickLabel Methods:
>Quick to create QLabel object, Set `setWordWrap(True)` by default
```py
QLabel    QuickLabel(
            QObject parent=None,
            str text=None,
            bool linkable=False,
            bool scaled=False,
            int font_size=None,
            int fixed_width=None,
            int fixed_height=None,
            QSize fixed_size=None,
            QPixmap pixmap=None,
            Qt.AlignmentFlag align=None,
            callable value_changed=None,
            object start_value=None,
            object end_value=None,
            int duration=300
          )
```

## QuickPushButton Methods:
>Quick to create QPushButton object, Set `setFocusPolicy(Qt.NoFocus)` by default
```py
QPushButton   QuickPushButton(
                QObject parent=None,
                str text=None,
                QIcon icon=None,
                QSize icon_size=None,
                QSize fixed_size=None,
                int fixed_width=None,
                int fixed_height=None,
                int font_size=None,
                callable value_changed=None,
                object start_value=None,
                object end_value=None,
                int duration=300,
                Qt.CursorShape cursor=None
              )
```

## QuickRadioButton Methods:
>Quick to create QRadioButton object, Set `setFocusPolicy(Qt.NoFocus)` by default
```py
QPushButton   QuickRadioButton(
                QObject parent=None,
                str text=None,
                QIcon icon=None,
                QSize icon_size=None,
                QSize fixed_size=None,
                int fixed_width=None,
                int fixed_height=None,
                int font_size=None,
                bool checked=False,
                callable value_changed=None,
                object start_value=None,
                object end_value=None,
                int duration=300,
                Qt.CursorShape cursor=None
              )
```

## QuickCheckBox Methods:
>Quick to create QCheckBox object, Set `setFocusPolicy(Qt.NoFocus)` by default
```py
QCheckBox   QuickCheckBox(
              QObject parent=None,
              str text=None,
              QIcon icon=None,
              QSize icon_size=None,
              QSize fixed_size=None,
              int fixed_width=None,
              int fixed_height=None,
              int font_size=None,
              bool checkable=True,
              bool checked=False,
              callable value_changed=None,
              object start_value=None,
              object end_value=None,
              int duration=300,
              Qt.CursorShape cursor=None
            )
```

## QuickDateEdit Methods:
>Quick to create QDateEdit object, Set `setContextMenuPolicy(Qt.NoContextMenu)`, `setCalendarPopup(True)` by default
```py
QDateEdit   QuickDateEdit(
              QObject parent=None,
              str text=None,
              bool writable=True,
              bool scrollable=True,
              Qt.AlignmentFlag align=None,
              QSize fixed_size=None,
              int fixed_width=None,
              int fixed_height=None,
              int font_size=None,
              callable value_changed=None,
              object start_value=None,
              object end_value=None,
              int duration=300,
              Qt.CursorShape cursor=None
            )
```

## QuickGroupBox Methods:
>Quick to create QGroupBox object
```py
QGroupBox   QuickGroupBox(
              QObject parent=None,
              str text=None,
              Qt.AlignmentFlag align=None,
              QSize fixed_size=None,
              int fixed_width=None,
              int fixed_height=None,
              int font_size=None,
              bool checkable=False,
              bool checked=False,
              callable value_changed=None,
              object start_value=None,
              object end_value=None,
              int duration=300
            )
```

## QuickComboBox Methods:
>Quick to create QComboBox object, Set `setFocusPolicy(Qt.NoFocus)`, `combobox_style(self)` by default
```py
QComboBox   QuickComboBox(
              QObject parent=None,
              list items=None,
              bool editable=False,
              str current_text=None,
              int current_index=None,
              int max_visiable_items=None,
              int max_count=None,
              QSize icon_size=None,
              QSize fixed_size=None,
              int fixed_width=None,
              int fixed_height=None,
              int font_size=None,
              callable value_changed=None,
              object start_value=None,
              object end_value=None,
              int duration=300,
              Qt.CursorShape cursor=None
            )
```

## QuickNotification Methods:
>Notifications object
```py
QListWidget   QuickNotification(
                QObject parent,
                QSize size=QSize(321, 51),
                str stylesheet='',
                int top_margin=31,
                int right_margin=31,
                int bottom_margin=31
              )
```
>Customize the notification element
```py
None    create_new(
          str icon,
          str text,
          int font_size=None,
          str color=None,
          int timeout=1500,
          callable finished=None
        )
```
>Information template
```py
None    information(
          str text,
          int font_size=None,
          int timeout=1500,
          callable finished=None
        )
```
>Warning template
```py
None    warning(
          str text,
          int font_size=None,
          int timeout=1500,
          callable finished=None
        )
```
>Successfully template
```py
None    successfully(
          str text,
          int font_size=None,
          int timeout=1500,
          callable finished=None
        )
```
>Failed template
```py
None    failed(
          str text,
          int font_size=None,
          int timeout=1500,
          callable finished=None
        )
```

## QLoadingEffect Methods:
>Loading motion effect
```py
QWidget   QLoadingEffect(
            QObject parent=None,
            float duration=300,
            int count=4,
            str color='#9557FC',
            str light_color='#FF7676'
          )
```
>Start effect
```py
None    start()
```
>Stop effect
```py
None    stop()
```

## QMarkNotify Methods:
>Mark point effect
```py
QLabel    QMarkNotify(
            QObject parent
          )
```
>Show effect
```py
None    show()
```
>Hide effect
```py
None    hide()
```

## QBorderBottom Methods:
>Border bottom animated
```py
QLabel    QBorderBottom(
            QObject parent
          )
```
>Move position
```py
None    move_to_x(
          int x
        )
```

## QSwitch Methods:
>Switch button to check or no check, [Resources](https://stackoverflow.com/questions/14780517/toggle-switch-in-qt)\
>Note:
>  - Thumb-size can be larger/smaller than the track size
>  - Use current app’s palette for coloring
>  - Emit toggled/clicked signals when clicked
```py
QSwitch   QSwitch(
            QObject parent=None,
            int track_radius=10,
            int thumb_radius=8
          )
```

## MessageBox Methods:
>MessageBox for text display only
```py
QDialog   MessageBox(
            QObject parent,
            str text,
            str icon=None,
            int font_size=None,
            str color=_Color.FONT,
            QSize window_size=QSize(401, 161)
          )
```
>Templates with animations
```py
None    sucess(
          str text=None,
          bool close=True
        )
None    failed(
          str text=None,
          bool close=True
        )
None    warning(
          str text=None,
          bool close=True
        )
```
>Update content message with beautiful animations\
Note : if you want to remove icon , use `icon=''`\
if you want to remove text , use `text=None`
```py
None    content_update(
          str text=None,
          str icon=None,
          str color=None,
          bool close=False
        )
```
| Return | Method | Description |
| --- | --- | --- |
| None | `exec_()` | Messagebox execute |
| None | `close()` | Messagebox close |
| QFrame | `frame` | Body widget |
| QLabel | `labelTitle` | Header widget |
| QPushButton | `pushButtonClose` | Close button |
| QGroupBox | `groupBoxContent` | Message content icon + text |
| QLabel | `labelIcon` | Message icon |
| QLabel | `labelMessage` | Message text |
| any | `issue` | Use this var for the error store |
| MessageBoxButtonObject | `ClickedOn` | Button clicked |

## MessageBoxConfirm Methods:
>MessageBox for actions, Buttons translate supported\
Note: Inheritance from ***MessageBox***
```py
QDialog   MessageBoxConfirm(
            QObject parent,
            str text,
            str icon=None,
            int font_size=None,
            str color=_Color.FONT,
            str accept="Accept",
            str cancel="Cancel",
            QSize window_size==QSize(401, 161)
          )
```
| Return | Method | Description |
| --- | --- | --- |
| QGroupBox | `groupBox` | Buttons available |
| QPushButton | `pushButtonAccept` | Button accept |
| QPushButton | `pushButtonCancel` | Button cancel |

## MessageBoxPassword Methods:
>MessageBox for get a password\
Note: Inheritance from ***MessageBox***
```py
QDialog   MessageBoxPassword(
            QObject parent,
            str text,
            str icon=None,
            int font_size=None,
            str color=_Color.FONT,
            QSize window_size=QSize(401, 161)
          )
```
| Return | Method | Description |
| --- | --- | --- |
| QGroupBox | `groupBox` | Buttons available |
| QLineEdit | `lineEdit` | Input password |
| QPushButton | `pushButtonEye` | Eye button |
| QPushButton | `pushButtonAccept` | Button accept |
| QstrengthBar | `strengthBar` | Button cancel |
| InputManager | `nptManager` | Input manager with ***SPInputmanager*** library |
| str | `password` | Password writed |

## MessageBoxPasswordConfirm Methods:
>MessageBox for confirm the password\
Note: Inheritance from ***MessageBoxPassword***
```py
QDialog   MessageBoxPasswordConfirm(
            QObject parent,
            str text,
            str password,
            str icon=None,
            int font_size=None,
            str color=_Color.FONT,
            QSize window_size=QSize(401, 161)
          )
```
| Return | Method | Description |
| --- | --- | --- |
| bool | `isVerified` | Check if is verified |
| str | ~~`password`~~ | Password writed |

## MessageBoxPasswordMatching Methods:
>MessageBox for get password and matching\
Note: Inheritance from ***MessageBoxPassword***
```py
QDialog   MessageBoxPasswordMatching(
            QObject parent,
            str text,
            str text_again,
            str text_weak_password,
            int password_score=50,
            str icon=None,
            int font_size=None,
            str color=_Color.FONT,
            QSize window_size=QSize(401, 161)
          )
```
| Return | Method | Description |
| --- | --- | --- |
| bool | `isVerified` | Check if is verified |
| str | `password` | Password writed |

## MessageBoxProgress Methods:
>MessageBox for processing with progressbar\
Note: Inheritance from ***MessageBox***
```py
QDialog   MessageBoxProgress(
            QObject parent,
            str text,
            callable core,
            callable finished=None,
            callable gui=None,
            bool auto_run=True,
            bool closable=True,
            str icon=None,
            int font_size=None,
            str color=_Color.FONT,
            QSize window_size=QSize(401, 161)
          )
```
| Return | Method | Description |
| --- | --- | --- |
| QProgressBar | `progressBar` | Progressbar widget |
| QThread | `thread` | Threading operator |
| None | `run()` | Run manually |
| None | `guiSignal()` | Emit the gui method |
| None | `progressSignal(int)` | Emit the progressbar |

## MessageBoxLoading Methods:
>MessageBox for processing with loading effect\
Note: Inheritance from ***MessageBox***
```py
QDialog   MessageBoxLoading(
            QObject parent,
            str text,
            callable core,
            callable finished=None,
            callable gui=None,
            bool auto_run=True,
            bool closable=True,
            str icon=None,
            int font_size=None,
            str color=_Color.FONT,
            QSize window_size=QSize(401, 161)
          )
```
| Return | Method | Description |
| --- | --- | --- |
| QThread | `thread` | Threading operator |
| None | `run()` | Run manually |
| None | `guiSignal()` | Emit the gui method |
