import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator, QDoubleValidator, QIntValidator
from PyQt5.QtWidgets import QLineEdit
from des import *


class ConvertorBranch(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.convertor_ui = Ui_RosmaryCandA()
        self.convertor_ui.setupUi(self)

        # Валидаторы для lineEdit
        validator = QRegExpValidator(QRegExp(r'\d*\.?\d+'))
        self.convertor_ui.lineEdit_kg.setValidator(validator)
        self.convertor_ui.lineEdit_kN.setValidator(validator)
        self.convertor_ui.lineEdit_N.setValidator(validator)
        self.convertor_ui.lineEdit_mN.setValidator(validator)
        self.convertor_ui.lineEdit_daN.setValidator(validator)
        self.convertor_ui.lineEdit_ib.setValidator(validator)
        self.convertor_ui.lineEdit_T.setValidator(validator)
        self.convertor_ui.lineEdit_MN.setValidator(validator)
        self.convertor_ui.lineEdit_kip.setValidator(validator)

        # Подключаем обработчики изменения текста
        self.convertor_ui.lineEdit_kg.textChanged.connect(lambda: self.convert_force('kg'))
        self.convertor_ui.lineEdit_kN.textChanged.connect(lambda: self.convert_force('kN'))
        self.convertor_ui.lineEdit_N.textChanged.connect(lambda: self.convert_force('N'))
        self.convertor_ui.lineEdit_mN.textChanged.connect(lambda: self.convert_force('mN'))
        self.convertor_ui.lineEdit_daN.textChanged.connect(lambda: self.convert_force('daN'))
        self.convertor_ui.lineEdit_ib.textChanged.connect(lambda: self.convert_force('ib'))
        self.convertor_ui.lineEdit_T.textChanged.connect(lambda: self.convert_force('T'))
        self.convertor_ui.lineEdit_MN.textChanged.connect(lambda: self.convert_force('MN'))
        self.convertor_ui.lineEdit_kip.textChanged.connect(lambda: self.convert_force('kip'))

    def convert_force(self, key_force):
        """
        -Описание: Метод обрабатывает lineEdit'ы, пересчитывает единицы измерения силы и выводит их в соответствующую строку
        -Принимает: key_force - str значение/флаг соответствующее конкретной единице измерения
        -Возвращает: Ничего
        """
        g = 9.80665
        ib_const = 2.20462
        kgf = 453.59237
        try:
            # Отключаем обработчики, чтобы избежать рекурсии
            self.convertor_ui.lineEdit_kg.blockSignals(True)
            self.convertor_ui.lineEdit_kN.blockSignals(True)
            self.convertor_ui.lineEdit_N.blockSignals(True)
            self.convertor_ui.lineEdit_mN.blockSignals(True)
            self.convertor_ui.lineEdit_daN.blockSignals(True)
            self.convertor_ui.lineEdit_ib.blockSignals(True)
            self.convertor_ui.lineEdit_T.blockSignals(True)
            self.convertor_ui.lineEdit_MN.blockSignals(True)
            self.convertor_ui.lineEdit_kip.blockSignals(True)

            if key_force == 'kg':
                kg = float(self.convertor_ui.lineEdit_kg.text())
                kn = (kg * g) / 1000
                n = kg * g
                mn = n * 1000
                dan = n / 10
                ib = kg * ib_const
                t = kg / 1000
                mil_n = n / 10**6
                kip = kg / kgf
                self.convertor_ui.lineEdit_kN.setText(f"{kn:.2f}")
                self.convertor_ui.lineEdit_N.setText(f"{n:.2f}")
                self.convertor_ui.lineEdit_mN.setText(f"{mn:.2f}")
                self.convertor_ui.lineEdit_daN.setText(f"{dan:.2f}")
                self.convertor_ui.lineEdit_ib.setText(f"{ib:.2f}")
                self.convertor_ui.lineEdit_T.setText(f"{t:.2f}")
                self.convertor_ui.lineEdit_MN.setText(f"{mil_n:.2f}")
                self.convertor_ui.lineEdit_kip.setText(f"{kip:.2f}")
            elif key_force == 'kN':
                kn = float(self.convertor_ui.lineEdit_kN.text())
                kg = (kn * 1000) / g
                n = kn * 1000
                mn = n * 1000
                dan = n / 10
                ib = kg * ib_const
                t = kg / 1000
                mil_n = n / 10**6
                kip = kg / kgf
                self.convertor_ui.lineEdit_kg.setText(f"{kg:.2f}")
                self.convertor_ui.lineEdit_N.setText(f"{n:.2f}")
                self.convertor_ui.lineEdit_mN.setText(f"{mn:.2f}")
                self.convertor_ui.lineEdit_daN.setText(f"{dan:.2f}")
                self.convertor_ui.lineEdit_ib.setText(f"{ib:.2f}")
                self.convertor_ui.lineEdit_T.setText(f"{t:.2f}")
                self.convertor_ui.lineEdit_MN.setText(f"{mil_n:.2f}")
                self.convertor_ui.lineEdit_kip.setText(f"{kip:.2f}")
            elif key_force == 'N':
                n = float(self.convertor_ui.lineEdit_N.text())
                kg = n / g
                kn = n / 1000
                mn = n * 1000
                dan = n / 10
                ib = kg * ib_const
                t = kg / 1000
                mil_n = n / 10**6
                kip = kg / kgf
                self.convertor_ui.lineEdit_kg.setText(f"{kg:.2f}")
                self.convertor_ui.lineEdit_kN.setText(f"{kn:.2f}")
                self.convertor_ui.lineEdit_mN.setText(f"{mn:.2f}")
                self.convertor_ui.lineEdit_daN.setText(f"{dan:.2f}")
                self.convertor_ui.lineEdit_ib.setText(f"{ib:.2f}")
                self.convertor_ui.lineEdit_T.setText(f"{t:.2f}")
                self.convertor_ui.lineEdit_MN.setText(f"{mil_n:.2f}")
                self.convertor_ui.lineEdit_kip.setText(f"{kip:.2f}")
            elif key_force == 'mN':
                mn = float(self.convertor_ui.lineEdit_mN.text())
                kg = (mn / 1000) / g
                n = kg * g
                kn = n / 1000
                dan = n / 10
                ib = kg * ib_const
                t = kg / 1000
                mil_n = n / 10**6
                kip = kg / kgf
                self.convertor_ui.lineEdit_kg.setText(f"{kg:.2f}")
                self.convertor_ui.lineEdit_N.setText(f"{n:.2f}")
                self.convertor_ui.lineEdit_kN.setText(f"{kn:.2f}")
                self.convertor_ui.lineEdit_daN.setText(f"{dan:.2f}")
                self.convertor_ui.lineEdit_ib.setText(f"{ib:.2f}")
                self.convertor_ui.lineEdit_T.setText(f"{t:.2f}")
                self.convertor_ui.lineEdit_MN.setText(f"{mil_n:.2f}")
                self.convertor_ui.lineEdit_kip.setText(f"{kip:.2f}")
            elif key_force == 'daN':
                dan = float(self.convertor_ui.lineEdit_daN.text())
                n = dan * 10
                kg = n / g
                kn = n / 1000
                mn = n * 1000
                ib = kg * ib_const
                t = kg / 1000
                mil_n = n / 10**6
                kip = kg / kgf
                self.convertor_ui.lineEdit_kg.setText(f"{kg:.2f}")
                self.convertor_ui.lineEdit_N.setText(f"{n:.2f}")
                self.convertor_ui.lineEdit_kN.setText(f"{kn:.2f}")
                self.convertor_ui.lineEdit_mN.setText(f"{mn:.2f}")
                self.convertor_ui.lineEdit_ib.setText(f"{ib:.2f}")
                self.convertor_ui.lineEdit_T.setText(f"{t:.2f}")
                self.convertor_ui.lineEdit_MN.setText(f"{mil_n:.2f}")
                self.convertor_ui.lineEdit_kip.setText(f"{kip:.2f}")
            elif key_force == 'ib':
                ib = float(self.convertor_ui.lineEdit_ib.text())
                kg = ib / ib_const
                n = kg * g
                kn = n / 1000
                mn = n * 1000
                dan = n / 10
                t = kg / 1000
                mil_n = n / 10**6
                kip = kg / kgf
                self.convertor_ui.lineEdit_kg.setText(f"{kg:.2f}")
                self.convertor_ui.lineEdit_N.setText(f"{n:.2f}")
                self.convertor_ui.lineEdit_kN.setText(f"{kn:.2f}")
                self.convertor_ui.lineEdit_mN.setText(f"{mn:.2f}")
                self.convertor_ui.lineEdit_daN.setText(f"{dan:.2f}")
                self.convertor_ui.lineEdit_T.setText(f"{t:.2f}")
                self.convertor_ui.lineEdit_MN.setText(f"{mil_n:.2f}")
                self.convertor_ui.lineEdit_kip.setText(f"{kip:.2f}")
            elif key_force == 'T':
                t = float(self.convertor_ui.lineEdit_T.text())
                kg = t * 1000
                n = kg * g
                kn = n / 1000
                mn = n * 1000
                dan = n / 10
                ib = kg * ib_const
                mil_n = n / 10**6
                kip = kg / kgf
                self.convertor_ui.lineEdit_kg.setText(f"{kg:.2f}")
                self.convertor_ui.lineEdit_N.setText(f"{n:.2f}")
                self.convertor_ui.lineEdit_kN.setText(f"{kn:.2f}")
                self.convertor_ui.lineEdit_mN.setText(f"{mn:.2f}")
                self.convertor_ui.lineEdit_daN.setText(f"{dan:.2f}")
                self.convertor_ui.lineEdit_ib.setText(f"{ib:.2f}")
                self.convertor_ui.lineEdit_MN.setText(f"{mil_n:.2f}")
                self.convertor_ui.lineEdit_kip.setText(f"{kip:.2f}")
            elif key_force == 'MN':
                mil_n = float(self.convertor_ui.lineEdit_MN.text())
                n = mil_n * 10**6
                kg = n / g
                kn = n / 1000
                mn = n * 1000
                dan = n / 10
                ib = kg * ib_const
                t = kg / 1000
                kip = kg / kgf
                self.convertor_ui.lineEdit_kg.setText(f"{kg:.2f}")
                self.convertor_ui.lineEdit_N.setText(f"{n:.2f}")
                self.convertor_ui.lineEdit_kN.setText(f"{kn:.2f}")
                self.convertor_ui.lineEdit_mN.setText(f"{mn:.2f}")
                self.convertor_ui.lineEdit_daN.setText(f"{dan:.2f}")
                self.convertor_ui.lineEdit_ib.setText(f"{ib:.2f}")
                self.convertor_ui.lineEdit_T.setText(f"{t:.2f}")
                self.convertor_ui.lineEdit_kip.setText(f"{kip:.2f}")
            elif key_force == 'kip':
                kip = float(self.convertor_ui.lineEdit_kip.text())
                kg = kip * kgf
                n = kg * g
                kn = n / 1000
                mn = n * 1000
                dan = n / 10
                ib = kg * ib_const
                t = kg / 1000
                mil_n = n / 10**6
                self.convertor_ui.lineEdit_kg.setText(f"{kg:.2f}")
                self.convertor_ui.lineEdit_N.setText(f"{n:.2f}")
                self.convertor_ui.lineEdit_kN.setText(f"{kn:.2f}")
                self.convertor_ui.lineEdit_mN.setText(f"{mn:.2f}")
                self.convertor_ui.lineEdit_daN.setText(f"{dan:.2f}")
                self.convertor_ui.lineEdit_ib.setText(f"{ib:.2f}")
                self.convertor_ui.lineEdit_T.setText(f"{t:.2f}")
                self.convertor_ui.lineEdit_MN.setText(f"{mil_n:.2f}")
        except ValueError:
            # Очищаем все поля
            self.convertor_ui.lineEdit_kg.clear()
            self.convertor_ui.lineEdit_kN.clear()
            self.convertor_ui.lineEdit_N.clear()
            self.convertor_ui.lineEdit_mN.clear()
            self.convertor_ui.lineEdit_daN.clear()
            self.convertor_ui.lineEdit_ib.clear()
            self.convertor_ui.lineEdit_T.clear()
            self.convertor_ui.lineEdit_MN.clear()
            self.convertor_ui.lineEdit_kip.clear()
        finally:
            # Возвращаем обработчики
            self.convertor_ui.lineEdit_kg.blockSignals(False)
            self.convertor_ui.lineEdit_kN.blockSignals(False)
            self.convertor_ui.lineEdit_N.blockSignals(False)
            self.convertor_ui.lineEdit_mN.blockSignals(False)
            self.convertor_ui.lineEdit_daN.blockSignals(False)
            self.convertor_ui.lineEdit_ib.blockSignals(False)
            self.convertor_ui.lineEdit_T.blockSignals(False)
            self.convertor_ui.lineEdit_MN.blockSignals(False)
            self.convertor_ui.lineEdit_kip.blockSignals(False)
