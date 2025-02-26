import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator, QDoubleValidator, QIntValidator
from PyQt5.QtWidgets import QLineEdit, QMainWindow, QStackedWidget, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from ui_designe import *
from convertor_branch import ConvertorBranch
from stifness_analyze import StifnessBranch


class MainApplication(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # Загружаем интерфейс из ui_designe.py
        self.ui = Ui_RosmaryCandA()
        self.ui.setupUi(self)

        # Валидаторы для lineEdit
        validator = QRegExpValidator(QRegExp(r'\d*\.?\d+'))
        for line_edit in self.findChildren(QLineEdit):
            line_edit.setValidator(validator)

        # Создаем экземпляры классов и передаем им интерфейс
        self.convertor_branch = ConvertorBranch()
        self.stifness_branch = StifnessBranch()

        # Подключаем интерфейс к классам
        self.convertor_branch.convertor_ui = self.ui  # Передаем интерфейс конвертера
        self.stifness_branch.stifness_analyze_ui = self.ui  # Передаем интерфейс анализа жесткости

        # Инициализируем логику
        self.convertor_branch.setup_connections()
        self.stifness_branch.setup_connections()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainApplication()
    window.show()
    sys.exit(app.exec_())
