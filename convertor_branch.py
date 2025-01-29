import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator, QDoubleValidator, QIntValidator
from PyQt5.QtWidgets import QLineEdit
from des import *
from unit_conversion import kN, N


class ConvertorBranch(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.convertor_ui = Ui_RosmaryCandA()
        self.convertor_ui.setupUi(self)

        # Валидаторы для lineEdit для сил
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

        # Валидаторы для lineEdit для моментов
        self.convertor_ui.lineEdit_moment1.setValidator(validator)
        self.convertor_ui.lineEdit_moment2.setValidator(validator)

        # Подключаем обработчики изменения текста для сил
        self.convertor_ui.lineEdit_kg.textChanged.connect(lambda: self.convert_force('кг'))
        self.convertor_ui.lineEdit_kN.textChanged.connect(lambda: self.convert_force('кН'))
        self.convertor_ui.lineEdit_N.textChanged.connect(lambda: self.convert_force('Н'))
        self.convertor_ui.lineEdit_mN.textChanged.connect(lambda: self.convert_force('мН'))
        self.convertor_ui.lineEdit_daN.textChanged.connect(lambda: self.convert_force('даН'))
        self.convertor_ui.lineEdit_ib.textChanged.connect(lambda: self.convert_force('фунт'))
        self.convertor_ui.lineEdit_T.textChanged.connect(lambda: self.convert_force('Т'))
        self.convertor_ui.lineEdit_MN.textChanged.connect(lambda: self.convert_force('МН'))
        self.convertor_ui.lineEdit_kip.textChanged.connect(lambda: self.convert_force('кип'))

        # Подключаем обработчики изменения текста для моментво
        self.convertor_ui.lineEdit_moment1.textChanged.connect(self.convert_moment)
        self.convertor_ui.lineEdit_moment2.textChanged.connect(self.convert_moment)
        self.convertor_ui.comboBox_moment_f1.currentIndexChanged.connect(self.convert_moment)
        self.convertor_ui.comboBox_moment_ld1.currentIndexChanged.connect(self.convert_moment)
        self.convertor_ui.comboBox_moment_f2.currentIndexChanged.connect(self.convert_moment)
        self.convertor_ui.comboBox_moment_ld2.currentIndexChanged.connect(self.convert_moment)

    def convert_force(self, key_force):
        """
        -Описание: Метод обрабатывает lineEdit'ы, пересчитывает единицы измерения силы и выводит их в
        соответствующую строку
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

            # Математический блок с проверкой по ключам
            if key_force == 'кг':
                kg = float(self.convertor_ui.lineEdit_kg.text())
                n = kg * g
                mn = n * 1000
                dan = n / 10
                ib = kg * ib_const
                t = kg / 1000
                mil_n = n / 10 ** 6
                kip = kg / kgf
                self.convertor_ui.lineEdit_kN.setText(f"{kN(kg, key_force):.2f}")
                self.convertor_ui.lineEdit_N.setText(f"{N(kg, key_force):.2f}")
                self.convertor_ui.lineEdit_mN.setText(f"{mn:.2f}")
                self.convertor_ui.lineEdit_daN.setText(f"{dan:.2f}")
                self.convertor_ui.lineEdit_ib.setText(f"{ib:.2f}")
                self.convertor_ui.lineEdit_T.setText(f"{t:.2f}")
                self.convertor_ui.lineEdit_MN.setText(f"{mil_n:.2f}")
                self.convertor_ui.lineEdit_kip.setText(f"{kip:.2f}")
            elif key_force == 'кН':
                kn = float(self.convertor_ui.lineEdit_kN.text())
                kg = (kn * 1000) / g
                n = kn * 1000
                mn = n * 1000
                dan = n / 10
                ib = kg * ib_const
                t = kg / 1000
                mil_n = n / 10 ** 6
                kip = kg / kgf
                self.convertor_ui.lineEdit_kg.setText(f"{kg:.2f}")
                self.convertor_ui.lineEdit_N.setText(f"{N(kn, key_force):.2f}")
                self.convertor_ui.lineEdit_mN.setText(f"{mn:.2f}")
                self.convertor_ui.lineEdit_daN.setText(f"{dan:.2f}")
                self.convertor_ui.lineEdit_ib.setText(f"{ib:.2f}")
                self.convertor_ui.lineEdit_T.setText(f"{t:.2f}")
                self.convertor_ui.lineEdit_MN.setText(f"{mil_n:.2f}")
                self.convertor_ui.lineEdit_kip.setText(f"{kip:.2f}")
            elif key_force == 'Н':
                n = float(self.convertor_ui.lineEdit_N.text())
                kg = n / g
                mn = n * 1000
                dan = n / 10
                ib = kg * ib_const
                t = kg / 1000
                mil_n = n / 10 ** 6
                kip = kg / kgf
                self.convertor_ui.lineEdit_kg.setText(f"{kg:.2f}")
                self.convertor_ui.lineEdit_kN.setText(f"{kN(n, key_force):.2f}")
                self.convertor_ui.lineEdit_mN.setText(f"{mn:.2f}")
                self.convertor_ui.lineEdit_daN.setText(f"{dan:.2f}")
                self.convertor_ui.lineEdit_ib.setText(f"{ib:.2f}")
                self.convertor_ui.lineEdit_T.setText(f"{t:.2f}")
                self.convertor_ui.lineEdit_MN.setText(f"{mil_n:.2f}")
                self.convertor_ui.lineEdit_kip.setText(f"{kip:.2f}")
            elif key_force == 'мН':
                mn = float(self.convertor_ui.lineEdit_mN.text())
                kg = (mn / 1000) / g
                n = kg * g
                dan = n / 10
                ib = kg * ib_const
                t = kg / 1000
                mil_n = n / 10 ** 6
                kip = kg / kgf
                self.convertor_ui.lineEdit_kg.setText(f"{kg:.2f}")
                self.convertor_ui.lineEdit_N.setText(f"{N(mn, key_force):.2f}")
                self.convertor_ui.lineEdit_kN.setText(f"{kN(mn, key_force):.2f}")
                self.convertor_ui.lineEdit_daN.setText(f"{dan:.2f}")
                self.convertor_ui.lineEdit_ib.setText(f"{ib:.2f}")
                self.convertor_ui.lineEdit_T.setText(f"{t:.2f}")
                self.convertor_ui.lineEdit_MN.setText(f"{mil_n:.2f}")
                self.convertor_ui.lineEdit_kip.setText(f"{kip:.2f}")
            elif key_force == 'даН':
                dan = float(self.convertor_ui.lineEdit_daN.text())
                n = dan * 10
                kg = n / g
                mn = n * 1000
                ib = kg * ib_const
                t = kg / 1000
                mil_n = n / 10 ** 6
                kip = kg / kgf
                self.convertor_ui.lineEdit_kg.setText(f"{kg:.2f}")
                self.convertor_ui.lineEdit_N.setText(f"{N(dan, key_force):.2f}")
                self.convertor_ui.lineEdit_kN.setText(f"{kN(dan, key_force):.2f}")
                self.convertor_ui.lineEdit_mN.setText(f"{mn:.2f}")
                self.convertor_ui.lineEdit_ib.setText(f"{ib:.2f}")
                self.convertor_ui.lineEdit_T.setText(f"{t:.2f}")
                self.convertor_ui.lineEdit_MN.setText(f"{mil_n:.2f}")
                self.convertor_ui.lineEdit_kip.setText(f"{kip:.2f}")
            elif key_force == 'фунт':
                ib = float(self.convertor_ui.lineEdit_ib.text())
                kg = ib / ib_const
                n = kg * g
                mn = n * 1000
                dan = n / 10
                t = kg / 1000
                mil_n = n / 10 ** 6
                kip = kg / kgf
                self.convertor_ui.lineEdit_kg.setText(f"{kg:.2f}")
                self.convertor_ui.lineEdit_N.setText(f"{N(ib, key_force):.2f}")
                self.convertor_ui.lineEdit_kN.setText(f"{kN(ib, key_force):.2f}")
                self.convertor_ui.lineEdit_mN.setText(f"{mn:.2f}")
                self.convertor_ui.lineEdit_daN.setText(f"{dan:.2f}")
                self.convertor_ui.lineEdit_T.setText(f"{t:.2f}")
                self.convertor_ui.lineEdit_MN.setText(f"{mil_n:.2f}")
                self.convertor_ui.lineEdit_kip.setText(f"{kip:.2f}")
            elif key_force == 'Т':
                t = float(self.convertor_ui.lineEdit_T.text())
                kg = t * 1000
                n = kg * g
                mn = n * 1000
                dan = n / 10
                ib = kg * ib_const
                mil_n = n / 10 ** 6
                kip = kg / kgf
                self.convertor_ui.lineEdit_kg.setText(f"{kg:.2f}")
                self.convertor_ui.lineEdit_N.setText(f"{N(t, key_force):.2f}")
                self.convertor_ui.lineEdit_kN.setText(f"{kN(t, key_force):.2f}")
                self.convertor_ui.lineEdit_mN.setText(f"{mn:.2f}")
                self.convertor_ui.lineEdit_daN.setText(f"{dan:.2f}")
                self.convertor_ui.lineEdit_ib.setText(f"{ib:.2f}")
                self.convertor_ui.lineEdit_MN.setText(f"{mil_n:.2f}")
                self.convertor_ui.lineEdit_kip.setText(f"{kip:.2f}")
            elif key_force == 'МН':
                mil_n = float(self.convertor_ui.lineEdit_MN.text())
                n = mil_n * 10 ** 6
                kg = n / g
                mn = n * 1000
                dan = n / 10
                ib = kg * ib_const
                t = kg / 1000
                kip = kg / kgf
                self.convertor_ui.lineEdit_kg.setText(f"{kg:.2f}")
                self.convertor_ui.lineEdit_N.setText(f"{N(mil_n, key_force):.2f}")
                self.convertor_ui.lineEdit_kN.setText(f"{kN(mil_n, key_force):.2f}")
                self.convertor_ui.lineEdit_mN.setText(f"{mn:.2f}")
                self.convertor_ui.lineEdit_daN.setText(f"{dan:.2f}")
                self.convertor_ui.lineEdit_ib.setText(f"{ib:.2f}")
                self.convertor_ui.lineEdit_T.setText(f"{t:.2f}")
                self.convertor_ui.lineEdit_kip.setText(f"{kip:.2f}")
            elif key_force == 'кип':
                kip = float(self.convertor_ui.lineEdit_kip.text())
                kg = kip * kgf
                n = kg * g
                mn = n * 1000
                dan = n / 10
                ib = kg * ib_const
                t = kg / 1000
                mil_n = n / 10 ** 6
                self.convertor_ui.lineEdit_kg.setText(f"{kg:.2f}")
                self.convertor_ui.lineEdit_N.setText(f"{N(kip, key_force):.2f}")
                self.convertor_ui.lineEdit_kN.setText(f"{kN(kip, key_force):.2f}")
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

    def convert_moment(self):
        """
        -Описание: Метод обрабатывает lineEdit'ы моментво сил, пересчитывает единицы измерения моментво и выводит их в
        соответствующую строку
        -Принимает: Ничего
        -Возвращает: Ничего
        """
        g = 9.80665
        ib_const = 2.20462
        kgf = 453.59237
        length_measurement = {'м': 1, 'см': 100, 'мм': 1000, 'дюйм': 39.37008, 'фут': 3.28084}
        try:
            # Отключаем обработчики, чтобы избежать рекурсии
            self.convertor_ui.lineEdit_moment1.blockSignals(True)
            self.convertor_ui.lineEdit_moment2.blockSignals(True)

            # Математический блок
            moment_value = float(self.convertor_ui.lineEdit_moment1.text())

            # Входящие значения (сила * длина)
            force_input = self.convertor_ui.comboBox_moment_f1.currentText()
            linear_dimension_input = self.convertor_ui.comboBox_moment_ld1.currentText()

            # Выходящие значения (сила * длина)
            force_output = self.convertor_ui.comboBox_moment_f2.currentText()
            linear_dimension_output = self.convertor_ui.comboBox_moment_ld2.currentText()

            # Оброботка кг в кН
            if force_input == 'кг' and linear_dimension_input == 'м':
                if force_output == 'кН' and linear_dimension_output == 'мм':
                    moment_output = kN(moment_value, force_input) * length_measurement[linear_dimension_output]
                    self.convertor_ui.lineEdit_moment2.setText(f"{moment_output:.2f}")
                elif force_output == 'кН' and linear_dimension_output == 'м':
                    moment_output = kN(moment_value, force_input) * length_measurement[linear_dimension_output]
                    self.convertor_ui.lineEdit_moment2.setText(f"{moment_output:.2f}")
                elif force_output == 'кН' and linear_dimension_output == 'см':
                    moment_output = kN(moment_value, force_input) * length_measurement[linear_dimension_output]
                    self.convertor_ui.lineEdit_moment2.setText(f"{moment_output:.2f}")
                elif force_output == 'кН' and linear_dimension_output == 'дюйм':
                    moment_output = kN(moment_value, force_input) * length_measurement[linear_dimension_output]
                    self.convertor_ui.lineEdit_moment2.setText(f"{moment_output:.2f}")
                elif force_output == 'кН' and linear_dimension_output == 'фут':
                    moment_output = kN(moment_value, force_input) * length_measurement[linear_dimension_output]
                    self.convertor_ui.lineEdit_moment2.setText(f"{moment_output:.2f}")

        except ValueError:
            # Очищаем все поля
            self.convertor_ui.lineEdit_moment1.clear()
            self.convertor_ui.lineEdit_moment2.clear()
        finally:
            # Возвращаем обработчики
            self.convertor_ui.lineEdit_moment1.blockSignals(False)
            self.convertor_ui.lineEdit_moment2.blockSignals(False)
