## Usage
This package mainly consists of two classes. ```LoadingTranslucentScreen(parent: QWidget, description_text: str = '', dot_animation: bool = True)``` and ```LoadingThread(loading_screen: LoadingTranslucentScreen)```. I can show you how it works basically.
```python
self.loadingTranslucentScreen = LoadingTranslucentScreen(parent=self,
                                                           description_text='Waiting...', dot_animation=False)
self.thread = LoadingThread(loading_screen=self.loadingTranslucentScreen)
self.thread.start()
```

Just give the parent widget to ```LoadingTranslucentScreen``` as a <b>first argument</b>. 

<b>Second argument</b> is description text of ```QLabel``` which will be shown with loading icon(loading icon is .gif extension, ```QMovie``` will get the gif loading icon) when you start the ```LoadingThread```. Defaut value is empty string.

<b>Third argument</b>(```dot_animation```) decides if triple dots animation of description text will operate or not. There is an explanation of triple dots animation feature below. Default value is True.

Give instant of ```LoadingTranslucentScreen``` to ```LoadingThread```'s argument and call the start method of it. 

Default ```run()``` task of this thread is ```time.sleep(5)```.

You can inherit this module and override run method.

You can use ```setDescriptionLabelDirection(direction: str)``` method of ```LoadingTranslucentScreen``` to set the direction of description label.

If thread starts running, dot animation will be activated. If the description text is 'Waiting', dot animation will be like below.
```
Waiting.
Waiting..
Waiting...
```
Of course this feature can reveal a couple of potential flaws if any dots are included in description text. I will fix that soon enough.

Valid argument is ```Left```, ```Right```, ```Top```, ```Bottom```. All of them should be ```str``` type.

Default direction is ```Bottom```.

I show you how to use the method ```setDescriptionLabelDirection```.
```python
self.loadingTranslucentScreen.setDescriptionLabelDirection('Right')
```
If you set the description label direction right like the example above, description text will be shown on the right side of the loading icon.

If you want to show loading icon only, make instance like this.
```python
self.__loadingTranslucentScreen = LoadingTranslucentScreen(parent=self, dot_animation=False)
```

## Example
### Code Sample
```python
import time
from PyQt6.QtWidgets import QPushButton, QTextEdit, QVBoxLayout, QWidget, QApplication

from pyqt_translucent_full_loading_screen_thread import LoadingThread, LoadingTranslucentScreen

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
```

