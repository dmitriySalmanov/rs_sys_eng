import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator, QDoubleValidator, QIntValidator, QRegularExpressionValidator
from PyQt5.QtWidgets import QLineEdit
from ui_designe import *
from unit_conversion import *


class ConvertorBranch(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.convertor_ui = Ui_RosmaryCandA()
        self.convertor_ui.setupUi(self)

        # Валидаторы для lineEdit для сил и моментов
        validator = QRegExpValidator(QRegExp(r'\d*\.?\d+'))
        for line_edit in self.findChildren(QLineEdit):
            line_edit.setValidator(validator)

        # Подключаем обработчики изменения текста для сил
        self.convertor_ui.lineEdit_kg.textChanged.connect(lambda: self.convert_force('kg'))
        self.convertor_ui.lineEdit_kN.textChanged.connect(lambda: self.convert_force('kN'))
        self.convertor_ui.lineEdit_N.textChanged.connect(lambda: self.convert_force('N'))
        self.convertor_ui.lineEdit_mN.textChanged.connect(lambda: self.convert_force('mN'))
        self.convertor_ui.lineEdit_daN.textChanged.connect(lambda: self.convert_force('daN'))
        self.convertor_ui.lineEdit_ib.textChanged.connect(lambda: self.convert_force('ib'))
        self.convertor_ui.lineEdit_T.textChanged.connect(lambda: self.convert_force('T'))
        self.convertor_ui.lineEdit_MN.textChanged.connect(lambda: self.convert_force('MN'))
        self.convertor_ui.lineEdit_kip.textChanged.connect(lambda: self.convert_force('kip'))

        # Подключаем обработчики изменения текста для моментво
        self.convertor_ui.lineEdit_moment1.textChanged.connect(self.convert_moment)
        self.convertor_ui.lineEdit_moment2.textChanged.connect(self.convert_moment)
        self.convertor_ui.comboBox_moment_f1.currentIndexChanged.connect(self.convert_moment)
        self.convertor_ui.comboBox_moment_ld1.currentIndexChanged.connect(self.convert_moment)
        self.convertor_ui.comboBox_moment_f2.currentIndexChanged.connect(self.convert_moment)
        self.convertor_ui.comboBox_moment_ld2.currentIndexChanged.connect(self.convert_moment)

    def convert_force(self, unit):
        """
        -Описание: Метод обрабатывает lineEdit'ы, пересчитывает единицы измерения силы и выводит их в
        соответствующую строку
        -Принимает: key_force - str значение/флаг соответствующее конкретной единице измерения
        -Возвращает: Ничего
        """
        try:
            # Отключаем обработчики, чтобы избежать рекурсии
            for line_edit in self.convertor_ui.groupBox_force.findChildren(QLineEdit):
                line_edit.blockSignals(True)

            # Математический блок с проверкой по ключам
            value = float(getattr(self.convertor_ui, f"lineEdit_{unit}").text())
            if unit == 'kg':
                for line_edit in self.convertor_ui.groupBox_force.findChildren(QLineEdit):
                    if line_edit != self.convertor_ui.lineEdit_kg:
                        unit_name = line_edit.objectName().split('_')[-1]
                        line_edit.setText(f"{convert(value, unit, unit_name):.3f}")
            elif unit == 'kN':
                for line_edit in self.convertor_ui.groupBox_force.findChildren(QLineEdit):
                    if line_edit != self.convertor_ui.lineEdit_kN:
                        unit_name = line_edit.objectName().split('_')[-1]
                        line_edit.setText(f"{convert(value, unit, unit_name):.3f}")
            elif unit == 'N':
                for line_edit in self.convertor_ui.groupBox_force.findChildren(QLineEdit):
                    if line_edit != self.convertor_ui.lineEdit_N:
                        unit_name = line_edit.objectName().split('_')[-1]
                        line_edit.setText(f"{convert(value, unit, unit_name):.3f}")
            elif unit == 'mN':
                for line_edit in self.convertor_ui.groupBox_force.findChildren(QLineEdit):
                    if line_edit != self.convertor_ui.lineEdit_mN:
                        unit_name = line_edit.objectName().split('_')[-1]
                        line_edit.setText(f"{convert(value, unit, unit_name):.3f}")
            elif unit == 'daN':
                for line_edit in self.convertor_ui.groupBox_force.findChildren(QLineEdit):
                    if line_edit != self.convertor_ui.lineEdit_daN:
                        unit_name = line_edit.objectName().split('_')[-1]
                        line_edit.setText(f"{convert(value, unit, unit_name):.3f}")
            elif unit == 'ib':
                for line_edit in self.convertor_ui.groupBox_force.findChildren(QLineEdit):
                    if line_edit != self.convertor_ui.lineEdit_ib:
                        unit_name = line_edit.objectName().split('_')[-1]
                        line_edit.setText(f"{convert(value, unit, unit_name):.3f}")
            elif unit == 'T':
                for line_edit in self.convertor_ui.groupBox_force.findChildren(QLineEdit):
                    if line_edit != self.convertor_ui.lineEdit_T:
                        unit_name = line_edit.objectName().split('_')[-1]
                        line_edit.setText(f"{convert(value, unit, unit_name):.3f}")
            elif unit == 'MN':
                for line_edit in self.convertor_ui.groupBox_force.findChildren(QLineEdit):
                    if line_edit != self.convertor_ui.lineEdit_MN:
                        unit_name = line_edit.objectName().split('_')[-1]
                        line_edit.setText(f"{convert(value, unit, unit_name):.3f}")
            elif unit == 'kip':
                for line_edit in self.convertor_ui.groupBox_force.findChildren(QLineEdit):
                    if line_edit != self.convertor_ui.lineEdit_kip:
                        unit_name = line_edit.objectName().split('_')[-1]
                        line_edit.setText(f"{convert(value, unit, unit_name):.3f}")


        except ValueError:
            # Очищаем все поля
            for line_edit in self.convertor_ui.groupBox_force.findChildren(QLineEdit):
                line_edit.clear()

        finally:
            # Возвращаем обработчики
            for line_edit in self.convertor_ui.groupBox_force.findChildren(QLineEdit):
                line_edit.blockSignals(False)

    def convert_moment(self):
        """
        -Описание: Метод обрабатывает lineEdit'ы моментво сил, пересчитывает единицы измерения моментво и выводит их в
        соответствующую строку
        -Принимает: Ничего
        -Возвращает: Ничего
        """
        length_measurement = {'m': 1, 'cm': 100, 'mm': 1000, 'inch': 39.37008, 'foot': 3.28084}

        try:
            # Отключаем обработчики, чтобы избежать рекурсии
            self.convertor_ui.lineEdit_moment1.blockSignals(True)
            self.convertor_ui.lineEdit_moment2.blockSignals(True)

            # Получаем входные данные
            moment_input = float(self.convertor_ui.lineEdit_moment1.text())

            force_input = self.convertor_ui.comboBox_moment_f1.currentText()
            linear_dimension_input = self.convertor_ui.comboBox_moment_ld1.currentText()

            force_output = self.convertor_ui.comboBox_moment_f2.currentText()
            linear_dimension_output = self.convertor_ui.comboBox_moment_ld2.currentText()

            # Если входные и выходные единицы одинаковы — просто копируем значение
            if force_input == force_output and linear_dimension_input == linear_dimension_output:
                self.convertor_ui.lineEdit_moment2.setText(f"{moment_input:.3f}")
                return  # Досрочно завершаем метод

            # Обработка перевода моментов сил
            moment_output = (convert(moment_input, force_input, force_output) *
                             (length_measurement[linear_dimension_output] /
                              length_measurement[linear_dimension_input]))
            self.convertor_ui.lineEdit_moment2.setText(f"{moment_output:.3f}")

        except ValueError:
            # Очищаем все поля
            self.convertor_ui.lineEdit_moment1.clear()
            self.convertor_ui.lineEdit_moment2.clear()

        finally:
            # Включаем обработчики обратно
            self.convertor_ui.lineEdit_moment1.blockSignals(False)
            self.convertor_ui.lineEdit_moment2.blockSignals(False)
