import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator, QDoubleValidator, QIntValidator
from PyQt5.QtWidgets import QLineEdit
from des import *
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
            for line_edit in self.findChildren(QLineEdit):
                if (line_edit != self.convertor_ui.lineEdit_moment1 and
                        line_edit != self.convertor_ui.lineEdit_moment2):
                    line_edit.blockSignals(True)

            # Математический блок с проверкой по ключам
            if unit == 'kg':
                kg = float(self.convertor_ui.lineEdit_kg.text())
                for line_edit in self.findChildren(QLineEdit):
                    if (line_edit != self.convertor_ui.lineEdit_kg and
                            line_edit != self.convertor_ui.lineEdit_moment1 and
                            line_edit != self.convertor_ui.lineEdit_moment2):
                        unit_name = line_edit.objectName().split('_')[-1]
                        line_edit.setText(f"{convert(kg, unit, unit_name):.2f}")
            elif unit == 'kN':
                kn = float(self.convertor_ui.lineEdit_kN.text())
                for line_edit in self.findChildren(QLineEdit):
                    if (line_edit != self.convertor_ui.lineEdit_kN and
                            line_edit != self.convertor_ui.lineEdit_moment1 and
                            line_edit != self.convertor_ui.lineEdit_moment2):
                        unit_name = line_edit.objectName().split('_')[-1]
                        line_edit.setText(f"{convert(kn, unit, unit_name):.2f}")
            elif unit == 'N':
                n = float(self.convertor_ui.lineEdit_N.text())
                for line_edit in self.findChildren(QLineEdit):
                    if (line_edit != self.convertor_ui.lineEdit_N and
                            line_edit != self.convertor_ui.lineEdit_moment1 and
                            line_edit != self.convertor_ui.lineEdit_moment2):
                        unit_name = line_edit.objectName().split('_')[-1]
                        line_edit.setText(f"{convert(n, unit, unit_name):.2f}")
            elif unit == 'mN':
                mn = float(self.convertor_ui.lineEdit_mN.text())
                for line_edit in self.findChildren(QLineEdit):
                    if (line_edit != self.convertor_ui.lineEdit_mN and
                            line_edit != self.convertor_ui.lineEdit_moment1 and
                            line_edit != self.convertor_ui.lineEdit_moment2):
                        unit_name = line_edit.objectName().split('_')[-1]
                        line_edit.setText(f"{convert(mn, unit, unit_name):.2f}")
            elif unit == 'daN':
                dan = float(self.convertor_ui.lineEdit_daN.text())
                for line_edit in self.findChildren(QLineEdit):
                    if (line_edit != self.convertor_ui.lineEdit_daN and
                            line_edit != self.convertor_ui.lineEdit_moment1 and
                            line_edit != self.convertor_ui.lineEdit_moment2):
                        unit_name = line_edit.objectName().split('_')[-1]
                        line_edit.setText(f"{convert(dan, unit, unit_name):.2f}")
            elif unit == 'ib':
                ib = float(self.convertor_ui.lineEdit_ib.text())
                for line_edit in self.findChildren(QLineEdit):
                    if (line_edit != self.convertor_ui.lineEdit_ib and
                            line_edit != self.convertor_ui.lineEdit_moment1 and
                            line_edit != self.convertor_ui.lineEdit_moment2):
                        unit_name = line_edit.objectName().split('_')[-1]
                        line_edit.setText(f"{convert(ib, unit, unit_name):.2f}")
            elif unit == 'T':
                t = float(self.convertor_ui.lineEdit_T.text())
                for line_edit in self.findChildren(QLineEdit):
                    if (line_edit != self.convertor_ui.lineEdit_T and
                            line_edit != self.convertor_ui.lineEdit_moment1 and
                            line_edit != self.convertor_ui.lineEdit_moment2):
                        unit_name = line_edit.objectName().split('_')[-1]
                        line_edit.setText(f"{convert(t, unit, unit_name):.2f}")
            elif unit == 'MN':
                mil_n = float(self.convertor_ui.lineEdit_MN.text())
                for line_edit in self.findChildren(QLineEdit):
                    if (line_edit != self.convertor_ui.lineEdit_MN and
                            line_edit != self.convertor_ui.lineEdit_moment1 and
                            line_edit != self.convertor_ui.lineEdit_moment2):
                        unit_name = line_edit.objectName().split('_')[-1]
                        line_edit.setText(f"{convert(mil_n, unit, unit_name):.2f}")
            elif unit == 'kip':
                kip = float(self.convertor_ui.lineEdit_kip.text())
                for line_edit in self.findChildren(QLineEdit):
                    if (line_edit != self.convertor_ui.lineEdit_kip and
                            line_edit != self.convertor_ui.lineEdit_moment1 and
                            line_edit != self.convertor_ui.lineEdit_moment2):
                        unit_name = line_edit.objectName().split('_')[-1]
                        line_edit.setText(f"{convert(kip, unit, unit_name):.2f}")

        except ValueError:
            # Очищаем все поля
            for line_edit in self.findChildren(QLineEdit):
                if (line_edit != self.convertor_ui.lineEdit_moment1 and
                        line_edit != self.convertor_ui.lineEdit_moment2):
                    line_edit.clear()

        finally:
            # Возвращаем обработчики
            for line_edit in self.findChildren(QLineEdit):
                if (line_edit != self.convertor_ui.lineEdit_moment1 and
                        line_edit != self.convertor_ui.lineEdit_moment2):
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
            moment_value = float(self.convertor_ui.lineEdit_moment1.text())

            force_input = self.convertor_ui.comboBox_moment_f1.currentText()
            linear_dimension_input = self.convertor_ui.comboBox_moment_ld1.currentText()

            force_output = self.convertor_ui.comboBox_moment_f2.currentText()
            linear_dimension_output = self.convertor_ui.comboBox_moment_ld2.currentText()

            # Если входные и выходные единицы одинаковы — просто копируем значение
            if force_input == force_output and linear_dimension_input == linear_dimension_output:
                self.convertor_ui.lineEdit_moment2.setText(f"{moment_value:.3f}")
                return  # Досрочно завершаем метод

            # Обработка перевода моментов сил
            moment_output = (convert(moment_value, force_input, force_output) *
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

        '''
        force_outputs = [self.convertor_ui.comboBox_moment_f1.itemText(i)
                         for i in range(self.convertor_ui.comboBox_moment_f1.count())]
        linear_dimension_outputs = [self.convertor_ui.comboBox_moment_ld1.itemText(i)
                                    for i in range(self.convertor_ui.comboBox_moment_ld1.count())]
        length_measurement = {'m': 1, 'cm': 100, 'mm': 1000, 'inch': 39.37008, 'foot': 3.28084}
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

            # Оброботка кг
            if force_input == 'kg' and linear_dimension_input == 'm':
                for force_out in force_outputs:
                    for linear_out in linear_dimension_outputs:
                        if force_output == force_out and linear_dimension_output == linear_out:
                            moment_output = (convert(moment_value, force_input, force_output)
                                             * length_measurement[linear_dimension_output])
                            self.convertor_ui.lineEdit_moment2.setText(f"{moment_output:.2f}")
                        elif force_input == force_output and linear_dimension_input == linear_dimension_output:
                            self.convertor_ui.lineEdit_moment2.setText(f"{moment_value:.2f}")
                            break


            """
            if force_input == 'kg' and linear_dimension_input == 'm':
                if force_output == 'kN' and linear_dimension_output == 'mm':
                    moment_output = (convert(moment_value, force_input, force_output)
                                     * length_measurement[linear_dimension_output])
                    self.convertor_ui.lineEdit_moment2.setText(f"{moment_output:.2f}")

                elif force_output == 'kN' and linear_dimension_output == 'm':
                    moment_output = (convert(moment_value, force_input, force_output)
                                     * length_measurement[linear_dimension_output])
                    self.convertor_ui.lineEdit_moment2.setText(f"{moment_output:.2f}")

                elif force_output == 'kN' and linear_dimension_output == 'cm':
                    moment_output = (convert(moment_value, force_input, force_output)
                                     * length_measurement[linear_dimension_output])
                    self.convertor_ui.lineEdit_moment2.setText(f"{moment_output:.2f}")

                elif force_output == 'kN' and linear_dimension_output == 'inch':
                    moment_output = (convert(moment_value, force_input, force_output)
                                     * length_measurement[linear_dimension_output])
                    self.convertor_ui.lineEdit_moment2.setText(f"{moment_output:.2f}")

                elif force_output == 'kN' and linear_dimension_output == 'foot':
                    moment_output = (convert(moment_value, force_input, force_output)
                                     * length_measurement[linear_dimension_output])
                    self.convertor_ui.lineEdit_moment2.setText(f"{moment_output:.2f}")

                if force_output == 'N' and linear_dimension_output == 'mm':
                    moment_output = (convert(moment_value, force_input, force_output)
                                     * length_measurement[linear_dimension_output])
                    self.convertor_ui.lineEdit_moment2.setText(f"{moment_output:.2f}")

                elif force_output == 'N' and linear_dimension_output == 'm':
                    moment_output = (convert(moment_value, force_input, force_output)
                                     * length_measurement[linear_dimension_output])
                    self.convertor_ui.lineEdit_moment2.setText(f"{moment_output:.2f}")

                elif force_output == 'N' and linear_dimension_output == 'cm':
                    moment_output = (convert(moment_value, force_input, force_output)
                                     * length_measurement[linear_dimension_output])
                    self.convertor_ui.lineEdit_moment2.setText(f"{moment_output:.2f}")

                elif force_output == 'N' and linear_dimension_output == 'inch':
                    moment_output = (convert(moment_value, force_input, force_output)
                                     * length_measurement[linear_dimension_output])
                    self.convertor_ui.lineEdit_moment2.setText(f"{moment_output:.2f}")

                elif force_output == 'N' and linear_dimension_output == 'foot':
                    moment_output = (convert(moment_value, force_input, force_output)
                                     * length_measurement[linear_dimension_output])
                    self.convertor_ui.lineEdit_moment2.setText(f"{moment_output:.2f}")
                """

        except ValueError:
            # Очищаем все поля
            self.convertor_ui.lineEdit_moment1.clear()
            self.convertor_ui.lineEdit_moment2.clear()

        finally:
            # Возвращаем обработчики
            self.convertor_ui.lineEdit_moment1.blockSignals(False)
            self.convertor_ui.lineEdit_moment2.blockSignals(False)
        '''