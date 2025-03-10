import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator, QDoubleValidator, QIntValidator, QRegularExpressionValidator
from PyQt5.QtWidgets import QLineEdit
from ui_designe import *
from unit_conversion import *

class ConvertorBranch:
    def __init__(self):
        self.convertor_ui = None

    def setup_connections(self):
        '''
        -Описание: Метод подключает оброботчкики
        -Принимает: Ничего
        -Возвращает: Ничего
        '''
        # Подключаем обработчики изменения текста для сил
        if self.convertor_ui:
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

        # Подключаем обработчики изменения текста для линейных размеров
            self.convertor_ui.lineEdit_mm.textChanged.connect(lambda: self.convert_dimensions('mm'))
            self.convertor_ui.lineEdit_cm.textChanged.connect(lambda: self.convert_dimensions('cm'))
            self.convertor_ui.lineEdit_m.textChanged.connect(lambda: self.convert_dimensions('m'))
            self.convertor_ui.lineEdit_inch.textChanged.connect(lambda: self.convert_dimensions('inch'))
            self.convertor_ui.lineEdit_foot.textChanged.connect(lambda: self.convert_dimensions('foot'))

        # Подключаем обработчики изменения текста для углов
            self.convertor_ui.lineEdit_degrees.textChanged.connect(lambda: self.convert_angles('degrees'))
            self.convertor_ui.lineEdit_radians.textChanged.connect(lambda: self.convert_angles('radians'))

        # Подключаем обработчики изменения текста для моментов инерции
            self.convertor_ui.lineEdit_mm4.textChanged.connect(lambda: self.convert_inertia('mm4'))
            self.convertor_ui.lineEdit_cm4.textChanged.connect(lambda: self.convert_inertia('cm4'))
            self.convertor_ui.lineEdit_m4.textChanged.connect(lambda: self.convert_inertia('m4'))

        # Подключаем обработчики изменения текста для моментов сопротивления
            self.convertor_ui.lineEdit_mm3.textChanged.connect(lambda: self.convert_section_modulus('mm3'))
            self.convertor_ui.lineEdit_cm3.textChanged.connect(lambda: self.convert_section_modulus('cm3'))
            self.convertor_ui.lineEdit_m3.textChanged.connect(lambda: self.convert_section_modulus('m3'))


    def convert_force(self, unit):
        """
        -Описание: Метод обрабатывает lineEdit'ы, пересчитывает единицы измерения силы и выводит их в
        соответствующую строку
        -Принимает: unit - str значение/флаг соответствующее конкретной единице измерения
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

    def convert_pressure(self, unit):
        """
            -Описание: Метод обрабатывает lineEdit'ы, пересчитывает единицы измерения давлений и выводит их в
            соответствующую строку
            -Принимает: unit - str значение/флаг соответствующее конкретной единице измерения
            -Возвращает: Ничего
        """
        length_measurement = {'m²': 1 ** 2, 'cm²': 100 ** 2, 'mm²': 1000 ** 2, 'inch²': 39.37008 ** 2,
                              'foot²': 3.28084 ** 2}

        try:
            # Отключаем обработчики, чтобы избежать рекурсии
            for line_edit in self.convertor_ui.groupBox_pressure.findChildren(QLineEdit):
                line_edit.blockSignals(True)

            pressure_input = float(getattr(self.convertor_ui, f"lineEdit_{unit}").text())

            force_input = self.convertor_ui.comboBox_pressure_f1.currentText()
            quadratic_dimension_input = self.convertor_ui.comboBox_pressure_qd1.currentText()

            force_output = self.convertor_ui.comboBox_pressure_f2.currentText()
            quadratic_dimension_output = self.convertor_ui.comboBox_pressure_qd2.currentText()

            # Математический блок с проверкой по ключам
            if unit == 'pressure_1':
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

            if unit == 'pressure_3':  # Pa
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

            if unit == 'pressure_4':  # kPa
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

            if unit == 'pressure_5':  # MPa
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

    def convert_dimensions(self, unit):
        """
            -Описание: Метод обрабатывает lineEdit'ы, пересчитывает единицы измерения линейных размеров и выводит их в
            соответствующую строку
            -Принимает: unit - str значение/флаг соответствующее конкретной единице измерения
            -Возвращает: Ничего
        """
        try:
            # Отключаем обработчики, чтобы избежать рекурсии
            for line_edit in self.convertor_ui.groupBox_lenghts.findChildren(QLineEdit):
                line_edit.blockSignals(True)

            # Математический блок с проверкой по ключам
            value = float(getattr(self.convertor_ui, f"lineEdit_{unit}").text())

            if unit == 'mm':
                for line_edit in self.convertor_ui.groupBox_lenghts.findChildren(QLineEdit):
                    if line_edit != self.convertor_ui.lineEdit_mm:
                        unit_name = line_edit.objectName().split('_')[-1]
                        line_edit.setText(f"{convert(value, unit, unit_name):.3f}")

            if unit == 'cm':
                for line_edit in self.convertor_ui.groupBox_lenghts.findChildren(QLineEdit):
                    if line_edit != self.convertor_ui.lineEdit_cm:
                        unit_name = line_edit.objectName().split('_')[-1]
                        line_edit.setText(f"{convert(value, unit, unit_name):.3f}")

            if unit == 'm':
                for line_edit in self.convertor_ui.groupBox_lenghts.findChildren(QLineEdit):
                    if line_edit != self.convertor_ui.lineEdit_m:
                        unit_name = line_edit.objectName().split('_')[-1]
                        line_edit.setText(f"{convert(value, unit, unit_name):.3f}")

            if unit == 'inch':
                for line_edit in self.convertor_ui.groupBox_lenghts.findChildren(QLineEdit):
                    if line_edit != self.convertor_ui.lineEdit_inch:
                        unit_name = line_edit.objectName().split('_')[-1]
                        line_edit.setText(f"{convert(value, unit, unit_name):.3f}")

            if unit == 'foot':
                for line_edit in self.convertor_ui.groupBox_lenghts.findChildren(QLineEdit):
                    if line_edit != self.convertor_ui.lineEdit_foot:
                        unit_name = line_edit.objectName().split('_')[-1]
                        line_edit.setText(f"{convert(value, unit, unit_name):.3f}")

        except ValueError:
            # Очищаем все поля
            for line_edit in self.convertor_ui.groupBox_lenghts.findChildren(QLineEdit):
                line_edit.clear()

        finally:
            # Возвращаем обработчики
            for line_edit in self.convertor_ui.groupBox_lenghts.findChildren(QLineEdit):
                line_edit.blockSignals(False)

    def convert_angles(self, unit):
        """
            -Описание: Метод обрабатывает lineEdit'ы, пересчитывает единицы измерения углов и выводит их в
            соответствующую строку
            -Принимает: unit - str значение/флаг соответствующее конкретной единице измерения
            -Возвращает: Ничего
        """
        try:
            # Отключаем обработчики, чтобы избежать рекурсии
            for line_edit in self.convertor_ui.groupBox_angles.findChildren(QLineEdit):
                line_edit.blockSignals(True)

            # Математический блок с проверкой по ключам
            value = float(getattr(self.convertor_ui, f"lineEdit_{unit}").text())

            if unit == 'degrees':
                for line_edit in self.convertor_ui.groupBox_angles.findChildren(QLineEdit):
                    if line_edit != self.convertor_ui.lineEdit_degrees:
                        unit_name = line_edit.objectName().split('_')[-1]
                        line_edit.setText(f"{convert(value, unit, unit_name):.3f}")

            if unit == 'radians':
                for line_edit in self.convertor_ui.groupBox_angles.findChildren(QLineEdit):
                    if line_edit != self.convertor_ui.lineEdit_radians:
                        unit_name = line_edit.objectName().split('_')[-1]
                        line_edit.setText(f"{convert(value, unit, unit_name):.3f}")

        except ValueError:
            # Очищаем все поля
            for line_edit in self.convertor_ui.groupBox_angles.findChildren(QLineEdit):
                line_edit.clear()

        finally:
            # Возвращаем обработчики
            for line_edit in self.convertor_ui.groupBox_angles.findChildren(QLineEdit):
                line_edit.blockSignals(False)

    def convert_inertia(self, unit):
        """
            -Описание: Метод обрабатывает lineEdit'ы, пересчитывает единицы измерения моментов инерции и выводит их в
            соответствующую строку
            -Принимает: unit - str значение/флаг соответствующее конкретной единице измерения
            -Возвращает: Ничего
        """
        try:
            # Отключаем обработчики, чтобы избежать рекурсии
            for line_edit in self.convertor_ui.groupBox_m_inertia.findChildren(QLineEdit):
                line_edit.blockSignals(True)

            # Математический блок с проверкой по ключам
            value = float(getattr(self.convertor_ui, f"lineEdit_{unit}").text())

            if unit == 'mm4':
                for line_edit in self.convertor_ui.groupBox_m_inertia.findChildren(QLineEdit):
                    if line_edit != self.convertor_ui.lineEdit_mm4:
                        unit_name = line_edit.objectName().split('_')[-1]
                        line_edit.setText(f"{convert(value, unit, unit_name):.8f}")

            if unit == 'cm4':
                for line_edit in self.convertor_ui.groupBox_m_inertia.findChildren(QLineEdit):
                    if line_edit != self.convertor_ui.lineEdit_cm4:
                        unit_name = line_edit.objectName().split('_')[-1]
                        line_edit.setText(f"{convert(value, unit, unit_name):.8f}")

            if unit == 'm4':
                for line_edit in self.convertor_ui.groupBox_m_inertia.findChildren(QLineEdit):
                    if line_edit != self.convertor_ui.lineEdit_m4:
                        unit_name = line_edit.objectName().split('_')[-1]
                        line_edit.setText(f"{convert(value, unit, unit_name):.8f}")

        except ValueError:
            # Очищаем все поля
            for line_edit in self.convertor_ui.groupBox_m_inertia.findChildren(QLineEdit):
                line_edit.clear()

        finally:
            # Возвращаем обработчики
            for line_edit in self.convertor_ui.groupBox_m_inertia.findChildren(QLineEdit):
                line_edit.blockSignals(False)

    def convert_section_modulus(self, unit):
        """
            -Описание: Метод обрабатывает lineEdit'ы, пересчитывает единицы измерения моментов сопротивления и выводит их в
            соответствующую строку
            -Принимает: unit - str значение/флаг соответствующее конкретной единице измерения
            -Возвращает: Ничего
        """
        try:
            # Отключаем обработчики, чтобы избежать рекурсии
            for line_edit in self.convertor_ui.groupBox_section_modulus.findChildren(QLineEdit):
                line_edit.blockSignals(True)

            # Математический блок с проверкой по ключам
            value = float(getattr(self.convertor_ui, f"lineEdit_{unit}").text())

            if unit == 'mm3':
                for line_edit in self.convertor_ui.groupBox_section_modulus.findChildren(QLineEdit):
                    if line_edit != self.convertor_ui.lineEdit_mm3:
                        unit_name = line_edit.objectName().split('_')[-1]
                        line_edit.setText(f"{convert(value, unit, unit_name):.8f}")

            if unit == 'cm3':
                for line_edit in self.convertor_ui.groupBox_section_modulus.findChildren(QLineEdit):
                    if line_edit != self.convertor_ui.lineEdit_cm3:
                        unit_name = line_edit.objectName().split('_')[-1]
                        line_edit.setText(f"{convert(value, unit, unit_name):.8f}")

            if unit == 'm3':
                for line_edit in self.convertor_ui.groupBox_section_modulus.findChildren(QLineEdit):
                    if line_edit != self.convertor_ui.lineEdit_m3:
                        unit_name = line_edit.objectName().split('_')[-1]
                        line_edit.setText(f"{convert(value, unit, unit_name):.8f}")

        except ValueError:
            # Очищаем все поля
            for line_edit in self.convertor_ui.groupBox_section_modulus.findChildren(QLineEdit):
                line_edit.clear()

        finally:
            # Возвращаем обработчики
            for line_edit in self.convertor_ui.groupBox_section_modulus.findChildren(QLineEdit):
                line_edit.blockSignals(False)