import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from random import choice
import copy

class MyWidget(QMainWindow):
    with open('stroka.txt', "rt") as f:
        a = f.readlines()

    def __init__(self):
        super().__init__()
        uic.loadUi('перемешивание.ui', self)
        self.btn.clicked.connect(self.run)

    def run(self):
        self.new_a = copy.copy(self.a)
        self.count = len(self.a)
        self.a.clear()
        while self.count != 0:
            for i in range(len(self.new_a)):
                if i % 2 == 0:
                    self.a.append(self.new_a[i])
                    self.count -= 1
                else:
                    self.a.append(self.new_a[i])
                    self.count -= 1
        self.lineEdit.setText('/n'.join(self.a))

def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())