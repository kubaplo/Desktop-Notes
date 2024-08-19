from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys, time, getpass, os, re


class Autostart:
    def __init__(self):
        self.path = sys.argv[0].replace("/", "\\")
        self.dest_path = f"C:/Users/{getpass.getuser()}/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup/"

        # Always pass data to files in encoded (bytes) format. If not - errors with non-ascii chars may occur!
        # File mode  >chcp 65001<  is needed (!) to properly handle non-ascii chars (which may appear in .bat file path)
        self.filecontent = "@echo off\n" \
                           "chcp 65001\n" \
                           f"IF EXIST \"{self.path}\" (" \
                           f"START \"\" \"{self.path}\")".encode()

        if not self.autostart_exists():
            self.create_autostart()


    def create_autostart(self):
        filename = "DesktopNotes.bat"

        with open(self.dest_path + filename, "wb") as file:
            file.write(self.filecontent)


    def autostart_exists(self):
        exists = False

        with os.scandir(self.dest_path) as scan:
            for file in scan:
                if ".bat" in file.name:
                    try:
                        with open(self.dest_path + file.name, "rb") as temp:
                            data = temp.read()

                        if data == self.filecontent:
                            exists = True
                            break
                    except:
                        pass

        return exists



class SettingsWindow(QMainWindow):
    def __init__(self, position, size, conf, all_widgets, available_fonts):
        super().__init__()
        self.path = "/".join(sys.argv[0].replace("\\", "/").split("/")[:-1])
        self.main_position = position
        self.main_size = size
        self.configuration = conf
        self.all_widgets = all_widgets
        self.available_fonts = available_fonts
        self.setup()


    def setup(self):
        self.setWindowTitle("Settings")
        self.setWindowIcon(QtGui.QIcon(f"{self.path}/Icons/settings_icon.png"))
        self.setStyleSheet("background-color: #444")
        self.resize(300, 280)
        self.setFixedSize(self.size())

        if self.main_position[0] - self.width() - 20 < 0:
            self.move(self.main_position[0] + self.main_size[0] + 20, self.main_position[1])

        else:
            self.move(self.main_position[0] - self.width() - 20, self.main_position[1])

        self.create_widgets()


    def create_widgets(self):
        font = QtGui.QFont()
        font.setFamily("Bahnschrift")
        font.setPointSize(10)

        class ColorLabel(QtWidgets.QLabel):
            def __init__(self, init, conf, key, all):
                super().__init__(init)
                self.path = "/".join(sys.argv[0].replace("\\", "/").split("/")[:-1])
                self.configuration = conf
                self.key = key
                self.all_widgets = all

            def mousePressEvent(self, event):
                if event.button() == QtCore.Qt.LeftButton:
                    color = QtWidgets.QColorDialog(self)
                    color = color.getColor()
                    if color.isValid():
                        self.configuration[self.key] = color.name()
                        self.setStyleSheet(f"border: 2px solid #4C4A48; border-radius: 10px; background-color: {color.name()}")
                        if self.key == "background":
                            command = f"background-color: {self.configuration['background']}"
                        elif self.key == "border":
                            command = f"border: 2px solid {self.configuration['border']}"
                            self.all_widgets['move_label'](f"border: none; background-color: {self.configuration['border']}")
                        elif self.key == "font_color":
                            command = f"border: none; color: {self.configuration['font_color']}"


                        self.all_widgets[self.key](command)

                        with open(f"{self.path}/conf.data", "w") as file:
                            for key in self.configuration:
                                file.write(key)
                                file.write(":")
                                file.write(self.configuration[key])
                                file.write("\n")


        def row(i, title, key_name, type="color"):
            label = QtWidgets.QLabel(self)
            label.setFocus(True)
            label.setText(title)
            label.setFont(font)
            label.adjustSize()
            label.move(5, 10 + 40*i)

            if type == "color":
                color_box = ColorLabel(self, self.configuration, key_name, self.all_widgets)
                color_box.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                color_box.setStyleSheet(f"border: 2px solid #4C4A48; border-radius: 10px; background-color: {self.configuration[key_name]}")
                color_box.resize(70, 25)
                color_box.move(5 + label.width() + 10, 10 + 40*i)

            elif type == "value":
                class CustomInput(QtWidgets.QLineEdit):
                    digits = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
                    def __init__(self, init, all, conf):
                        super().__init__(init)
                        self.path = "/".join(sys.argv[0].replace("\\", "/").split("/")[:-1])
                        self.all_widgets = all
                        self.configuration = conf


                    def keyPressEvent(self, event):
                        if event.text() in self.digits:
                            super().keyPressEvent(event)
                            if self.text() and 1 <= int(self.text()) <= 200:
                                self.configuration['font_size'] = self.text()
                                self.all_widgets['font_size']()

                            with open(f"{self.path}/conf.data", "w") as file:
                                for key in self.configuration:
                                    file.write(key)
                                    file.write(":")
                                    file.write(self.configuration[key])
                                    file.write("\n")

                        elif event.key() == QtCore.Qt.Key_Backspace:
                            super().keyPressEvent(event)
                            if self.text() and 1 <= int(self.text()) <= 200:
                                self.configuration['font_size'] = self.text()
                                self.all_widgets['font_size']()

                            with open(f"{self.path}/conf.data", "w") as file:
                                for key in self.configuration:
                                    file.write(key)
                                    file.write(":")
                                    file.write(self.configuration[key])
                                    file.write("\n")
                        else:
                            pass


                input = CustomInput(self, self.all_widgets, self.configuration)
                input.setStyleSheet("border: 2px solid #4C4A48")
                input.setText(self.configuration['font_size'])
                input.resize(70, 25)
                input.move(5 + label.width() + 10, 7 + 40*i)


            elif type == "combobox":
                box = QtWidgets.QComboBox(self)
                box.resize(200, box.height())
                box.move(5 + label.width() + 10, 7 + 40*i)

                for font_name in self.available_fonts:
                    box.addItem(font_name)

                box.setCurrentText(self.configuration['font_family'])

                def combobox_changed(signal):
                    self.configuration['font_family'] = signal
                    with open(f"{self.path}/conf.data", "w") as file:
                        for key in self.configuration:
                            file.write(key)
                            file.write(":")
                            file.write(self.configuration[key])
                            file.write("\n")
                    self.all_widgets['font_family']()

                box.currentTextChanged.connect(combobox_changed)


        row(0, "BACKGROUND:", "background")
        row(1, "BORDER:", "border")
        row(2, "FONT COLOR:", "font_color")
        row(3, "FONT SIZE:", "font_size", "value")
        row(4, "FONT FAMILY:", "font_family", "combobox")

        default_button = QtWidgets.QPushButton(self)
        default_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        default_button.resize(self.width()-100, 35)
        default_button.move(50, self.height()-default_button.height()-10)
        font = QtGui.QFont()
        font.setFamily("Bahnschrift")
        font.setPointSize(11)
        font.setBold(True)
        default_button.setFont(font)
        default_button.setText("DEFAULT SETTINGS")
        default_button.setStyleSheet("background-color: #4d4d4d")

        def set_default():
            self.configuration['size'] = "300,400"
            self.configuration['position'] = f"{1920-300-20},20"
            self.configuration['background'] = "#3f3f3f"
            self.configuration['border'] = "#323232"
            self.configuration['font_color'] = "#499c54"
            self.configuration['font_size'] = "20"
            self.configuration['font_family'] = "Bahnschrift Light"

            with open(f"{self.path}/conf.data", "w") as file:
                for key in self.configuration:
                    file.write(key)
                    file.write(":")
                    file.write(self.configuration[key])
                    file.write("\n")

            width, height = self.configuration['size'].split(",")
            self.all_widgets['main_window'].resize(int(width), int(height))

            x, y = self.configuration['position'].split(",")
            self.all_widgets['main_window'].move(int(x), int(y))

            self.all_widgets['background'](f"background-color: {self.configuration['background']}")
            self.all_widgets['border'](f"border: 2px solid {self.configuration['border']}")
            self.all_widgets['move_label'](f"border: none; background-color: {self.configuration['border']}")
            self.all_widgets['font_color'](f"border: none; color: {self.configuration['font_color']}")
            self.all_widgets['font_size']()   #This line changes 'font_family' too.

            self.close()


        default_button.clicked.connect(set_default)


    def closeEvent(self, event):
        """To prevent NoteApp from closing.
        When 'X' was pressed on SettingsWindow, NoteApp was closing right after that."""

        event.ignore()
        self.hide()


#########################################################

class NoteApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.all_widgets = {}
        self.path = "/".join(sys.argv[0].replace("\\", "/").split("/")[:-1])

        self.setup()


    def setup(self):
        self.load_data()
        x, y = self.configuration['position'].split(",")
        width, height = self.configuration['size'].split(",")

        self.setWindowTitle("Desktop Notes")
        self.setGeometry(int(x), int(y), int(width), int(height))   #Default: 100, 100, 400, 600
        self.setWindowFlags(QtCore.Qt.ToolTip | QtCore.Qt.WindowStaysOnBottomHint)
        self.setStyleSheet(f"border: 2px solid {self.configuration['border']}")
        self.all_widgets['border'] = self.setStyleSheet
        self.all_widgets['main_window'] = self

        self.main_page()


    def load_data(self):
        #Need to check for available fonts here (in main window) and pass them to the SettingsWindow.
        #There are differences between available fonts in NoteApp window & SettingsWindow (two different types of windows).
        #QtGui.QFontDatabase().families() returns available fonts for window in which was called!
        self.available_fonts = QtGui.QFontDatabase().families()

        self.configuration = {}

        def get_default_settings():
            self.configuration = {}
            self.configuration['size'] = "300,400"
            self.configuration['position'] = f"{1920 - 300 - 20},20"
            self.configuration['background'] = "#3f3f3f"
            self.configuration['border'] = "#323232"
            self.configuration['font_color'] = "#499c54"
            self.configuration['font_size'] = "20"
            self.configuration['font_family'] = "Bahnschrift Light"
            self.configuration['text'] = "Create Your Note!"

            with open(f"{self.path}/conf.data", "w") as file:
                for key in self.configuration:
                    file.write(key)
                    file.write(":")
                    file.write(self.configuration[key])
                    file.write("\n")


        def validate():
            try:
                x, y = self.configuration['size'].split(",")
                x = int(x)
                y = int(y)
                if not (50 <= x <= 1920 and 50 <= y <= 1080):
                    self.configuration['size'] = "300,400"

            except KeyError:
                get_default_settings()
            except:
                self.configuration['size'] = "300,400"
            #--------------------------------------------------
            try:
                x, y = self.configuration['position'].split(",")
                x = int(x)
                y = int(y)
                if not (-40 < x < 1910 and -10 < y < 1070):
                    self.configuration['position'] = f"{1920 - 300 - 20},20"

            except KeyError:
                get_default_settings()
            except:
                self.configuration['position'] = f"{1920 - 300 - 20},20"
            #--------------------------------------------------
            pattern = re.compile("#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})")
            try:
                if not pattern.fullmatch(self.configuration['background']):
                    self.configuration['background'] = "#3f3f3f"
            except KeyError:
                get_default_settings()
            except:
                self.configuration['background'] = "#3f3f3f"
            try:
                if not pattern.fullmatch(self.configuration['border']):
                    self.configuration['border'] = "#323232"
            except KeyError:
                get_default_settings()
            except:
                self.configuration['border'] = "#323232"
            try:
                if not pattern.fullmatch(self.configuration['font_color']):
                    self.configuration['font_color'] = "#499c54"
            except KeyError:
                get_default_settings()
            except:
                self.configuration['font_color'] = "#499c54"
            #--------------------------------------------------
            try:
                x = self.configuration['font_size']
                x = int(x)
                if not (1 <= x <= 200):
                    self.configuration['font_size'] = "20"

            except KeyError:
                get_default_settings()
            except:
                self.configuration['font_size'] = "20"
            #--------------------------------------------------
            try:
                if not (self.configuration['font_family'] in self.available_fonts):
                    self.configuration['font_family'] = "Bahnschrift Light"
            except KeyError:
                get_default_settings()
            except:
                self.configuration['font_family'] = "Bahnschrift Light"




        if os.path.exists(f"{self.path}/conf.data"):
            try:
                with open(f"{self.path}/conf.data", "r") as file:
                    data = file.read()

                data = data.split("\n")[:-1]

                stop = False
                value = ""
                key = ""
                for line in data:
                    if key == "text":
                        stop = True
                        value += "\n" + line

                    if not stop:
                        key = line.split(":")[0]
                        value = ":".join(line.split(":")[1:])

                    self.configuration[key] = value

                validate()



            except:
                get_default_settings()


        else:
            get_default_settings()



    def main_page(self):
        frame = QtWidgets.QFrame(self)
        frame.setGeometry(0, 0, self.width(), self.height())
        frame.setStyleSheet(f"background-color: {self.configuration['background']}")
        self.all_widgets['background'] = frame.setStyleSheet
        self.frame = frame


        class MoveLabel(QtWidgets.QLabel):
            def __init__(self, init, main, function):
                super().__init__(init)
                self.holding = False
                self.window = main
                self.settings_window = function
                self.path = "/".join(sys.argv[0].replace("\\", "/").split("/")[:-1])

                self.create_buttons()


            def create_buttons(self):
                exit_button = QtWidgets.QPushButton(self)
                exit_button.setStyleSheet("border: none")
                exit_button.resize(30, 30)
                exit_button.setIcon(QtGui.QIcon(f"{self.path}/Icons/exit.png"))
                exit_button.setIconSize(QtCore.QSize(exit_button.width(), exit_button.height()))
                exit_button.setCursor(QtCore.Qt.PointingHandCursor)
                exit_button.clicked.connect(lambda: sys.exit())
                exit_button.hide()
                self.exit_button = exit_button

                settings_button = QtWidgets.QPushButton(self)
                settings_button.setStyleSheet("border: none")
                settings_button.resize(30, 30)
                settings_button.setCursor(QtCore.Qt.PointingHandCursor)
                settings_button.setIcon(QtGui.QIcon(f"{self.path}/Icons/settings.png"))
                settings_button.setIconSize(QtCore.QSize(settings_button.width(), settings_button.height()))
                settings_button.hide()
                settings_button.clicked.connect(self.settings_window)
                self.settings_button = settings_button


            def resizeEvent(self, event):
                self.exit_button.move(self.width()-self.exit_button.width()-5, 5)
                self.settings_button.move(self.width()-self.exit_button.width()-self.settings_button.width()-20, 5)


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

                    self.window.move(self.window.x() + x, self.window.y())
                    if self.window.y() + y > -10:
                        self.window.move(self.window.x(), self.window.y() + y)


            def enterEvent(self, event):
                self.resize(self.width(), 40)
                textbox.setGeometry(5, 40, self.window.width()-10, self.window.height()-45)
                self.exit_button.show()
                self.settings_button.show()


            def leaveEvent(self, event):
                self.resize(self.width(), 10)
                textbox.setGeometry(5, 10, self.window.width()-10, self.window.height()-15)
                self.exit_button.hide()
                self.settings_button.hide()


        def settings_window():
            position = (self.x(), self.y())
            size = (self.width(), self.height())
            self.settings_window = SettingsWindow(position, size, self.configuration, self.all_widgets, self.available_fonts)
            self.settings_window.show()


        move_label = MoveLabel(frame, self, settings_window)
        move_label.setGeometry(0, 0, self.width(), 10)
        move_label.setStyleSheet(f"border: none; background-color: {self.configuration['border']}")
        self.all_widgets['move_label'] = move_label.setStyleSheet
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

        ############################################################################

        class CustomTextInput(QtWidgets.QTextEdit):
            def __init__(self, init, conf):
                super().__init__(init)
                self.configuration = conf
                self.path = "/".join(sys.argv[0].replace("\\", "/").split("/")[:-1])


            def keyPressEvent(self, event):
                super().keyPressEvent(event)

                self.configuration["text"] = self.toPlainText()

                with open(f"{self.path}/conf.data", "w") as file:
                    for key in self.configuration:
                        file.write(key)
                        file.write(":")
                        file.write(self.configuration[key])
                        file.write("\n")


        textbox = CustomTextInput(frame, self.configuration)
        textbox.setGeometry(5, 10, self.width()-10, self.height()-15)
        textbox.setStyleSheet(f"border: none; color: {self.configuration['font_color']}")
        font = QtGui.QFont()
        font.setFamily(self.configuration['font_family'])
        font.setPointSize(int(self.configuration['font_size']))
        textbox.setFont(font)
        textbox.setText(self.configuration['text'])

        self.all_widgets['font_color'] = textbox.setStyleSheet

        def change_font_size():
            font = QtGui.QFont()
            font.setFamily(self.configuration['font_family'])
            font.setPointSize(int(self.configuration['font_size']))
            textbox.setFont(font)

        self.all_widgets['font_size'] = change_font_size
        self.all_widgets['font_family'] = change_font_size


        self.textbox = textbox



    def resizeEvent(self, event):
        self.frame.setGeometry(0, 0, self.width(), self.height())
        self.move_label.setGeometry(0, 0, self.width(), 10)
        self.left_resize.setGeometry(0, 10, 5, self.height()-20)
        self.right_resize.setGeometry(self.width()-5, 10, 5, self.height()-20)
        self.bottom_resize.setGeometry(10, self.height()-5, self.width()-20, 5)
        self.bottom_left_resize.setGeometry(0, self.height() - 5, 5, 5)
        self.bottom_right_resize.setGeometry(self.width()-5, self.height() - 5, 5, 5)
        self.textbox.setGeometry(5, 10, self.width()-10, self.height()-15)

        self.configuration['size'] = f"{self.width()},{self.height()}"

        with open(f"{self.path}/conf.data", "w") as file:
            for key in self.configuration:
                file.write(key)
                file.write(":")
                file.write(self.configuration[key])
                file.write("\n")



    def moveEvent(self, event):
        self.configuration['position'] = f"{self.x()},{self.y()}"

        with open(f"{self.path}/conf.data", "w") as file:
            for key in self.configuration:
                file.write(key)
                file.write(":")
                file.write(self.configuration[key])
                file.write("\n")





if __name__ == '__main__':
    # Uncomment to launch application on startup:
    #autostart = Autostart()

    app = QApplication(sys.argv)
    notes_app = NoteApp()
    notes_app.show()
    sys.exit(app.exec_())