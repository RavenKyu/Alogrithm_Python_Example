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
        self.sx = 5
        self.sy = 0
        self.r = 100
        self.is_touched = False

    def drawSelf(self, qp):
        if self.is_touched:
            pen = QtGui.QPen(QtCore.Qt.red, 2, QtCore.Qt.SolidLine)
        else:
            pen = QtGui.QPen(QtCore.Qt.black, 2, QtCore.Qt.SolidLine)

        qp.setPen(pen)
        qp.drawEllipse(self.x, self.y, self.r, self.r)
        qp.drawPoint((self.x + self.r /2), (self.y + self.r /2))


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

        for i in range(1, random.randrange(1,5)):
        # for i in range(1, 2):
            # x = random.randrange(0, 639)
            # y = random.randrange(0, 479)
            x = 200
            y = 0
            sr = random.randrange(20, 50)
            self.e.append(
                Enemy(x, y, sr, sr)
            )

    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key() == QtCore.Qt.Key_Escape:
            self.init_enemies()

    def timerEvent(self, e):
        # self.checkCrash()
        self.ball_moving()
        self.repaint()

    def mouseMoveEvent(self, QMouseEvent):
        self.mouse_x = QMouseEvent.x()
        self.mouse_y = QMouseEvent.y()

    def ball_moving(self):
        for b in self.e:
            if b.y >= 380:
                b.y = 380
                b.sy = -(b.sy)
            if b.x >= 540 or b.x < 0:
                b.sx = -(b.sx)

            b.sy = b.sy + 0.2
            b.x = b.x + b.sx
            b.y = b.y + b.sy


    # def checkCrash(self):
    #     mx = self.mouse_x
    #     my = self.mouse_y
    #
    #
    #     e_cnt = len(self.e)
    #     for i in range(0, e_cnt):
    #         z = (abs(mx - ((self.e[i].x) + (self.e[i].sx /2))) ** 2) + \
    #             (abs(my - ((self.e[i].y) + (self.e[i].sx /2))) ** 2)
    #         z = math.sqrt(z)
    #
    #         if z < ((self.e[i].sx / 2) + 50):
    #             self.e[i].is_touched = True
    #         else:
    #             self.e[i].is_touched = False


    def paintEvent(self, QPaintEvent):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawInfo(QPaintEvent, qp)
        # self.drawMouse(QPaintEvent, qp)
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
