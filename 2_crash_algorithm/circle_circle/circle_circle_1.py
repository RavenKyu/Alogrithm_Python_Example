# coding: utf-8

import sys
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui
import time
import random
import math

class Enemy():
    def __init__(self, x, y, sx, sy):
        self.x = x
        self.y = y
        self.sx = sx
        self.is_touched = False

    def drawSelf(self, qp):
        if self.is_touched:
            pen = QtGui.QPen(QtCore.Qt.red, 2, QtCore.Qt.SolidLine)
        else:
            pen = QtGui.QPen(QtCore.Qt.black, 2, QtCore.Qt.SolidLine)

        qp.setPen(pen)
        qp.drawEllipse(self.x, self.y, self.sx, self.sx)
        qp.drawPoint((self.x + self.sx /2), (self.y + self.sx /2))


class Form(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        self.mouse_x = 0
        self.mouse_y = 0
        self.setMouseTracking(True)

        self.init_enemies()

        self.rt = QtCore.QBasicTimer()
        self.rt.start(10, self)


    def init_enemies(self):
        self.e = []

        for i in range(1, random.randrange(1,10)):
            x = random.randrange(0, 639)
            y = random.randrange(0, 479)
            sr = random.randrange(20, 50)
            self.e.append(
                Enemy(x, y, sr, sr)
            )

    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key() == QtCore.Qt.Key_Escape:
            self.init_enemies()

    def timerEvent(self, e):
        self.checkCrash()
        self.repaint()

    def mouseMoveEvent(self, QMouseEvent):
        self.mouse_x = QMouseEvent.x()
        self.mouse_y = QMouseEvent.y()


    def checkCrash(self):
        mx = self.mouse_x
        my = self.mouse_y




        e_cnt = len(self.e)
        for i in range(0, e_cnt):
            z = (abs(mx - ((self.e[i].x) + (self.e[i].sx /2))) ** 2) + \
                (abs(my - ((self.e[i].y) + (self.e[i].sx /2))) ** 2)
            z = math.sqrt(z)

            if z < ((self.e[i].sx / 2) + 50):
                self.e[i].is_touched = True
            else:
                self.e[i].is_touched = False


    def paintEvent(self, QPaintEvent):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawInfo(QPaintEvent, qp)
        self.drawMouse(QPaintEvent, qp)
        self.drawEnemies(QPaintEvent, qp)
        qp.end()

    def drawEnemies(self, event, qp):
        for e in self.e:
            e.drawSelf(qp)

    def drawMouse(self, event, qp):
        qp.setPen(QtGui.QColor('black'))
        qp.drawEllipse(self.mouse_x - 50, self.mouse_y - 50, 100, 100)


    def drawInfo(self, event, qp):
        qp.setPen(QtGui.QColor('black'))
        qp.setFont(QtGui.QFont('Decorative', 11))
        qp.drawText(10, 10, "mX: %d mY: %d" % (self.mouse_x, self.mouse_y))



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    # app.processEvents(QtCore.QEventLoop.AllEvents)
    w = Form()
    w.show()
    sys.exit(app.exec())
