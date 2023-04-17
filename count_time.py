from main import *
import time
from PyQt5.QtCore import QThread, pyqtSignal

class Timeclass(QThread):
    value = pyqtSignal(int)

    def run(self):
        cnt = 1
        while True:
            self.value.emit(cnt)
            time.sleep(1)