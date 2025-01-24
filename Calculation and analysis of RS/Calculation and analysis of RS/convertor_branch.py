import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator, QDoubleValidator, QIntValidator
from PyQt5.QtWidgets import QLineEdit
from des import *


class ConvertorBranch(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.convertor_ui = Ui_MainWindow()
        self.convertor_ui.setupUi(self)

        # Валидаторы для lineEdit
        validator = QRegExpValidator(QRegExp(r'\d*\.?\d+'))
        self.convertor_ui.lineEdit_kg.setValidator(validator)
        self.convertor_ui.lineEdit_kN.setValidator(validator)
        self.convertor_ui.lineEdit_N.setValidator(validator)

        # Подключаем обработчики изменения текста
        self.convertor_ui.lineEdit_kg.textChanged.connect(lambda: self.convert_force('kg'))
        self.convertor_ui.lineEdit_kN.textChanged.connect(lambda: self.convert_force('kN'))
        self.convertor_ui.lineEdit_N.textChanged.connect(lambda: self.convert_force('N'))

    def convert_force(self, key_force):
        """
        -Описание: Метод обрабатывает lineEdit'ы, пересчитывает единицы измерения силы и выводит их в соответствующую строку
        -Принимает: key_force - str значение/флаг соответствующее конкретной единице измерения
        -Возвращает: Ничего
        """
        g = 9.80665
        try:
            # Отключаем обработчики, чтобы избежать рекурсии
            self.convertor_ui.lineEdit_kg.blockSignals(True)
            self.convertor_ui.lineEdit_kN.blockSignals(True)
            self.convertor_ui.lineEdit_N.blockSignals(True)

            if key_force == 'kg':
                value_kg = float(self.convertor_ui.lineEdit_kg.text())
                kn = (value_kg * g) / 1000
                n = value_kg * g
                self.convertor_ui.lineEdit_kN.setText(f"{kn:.2f}")
                self.convertor_ui.lineEdit_N.setText(f"{n:.2f}")
            elif key_force == 'kN':
                value_kn = float(self.convertor_ui.lineEdit_kN.text())
                kg = (value_kn * 1000) / g
                n = value_kn * 1000
                self.convertor_ui.lineEdit_kg.setText(f"{kg:.2f}")
                self.convertor_ui.lineEdit_N.setText(f"{n:.2f}")
            elif key_force == 'N':
                value_n = float(self.convertor_ui.lineEdit_N.text())
                kg = value_n / g
                kn = value_n / 1000
                self.convertor_ui.lineEdit_kg.setText(f"{kg:.2f}")
                self.convertor_ui.lineEdit_kN.setText(f"{kn:.2f}")
        except ValueError:
            # Очищаем только текущее поле
            if key_force == 'kg':
                self.convertor_ui.lineEdit_kg.clear()
            elif key_force == 'kN':
                self.convertor_ui.lineEdit_kN.clear()
            elif key_force == 'N':
                self.convertor_ui.lineEdit_N.clear()
        finally:
            # Возвращаем обработчики
            self.convertor_ui.lineEdit_kg.blockSignals(False)
            self.convertor_ui.lineEdit_kN.blockSignals(False)
            self.convertor_ui.lineEdit_N.blockSignals(False)
