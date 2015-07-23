# coding: utf-8

import sys
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui
import time
import random
import math

class Obj():
    def __init__(self, x, y):
        self._x = x
        self._y = y
        self._type = None
        self.is_touched = False

    def drawSelf(self, qp):
        """
        오버라이딩하여 사용할 것
        :param qp:
        :return:
        """

class Rectangle(Obj):
    def __init__(self, x, y, w, h):
        super(Rectangle, self).__init__(x, y)
        self._w = w
        self._h = h
        self._type = "Rectange"


    def is_overlap_circle(self, circle):
        """
         원과 사각형의 충돌 검사
        :param circle:
        :return: Boolean
        """

        pass

    def is_overlap_rectangle(self, rectangle):
        """
        사각형 끼리의 충돌
        :param rectangle:
        :return: Boolean
        """
        pass

    def drawSelf(self, qp):
        if self.is_touched:
            pen = QtGui.QPen(QtCore.Qt.red, 2, QtCore.Qt.SolidLine)
        else:
            pen = QtGui.QPen(QtCore.Qt.black, 2, QtCore.Qt.SolidLine)

        qp.setPen(pen)
        qp.drawRect(self._x, self._y, self._w, self._h)
        qp.drawPoint((self._x + self._w /2), (self._y + self._h /2))


class Circle(Obj):
    def __init__(self, x, y, r):
        super(Circle, self).__init__(x, y)
        self._r = r
        self._type = "Circle"

    def is_overlap_circle(self, circle):
        """
         원과 사각형의 충돌 검사
        :param circle:
        :return: Boolean
        """

        pass

    def is_overlap_rectangle(self, rectangle):
        """
        사각형 끼리의 충돌
        :param rectangle:
        :return: Boolean
        """
        pass

    def drawSelf(self, qp):
        if self.is_touched:
            pen = QtGui.QPen(QtCore.Qt.red, 2, QtCore.Qt.SolidLine)
        else:
            pen = QtGui.QPen(QtCore.Qt.black, 2, QtCore.Qt.SolidLine)

        qp.setPen(pen)
        qp.drawEllipse(self._x, self._y, self._r, self._r)
        qp.drawPoint((self._x + self._r /2), (self._y + self._r /2))



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

        for i in range(1, random.randrange(2,3)):
            # x = random.randrange(0, 639)
            # y = random.randrange(0, 479)
            x = 200
            y = 200
            # sr = random.randrange(20, 10)
            w = h = 100
            self.e.append(
                Rectangle(x, y, w, h)
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
        mc_x = self.mouse_x
        mc_y = self.mouse_y
        close_x = mc_x
        close_y = mc_y
        e_cnt = len(self.e)
        for i in range(0, e_cnt):
            if mc_x < self.e[i]._x:
                close_x = self.e[i]._x
            elif  mc_x > self.e[i]._x + self.e[i]._w:
                close_x = self.e[i]._x + self.e[i]._w

            if mc_y < self.e[i]._y:
                close_y = self.e[i]._y
            elif mc_y > self.e[i]._y + self.e[i]._h:
                close_y = self.e[i]._y + self.e[i]._h

            z = (abs(mc_x - close_x) ** 2) + (abs(mc_y - close_y) ** 2)
            z = math.sqrt(z)

            if z < 50:
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