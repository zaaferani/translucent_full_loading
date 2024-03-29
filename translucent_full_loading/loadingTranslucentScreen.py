import os, inspect, sys

from PyQt6.QtWidgets import QWidget, QLabel, QGridLayout, QGraphicsOpacityEffect
from PyQt6.QtCore import QSize, Qt, QThread, QTimer
from PyQt6.QtGui import QMovie, QPalette, QColor


class LoadingTranslucentScreen(QWidget):
    def __init__(self, parent: QWidget, description_text: str = '', dot_animation: bool = True):
        super().__init__(parent)
        self.__parent = parent
        self.__parent.installEventFilter(self)
        self.__parent.resizeEvent = self.resizeEvent

        self.__dot_animation_flag = dot_animation

        self.__descriptionLbl_original_text = description_text

        self.__initUi(description_text)

    def __initUi(self, description_text):
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)

        self.__movieLbl = QLabel(self.__parent)

        caller_path = os.path.dirname(inspect.getframeinfo(sys._getframe(1)).filename)
        loading_screen_ico_filename = os.path.join(caller_path, 'ico/loading.gif')

        self.__loading_mv = QMovie(loading_screen_ico_filename)
        self.__loading_mv.setScaledSize(QSize(45, 45))
        self.__movieLbl.setMovie(self.__loading_mv)
        self.__movieLbl.setStyleSheet('QLabel { background: transparent; }')
        self.__movieLbl.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignCenter)

        self.__descriptionLbl = QLabel()
        if description_text.strip() != '':
            self.__descriptionLbl.setText(description_text)
            self.__descriptionLbl.setVisible(False)
            self.__descriptionLbl.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignCenter)

        lay = QGridLayout()
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignCenter)
        self.setLayout(lay)
        self.setDescriptionLabelDirection('Bottom')  # default description label direction

        self.setMinimumSize(self.__parent.width(), self.__parent.height())

        self.setVisible(False)

        self.__timerInit()

    def __timerInit(self):
        if self.__dot_animation_flag:
            self.__timer = QTimer(self)
            self.__timer.timeout.connect(self.__ticking)
            self.__timer.singleShot(0, self.__ticking)
            self.__timer.start(500)

    def __ticking(self):
        dot = '.'
        cur_text = self.__descriptionLbl.text()
        cnt = cur_text.count(dot)
        if cnt % 3 == 0 and cnt != 0:
            self.__descriptionLbl.setText(self.__descriptionLbl_original_text + dot)
        else:
            self.__descriptionLbl.setText(cur_text + dot)

    def setParentThread(self, parent_thread: QThread):
        self.__thread = parent_thread

    def setDescriptionLabelDirection(self, direction: str):
        lay = self.layout()
        if direction == 'Left':
            lay.addWidget(self.__descriptionLbl, 0, 0, 1, 1)
            lay.addWidget(self.__movieLbl, 0, 1, 1, 1)
        elif direction == 'Top':
            lay.addWidget(self.__descriptionLbl, 0, 0, 1, 1)
            lay.addWidget(self.__movieLbl, 1, 0, 1, 1)
        elif direction == 'Right':
            lay.addWidget(self.__movieLbl, 0, 0, 1, 1)
            lay.addWidget(self.__descriptionLbl, 0, 1, 1, 1)
        elif direction == 'Bottom':
            lay.addWidget(self.__movieLbl, 0, 0, 1, 1)
            lay.addWidget(self.__descriptionLbl, 1, 0, 1, 1)
        else:
            raise BaseException('Invalid direction.')

    def start(self):
        self.__loading_mv.start()
        self.__descriptionLbl.setVisible(True)
        self.raise_()

        self.setVisible(True)
        opacity_effect = QGraphicsOpacityEffect(opacity=0.75)
        self.setGraphicsEffect(opacity_effect)

    def stop(self):
        self.__loading_mv.stop()
        self.__descriptionLbl.setVisible(False)
        self.lower()

        self.setVisible(False)

    def makeParentDisabledDuringLoading(self):
        if self.__thread.isRunning():
            self.__parent.setEnabled(False)
        else:
            self.__parent.setEnabled(True)

    def paintEvent(self, e):
        palette = QPalette()
        palette.setColor( QPalette.ColorGroup.Active, QPalette.ColorRole.Window , QColor(255, 255, 255))
        self.setAutoFillBackground(True)
        self.setPalette(palette)
        return super().paintEvent(e)

    def eventFilter(self, obj, e):
        if isinstance(obj, QWidget):
            if e.type() == 14:
                self.setFixedSize(e.size())
        return super(LoadingTranslucentScreen, self).eventFilter(obj, e)

