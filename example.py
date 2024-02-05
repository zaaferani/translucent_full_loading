import time
from PyQt6.QtWidgets import QPushButton, QTextEdit, QVBoxLayout, QWidget, QApplication
import os, sys; sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from loadingThread import LoadingThread
from loadingTranslucentScreen import LoadingTranslucentScreen


# for second result
class MyThread(LoadingThread):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self):
        time.sleep(1)


class Main(QWidget):
    def __init__(self):
        super().__init__()
        self.__initUi()

    def __initUi(self):
        btn = QPushButton('Start Loading Thread')
        btn.clicked.connect(self.__startLoadingThread)
        self.__te = QTextEdit()

        lay = QVBoxLayout()
        lay.addWidget(btn)
        lay.addWidget(self.__te)

        self.setLayout(lay)

    def __startLoadingThread(self):
        self.__loadingTranslucentScreen = LoadingTranslucentScreen(parent=self,
                                                                   description_text='Waiting')
        self.__loadingTranslucentScreen.setDescriptionLabelDirection('Right')
        self.__thread = LoadingThread(loading_screen=self.__loadingTranslucentScreen)
        # for second result
        # self.__thread = MyThread(loading_screen=self.__loadingTranslucentScreen)
        self.__thread.start()


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    window = Main()
    window.show()
    app.exec()
