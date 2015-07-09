# coding: utf-8

import sys
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui
import time
import random
import math

class Ball():
    _con_size = 50
    _bg_w = 0
    _bg_h = 0

    def __init__(self, x, y, r):

        # 좌표
        self.x = x
        self.y = y
        # 속도
        self.sx = 5 if random.randrange(1,3) == 1 else -5

        self.sy = 0
        # 지름
        self.r = r
        # 상태
        self.is_touched = False

    def move(self):
        """볼의 이동 값을 구한다."""
        # 볼이 움직일 수 있는 값을 구한다
        end_of_ww = (self._bg_w - self.r)
        end_of_wh = (self._bg_h - self.r)

        # x 좌표값 검사
        if self.x >= end_of_ww or self.x < 0:
            self.sx *= -1 # 음양수 토글

        # y 좌표값 검사
        if self.y >= end_of_wh:
            self.y = end_of_wh
            self.sy *= -1
        elif self.y <= 0:
            self.y = 0
            self.sy *= -1
        else:
            self.sy += 0.1

        self.x += self.sx
        self.y += self.sy


    def draw(self, qp):
        # 원을 그리는 함수
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

        self.init_objects()

        self.rt = QtCore.QBasicTimer()
        self.rt.start(10, self)


    def init_objects(self):
        self.ww = self.width()
        self.wh = self.height()
        Ball._bg_w = self.ww
        Ball._bg_h = self.wh

        self.e = []

        for i in range(1, random.randrange(2,7)):
            r = random.randrange(1, 4) * Ball._con_size
            x = random.randrange(0, self.ww - r)

            y = random.randrange(1, ((self.wh - r) - 100))

            self.e.append(
                Ball(x, y, r)
            )

    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key() == QtCore.Qt.Key_Escape:
            self.init_objects()

    def timerEvent(self, e):
        self.ball_moving()
        self.repaint()


    def mouseMoveEvent(self, QMouseEvent):
        self.mouse_x = QMouseEvent.x()
        self.mouse_y = QMouseEvent.y()


    def ball_moving(self):
        for b in self.e:
            b.move()


    def paintEvent(self, QPaintEvent):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawInfo(QPaintEvent, qp)
        self.draw_balls(QPaintEvent, qp)
        qp.end()


    def draw_balls(self, event, qp):
        for e in self.e:
            e.draw(qp)


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
