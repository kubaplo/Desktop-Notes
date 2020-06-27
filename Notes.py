from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys, time


class NoteApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setup()


    def setup(self):
        self.setWindowTitle("Desktop Notes")
        self.setGeometry(100, 100, 400, 600)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setStyleSheet("border: 2px solid #4C4A48")
        self.main_page()


    def main_page(self):
        frame = QtWidgets.QFrame(self)
        frame.setGeometry(0, 0, self.width(), self.height())
        background = "#444"
        frame.setStyleSheet(f"background-color: {background}")
        self.frame = frame

        class MoveLabel(QtWidgets.QLabel):
            def __init__(self, *args):
                super().__init__(args[0])
                self.holding = False
                self.window = args[-1]


            def mousePressEvent(self, event):
                if event.button() == QtCore.Qt.LeftButton:
                    self.holding = True
                    self.last_position = (event.pos().x(), event.pos().y())


            def mouseReleaseEvent(self, event):
                if event.button() == QtCore.Qt.LeftButton:
                    self.holding = False


            def mouseMoveEvent(self, event):
                position = (event.pos().x(), event.pos().y())
                if self.holding:
                    x = position[0] - self.last_position[0]
                    y = position[1] - self.last_position[1]

                    self.window.move(self.window.x() + x, self.window.y() + y)



        move_label = MoveLabel(frame, self)
        move_label.setGeometry(0, 0, self.width(), 10)
        move_label.setStyleSheet("background-color: #4C4A48")
        self.move_label = move_label


        class LeftResize(QtWidgets.QLabel):
            def __init__(self, *args):
                super().__init__(args[0])
                self.window = args[1]
                self.holding = False
                self.last_position = (0, 0)

            def mousePressEvent(self, event):
                if event.button() == QtCore.Qt.LeftButton:
                    self.holding = True
                    self.last_position = (event.pos().x(), event.pos().y())

            def mouseReleaseEvent(self, event):
                if event.button() == QtCore.Qt.LeftButton:
                    self.holding = False

            def mouseMoveEvent(self, event):
                if self.holding:
                    x = self.last_position[0] - event.pos().x()
                    if x >= 0 or self.window.width() > 50:
                        self.window.resize(self.window.width() + x, self.window.height())
                        self.window.move(self.window.x() - x, self.window.y())


        left_resize = LeftResize(frame, self)
        left_resize.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        left_resize.setGeometry(0, 10, 5, self.height()-20)
        left_resize.setCursor(QtGui.QCursor(QtCore.Qt.SizeHorCursor))
        self.left_resize = left_resize


        class RightResize(QtWidgets.QLabel):
            def __init__(self, *args):
                super().__init__(args[0])
                self.window = args[1]
                self.holding = False
                self.last_position = (0, 0)

            def mousePressEvent(self, event):
                if event.button() == QtCore.Qt.LeftButton:
                    self.holding = True
                    self.last_position = (event.pos().x(), event.pos().y())

            def mouseReleaseEvent(self, event):
                if event.button() == QtCore.Qt.LeftButton:
                    self.holding = False

            def mouseMoveEvent(self, event):
                if self.holding:
                    x = event.pos().x() - self.last_position[0]
                    if x >= 0 or self.window.width() > 50:
                        self.window.resize(self.window.width() + x, self.window.height())


        right_resize = RightResize(frame, self)
        right_resize.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        right_resize.setGeometry(self.width()-5, 10, 5, self.height()-20)
        right_resize.setCursor(QtGui.QCursor(QtCore.Qt.SizeHorCursor))
        self.right_resize = right_resize


        class BottomResize(QtWidgets.QLabel):
            def __init__(self, *args):
                super().__init__(args[0])
                self.window = args[1]
                self.holding = False
                self.last_position = (0, 0)

            def mousePressEvent(self, event):
                if event.button() == QtCore.Qt.LeftButton:
                    self.holding = True
                    self.last_position = (event.pos().x(), event.pos().y())

            def mouseReleaseEvent(self, event):
                if event.button() == QtCore.Qt.LeftButton:
                    self.holding = False

            def mouseMoveEvent(self, event):
                if self.holding:
                    y = event.pos().y() - self.last_position[1]
                    if y >= 0 or self.window.height() > 50:
                        self.window.resize(self.window.width(), self.window.height() + y)



        bottom_resize = BottomResize(frame, self)
        bottom_resize.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        bottom_resize.setGeometry(10, self.height()-5, self.width()-20, 5)
        bottom_resize.setCursor(QtGui.QCursor(QtCore.Qt.SizeVerCursor))
        self.bottom_resize = bottom_resize


        class BottomLeftResize(QtWidgets.QLabel):
            def __init__(self, *args):
                super().__init__(args[0])
                self.window = args[1]
                self.holding = False
                self.last_position = (0, 0)

            def mousePressEvent(self, event):
                if event.button() == QtCore.Qt.LeftButton:
                    self.holding = True
                    self.last_position = (event.pos().x(), event.pos().y())

            def mouseReleaseEvent(self, event):
                if event.button() == QtCore.Qt.LeftButton:
                    self.holding = False

            def mouseMoveEvent(self, event):
                if self.holding:
                    x = self.last_position[0] - event.pos().x()
                    y = event.pos().y() - self.last_position[1]
                    if x >= 0 or self.window.width() > 50:
                        self.window.resize(self.window.width() + x, self.window.height())
                        self.window.move(self.window.x() - x, self.window.y())
                    if y >= 0 or self.window.height() > 50:
                        self.window.resize(self.window.width(), self.window.height() + y)


        bottom_left_resize = BottomLeftResize(frame, self)
        bottom_left_resize.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        bottom_left_resize.setGeometry(0, self.height() - 5, 5, 5)
        bottom_left_resize.setCursor(QtGui.QCursor(QtCore.Qt.SizeBDiagCursor))
        self.bottom_left_resize = bottom_left_resize

        class BottomRightResize(QtWidgets.QLabel):
            def __init__(self, *args):
                super().__init__(args[0])
                self.window = args[1]
                self.holding = False
                self.last_position = (0, 0)

            def mousePressEvent(self, event):
                if event.button() == QtCore.Qt.LeftButton:
                    self.holding = True
                    self.last_position = (event.pos().x(), event.pos().y())

            def mouseReleaseEvent(self, event):
                if event.button() == QtCore.Qt.LeftButton:
                    self.holding = False

            def mouseMoveEvent(self, event):
                if self.holding:
                    x = event.pos().x() - self.last_position[0]
                    y = event.pos().y() - self.last_position[1]
                    if x >= 0 or self.window.width() > 50:
                        self.window.resize(self.window.width() + x, self.window.height())
                    if y >= 0 or self.window.height() > 50:
                        self.window.resize(self.window.width(), self.window.height() + y)

        bottom_right_resize = BottomRightResize(frame, self)
        bottom_right_resize.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        bottom_right_resize.setGeometry(self.width()-5, self.height() - 5, 5, 5)
        bottom_right_resize.setCursor(QtGui.QCursor(QtCore.Qt.SizeFDiagCursor))
        self.bottom_right_resize = bottom_right_resize






    def resizeEvent(self, event):
        self.frame.setGeometry(0, 0, self.width(), self.height())
        self.move_label.setGeometry(0, 0, self.width(), 10)
        self.left_resize.setGeometry(0, 10, 5, self.height()-20)
        self.right_resize.setGeometry(self.width()-5, 10, 5, self.height()-20)
        self.bottom_resize.setGeometry(10, self.height()-5, self.width()-20, 5)
        self.bottom_left_resize.setGeometry(0, self.height() - 5, 5, 5)
        self.bottom_right_resize.setGeometry(self.width()-5, self.height() - 5, 5, 5)










if __name__ == '__main__':
    app = QApplication(sys.argv)
    notes_app = NoteApp()
    notes_app.show()
    sys.exit(app.exec_())