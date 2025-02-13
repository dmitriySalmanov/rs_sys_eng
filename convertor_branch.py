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
        self.setStyleSheet("QMainWindow { background-image:"
                           " url(D:/Projects/Calculation and analysis of RS/resources/background.jpeg); }")

        # Валидаторы для lineEdit
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

        # Подключаем обработчики изменения текста для давлений
        self.convertor_ui.comboBox_pressure_f1.currentIndexChanged.connect(lambda: self.convert_pressure('pressure_1'))
        self.convertor_ui.comboBox_pressure_qd1.currentIndexChanged.connect(lambda: self.convert_pressure('pressure_1'))
        self.convertor_ui.comboBox_pressure_f2.currentIndexChanged.connect(lambda: self.convert_pressure('pressure_1'))
        self.convertor_ui.comboBox_pressure_qd2.currentIndexChanged.connect(lambda: self.convert_pressure('pressure_1'))
        self.convertor_ui.lineEdit_pressure_1.textChanged.connect(lambda: self.convert_pressure('pressure_1'))
        self.convertor_ui.lineEdit_pressure_2.textChanged.connect(lambda: self.convert_pressure('pressure_1'))
        self.convertor_ui.lineEdit_pressure_3.textChanged.connect(lambda: self.convert_pressure('pressure_3'))
        self.convertor_ui.lineEdit_pressure_4.textChanged.connect(lambda: self.convert_pressure('pressure_4'))
        self.convertor_ui.lineEdit_pressure_5.textChanged.connect(lambda: self.convert_pressure('pressure_5'))

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

    def convert_pressure(self, key):
        length_measurement = {'m²': 1 ** 2, 'cm²': 100 ** 2, 'mm²': 1000 ** 2, 'inch²': 39.37008 ** 2,
                              'foot²': 3.28084 ** 2}

        try:
            # Отключаем обработчики, чтобы избежать рекурсии
            for line_edit in self.convertor_ui.groupBox_pressure.findChildren(QLineEdit):
                line_edit.blockSignals(True)

            pressure_input = float(getattr(self.convertor_ui, f"lineEdit_{key}").text())

            force_input = self.convertor_ui.comboBox_pressure_f1.currentText()
            quadratic_dimension_input = self.convertor_ui.comboBox_pressure_qd1.currentText()

            force_output = self.convertor_ui.comboBox_pressure_f2.currentText()
            quadratic_dimension_output = self.convertor_ui.comboBox_pressure_qd2.currentText()

            # Математический блок с проверкой по ключам
            if key == 'pressure_1':
                # Если входные и выходные единицы одинаковы — просто копируем значение
                if force_input == force_output and quadratic_dimension_input == quadratic_dimension_output:
                    self.convertor_ui.lineEdit_pressure_2.setText(f"{pressure_input:.3f}")

                pressure_output = (convert(pressure_input, force_input, force_output) / (
                            length_measurement[quadratic_dimension_output] / length_measurement[
                        quadratic_dimension_input]))
                self.convertor_ui.lineEdit_pressure_2.setText(f"{pressure_output:.3f}")

                pressure_output_MPa = (convert(pressure_input, force_input, 'N') / (
                            length_measurement['mm²'] / length_measurement[quadratic_dimension_input]))
                self.convertor_ui.lineEdit_pressure_5.setText(f"{pressure_output_MPa:.3f}")

                pressure_output_kPa = pressure_output_MPa * 1000
                self.convertor_ui.lineEdit_pressure_4.setText(f"{pressure_output_kPa:.3f}")

                pressure_output_Pa = pressure_output_MPa * 1000000
                self.convertor_ui.lineEdit_pressure_3.setText(f"{pressure_output_Pa:.3f}")

            if key == 'pressure_3':  # Pa
                pressure_output_MPa = pressure_input / 1000000
                self.convertor_ui.lineEdit_pressure_5.setText(f"{pressure_output_MPa:.3f}")

                pressure_output_kPa = pressure_output_MPa * 1000
                self.convertor_ui.lineEdit_pressure_4.setText(f"{pressure_output_kPa:.3f}")

                pressure_output_first_line = (convert(pressure_output_MPa * 1e6, 'N', force_input) *
                                              (1 / length_measurement[quadratic_dimension_input]))
                self.convertor_ui.lineEdit_pressure_1.setText(f"{pressure_output_first_line:.3f}")

                pressure_output_second_line = (convert(pressure_output_MPa * 1e6, 'N', force_output) *
                                               (1 / length_measurement[quadratic_dimension_output]))
                self.convertor_ui.lineEdit_pressure_2.setText(f"{pressure_output_second_line:.3f}")

            if key == 'pressure_4':  # kPa
                pressure_output_MPa = pressure_input / 1000
                self.convertor_ui.lineEdit_pressure_5.setText(f"{pressure_output_MPa:.3f}")

                pressure_output_Pa = pressure_output_MPa * 1000000
                self.convertor_ui.lineEdit_pressure_3.setText(f"{pressure_output_Pa:.3f}")

                pressure_output_first_line = (convert(pressure_output_MPa * 1e6, 'N', force_input) *
                                              (1 / length_measurement[quadratic_dimension_input]))
                self.convertor_ui.lineEdit_pressure_1.setText(f"{pressure_output_first_line:.3f}")

                pressure_output_second_line = (convert(pressure_output_MPa * 1e6, 'N', force_output) *
                                               (1 / length_measurement[quadratic_dimension_output]))
                self.convertor_ui.lineEdit_pressure_2.setText(f"{pressure_output_second_line:.3f}")

            if key == 'pressure_5':  # MPa
                pressure_output_kPa = pressure_input * 1000
                self.convertor_ui.lineEdit_pressure_4.setText(f"{pressure_output_kPa:.3f}")

                pressure_output_Pa = pressure_output_kPa * 1000
                self.convertor_ui.lineEdit_pressure_3.setText(f"{pressure_output_Pa:.3f}")

                pressure_output_first_line = (convert(pressure_input * 1e6, 'N', force_input) *
                                              (1 / length_measurement[quadratic_dimension_input]))
                self.convertor_ui.lineEdit_pressure_1.setText(f"{pressure_output_first_line:.3f}")

                pressure_output_second_line = (convert(pressure_input * 1e6, 'N', force_output) *
                                               (1 / length_measurement[quadratic_dimension_output]))
                self.convertor_ui.lineEdit_pressure_2.setText(f"{pressure_output_second_line:.3f}")

        except ValueError:
            # Очищаем все поля
            for line_edit in self.convertor_ui.groupBox_pressure.findChildren(QLineEdit):
                line_edit.clear()

        finally:
            # Возвращаем обработчики
            for line_edit in self.convertor_ui.groupBox_pressure.findChildren(QLineEdit):
                line_edit.blockSignals(False)
