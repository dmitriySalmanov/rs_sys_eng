import os
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtCore import QObject, Qt, QPointF, QEasingCurve
from PyQt5.QtGui import QPainter, QPen, QBrush, QPixmap, QPalette, QColor, QDoubleValidator
from PyQt5.QtWidgets import QWidget, QSizePolicy, QGroupBox, QStyledItemDelegate
from math_calculation import calculate_all_beams, format_section_name
# from section_pandas_model import PandasModel
from unified_pandas_model import SectionPandasModel
from loading_scheme_canvas import LoadingSchemeCanvas
from utilities import STANDARDS, LOAD_CONDITIONS, DEFLECTIONS
import pandas as pd
import re


class _FloatDelegate(QStyledItemDelegate):
    """Редактор с QDoubleValidator для ячеек QTableWidget."""

    def __init__(self, parent=None, bottom=0.0, top=1e12, decimals=3):
        super().__init__(parent)
        self._bottom, self._top, self._dec = bottom, top, decimals

    def createEditor(self, parent, option, index):
        editor = QtWidgets.QLineEdit(parent)
        val = QDoubleValidator(self._bottom, self._top, self._dec, editor)
        val.setNotation(QDoubleValidator.StandardNotation)
        editor.setValidator(val)
        editor.setPlaceholderText("0")
        return editor

class _DeleteRowFilter(QtCore.QObject):
    """Перехватывает клавиши Delete/Backspace и вызывает колбэк удаления строк."""
    def __init__(self, on_delete, parent=None):
        super().__init__(parent)
        self._on_delete = on_delete

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.KeyPress and event.key() in (Qt.Key_Delete, Qt.Key_Backspace):
            # удаляем только если таблица активна
            if isinstance(obj, QtWidgets.QTableWidget) and obj.isEnabled():
                self._on_delete()
                return True
        return False


class BeamCalc:
    """
    -Описание: Класс для оброботки основных расчетов
    -Принимает: Ничего
    -Возвращает: Ничего
    """

    def __init__(self):

        self.beams_ui = None
        self.materials_data = None
        self.materials_dict = {}
        self.loading_canvas = None
        self.sections_data = None
        self.point_loads = []

        self.length = 0.0  # длина балки в метрах
        self.load = 0.0  # нагрузка в килограммах

        # Коэффициенты
        self.gamma_g = 1  # Коэффициент надёжности по нагрузке для собственного веса
        self.gamma_q_omega = 1  # Коэффициент надёжности по нагрузке при расчёте по прочности
        self.gamma_q_f = 1  # Коэффициент надёжности по нагрузке при расчёте по прогибу
        self.reduction_factor_i = 1.03  # Коэффициент уменьшающий момент инерции траверсы, только для Beam Loads
        self.reduction_factor_w = 1.12  # Коэффициент уменьшающий момент сопротивления траверсы, только для Beam Loads
        self.gamma_mb = 0.953191488  # Коэффициент надёжности по материалу стали траверсы
        self.load_factor = 0  # Коэффициент нагрузки
        self.modulus_elasticity = 196.133  # Модуль Юнга
        self.beta_m = 1
        self.beta_teta = 1
        self.beta_delta = 1
        self.n_forces = 1
        self.deflection_limit = 200



    def apply_styles(self):
        box = getattr(self.beams_ui, "boundaryConditionsGroupBox", None)
        if box is None and hasattr(self.beams_ui, "findChild"):
            box = self.beams_ui.findChild(QGroupBox, "boundaryConditionsGroupBox")
        if not box:
            return  # имя в Designer другое? проверь objectName

        box.setStyleSheet("""
            QGroupBox#boundaryConditionsGroupBox {
                 border-image: url(resources/backgroundBoxes) 0 0 0 0 stretch stretch;
                border: 1px solid gray;
                border-radius: 6px;
                margin-top: 18px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 4px;
            }
        """)

    def initialize_materials(self):
        """
        -Описание: Метод загружает словарь материалов из materials_data и обновляет combobox
        """
        self.materials_data.load_materials_data()
        self.materials_dict = self.materials_data.get_materials_dict()
        self.update_materials_combobox()

    def setup_connections(self):
        """
        -Описание: Метод для подключения соединений и сигналов
        """
        if not self.beams_ui:
            return

        self._connect_input_controls()
        self._connect_filter_controls()
        self._connect_output_controls()
        self._connect_misc_controls()

        cb = self.beams_ui.baseConBoundaryComboBox
        cb.currentTextChanged.connect(self._on_boundary_mode_changed)
        self._on_boundary_mode_changed(cb.currentText())

    def _connect_input_controls(self):
        self.beams_ui.baseConMaterialComboBox.currentTextChanged.connect(self.on_material_selected)
        self.beams_ui.baseConBoundaryComboBox.currentTextChanged.connect(self.on_loading_scheme_changed)
        self.beams_ui.baseConLenghtLineEdit.textChanged.connect(self.update_beam_length)
        self.beams_ui.baseConLoadingLineEdit.textChanged.connect(self.update_beam_load)
        self.beams_ui.baseConLoadingPairRadioButton.toggled.connect(self.update_beam_load)
        self.beams_ui.baseConLoadingOneRadioButton.toggled.connect(self.update_beam_load)
        self.beams_ui.baseConUprHeightLineEdit.textChanged.connect(self.update_column_height)
        self.beams_ui.baseConUprHeightLineEdit.textChanged.connect(self.run_section_check)

    def _connect_filter_controls(self):
        self.beams_ui.sectionCheckManufacturComboBox.currentTextChanged.connect(self.update_series_combobox)

        self.beams_ui.sectionCheckManufacturComboBox.currentTextChanged.connect(self.update_width_combobox)
        self.beams_ui.sectionCheckSeriesComboBox.currentTextChanged.connect(self.update_width_combobox)

        self.beams_ui.sectionCheckManufacturComboBox.currentTextChanged.connect(self.update_thickness_combobox)
        self.beams_ui.sectionCheckSeriesComboBox.currentTextChanged.connect(self.update_thickness_combobox)

        self.beams_ui.sectionCheckManufacturComboBox.currentTextChanged.connect(self.run_section_check)
        self.beams_ui.sectionCheckSeriesComboBox.currentTextChanged.connect(self.run_section_check)
        self.beams_ui.sectionCheckWidthComboBox.currentTextChanged.connect(self.run_section_check)
        self.beams_ui.sectionCheckThicknessComboBox.currentTextChanged.connect(self.run_section_check)

    def _connect_output_controls(self):
        self.beams_ui.sectionCheckStandartComboBox.currentTextChanged.connect(self.on_standart_changed)
        self.beams_ui.sectionCheckSupportComboBox.currentTextChanged.connect(self.on_support_changed)
        self.beams_ui.sectionCheckHorizontalSlider.valueChanged.connect(self.sync_slider_to_lineedit)
        self.beams_ui.sectionCheckLineEdit.textChanged.connect(self.sync_lineedit_to_slider)
        self.beams_ui.sectionCheckCheckBox.stateChanged.connect(self.run_section_check)
        self.beams_ui.sectionCheckCheckBox.stateChanged.connect(self.update_beam_image_rotation)
        self.beams_ui.sectionCheckDelComboBox.currentTextChanged.connect(self.on_deflection_changed)
        self.beams_ui.sectionCheckTableView.clicked.connect(self.show_beam_image_from_results)
        self.beams_ui.sectionCheckTableView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

    def _connect_misc_controls(self):
        self.on_standart_changed()
        if self.materials_data:
            self.materials_data.materials_updated.connect(self.update_materials_combobox)
        if self.loading_canvas:
            self.loading_canvas.set_support(self.beams_ui.sectionCheckSupportComboBox.currentText())
        if self.sections_data:
            self.sections_data.data_updated.connect(self.update_manufacturer_combobox)
        self.init_placeholders()
        self.beams_ui.baseConLoadingPairRadioButton.setChecked(True)
        # ИНИЦИАЛИЗАЦИЯ ТАБЛИЦЫ ТОЧЕЧНЫХ НАГРУЗОК
        self.setup_boundary_table()
        self.beams_ui.baseConBoundaryComboBox.currentTextChanged.connect(
            self.on_boundary_mode_changed
        )
        current = self.beams_ui.baseConBoundaryComboBox.currentText()
        self.on_boundary_mode_changed(current)

    def init_placeholders(self):
        """
        -Описание: Метод добавляющий плейсхолдеры на лайнЭдиты
        """
        placeholder_style = "QLineEdit::placeholder { color: red; }"

        def apply_placeholder(line_edit, text):
            line_edit.setPlaceholderText(text)
            line_edit.setStyleSheet(placeholder_style)

        apply_placeholder(self.beams_ui.baseConLenghtLineEdit, "Введите длину балки (м)")
        apply_placeholder(self.beams_ui.baseConLoadingLineEdit, "Введите нагрузку (кг)")
        apply_placeholder(self.beams_ui.sectionCheckLineEdit, "Введите коэффициент n")
        apply_placeholder(self.beams_ui.baseConUprHeightLineEdit, "Введите высоту стойки (м)")

    def update_column_height(self):
        """
        -Описание: Считывает значение из baseConUprHeightLineEdit и передаёт его в холст
        """
        text = self.beams_ui.baseConUprHeightLineEdit.text().replace(",", ".")
        try:
            height = float(text)
            if self.loading_canvas:
                self.loading_canvas.set_column_height(height)
        except ValueError:
            pass

    def update_beam_length(self):
        """
        -Описание: Метод принимает значение введенное baseConLenghtLineEdit и устанавливает его в холст
        -Принимает: Ничего
        -Возвращает: Ничего
        """
        text = self.beams_ui.baseConLenghtLineEdit.text().replace(",", ".")
        try:
            length = float(text)
            if length < 0.001:  # минимальное допустимое значение
                self.length = 0.0
                return  # не запускаем расчет при нуле
            self.length = length  # сохраняем для других методов
            if self.loading_canvas:
                self.loading_canvas.set_beam_length(length)
        except ValueError:
            self.length = 0.0  # сбрасываем на 0 при некорректном вводе
            return  # ничего не делаем

        self.run_section_check()

    def update_beam_load(self):
        """
        -Описание: Метод принимает значение введенное baseConLoadingLineEdit и устанавливает его в холст
        """
        text = self.beams_ui.baseConLoadingLineEdit.text().replace(",", ".")
        try:
            load = float(text)
            if self.beams_ui.baseConLoadingPairRadioButton.isChecked():
                self.load = load / 2
            else:
                self.load = load
            if self.loading_canvas:
                self.loading_canvas.set_beam_load(load)
        except ValueError:
            self.load = 0.0
            pass
        self.run_section_check()

    def update_materials_combobox(self):
        """
        -Описание: Добавляет в baseConMaterialComboBox сталь из базы данных
        """
        current_text = self.beams_ui.baseConMaterialComboBox.currentText()

        # Получаем только включенные материалы (с "Включить"=1)
        self.materials_dict = self.materials_data.get_materials_dict(only_enabled=True)
        box = self.beams_ui.baseConMaterialComboBox
        box.blockSignals(True)
        box.clear()
        box.addItems(self.materials_dict.keys())

        # Восстанавливаем выбранный элемент, если он есть в отфильтрованном списке
        index = box.findText(current_text)
        if index >= 0:
            box.setCurrentIndex(index)
        elif self.materials_dict:
            box.setCurrentIndex(0)

        box.blockSignals(False)
        self.run_section_check()

    def setup_loading_scheme_ui(self):
        """
        -Описание: Метод для отображения схем нагружения (создает объект класса LoadingSchemeCanvas)
        """
        self.loading_canvas = LoadingSchemeCanvas()
        self.beams_ui.loadingLayout.addWidget(self.loading_canvas)

        # Инициализация текущими значениями
        self.loading_canvas.set_beam_length(self.length or 0.0)
        self.loading_canvas.set_beam_load(self.load or 0.0)
        self.loading_canvas.set_support(self.beams_ui.sectionCheckSupportComboBox.currentText())
        self.loading_canvas.set_standart(self.beams_ui.sectionCheckStandartComboBox.currentText())

        scheme = self.beams_ui.baseConBoundaryComboBox.currentText()
        self.loading_canvas.set_scheme(scheme)

        # Если уже выбран «Свой тип нагружения», сразу отрисуем введённые точки
        if scheme.strip().lower() == "свой тип нагружения":
            pts = self.get_point_loads_from_table()
            if hasattr(self.loading_canvas, "set_point_loads"):
                self.loading_canvas.set_point_loads(pts)

    def on_material_selected(self):
        """
        -Описание: Метод-скрипт для реагирования мат-модели на действия пользователя при смене материалов
        """
        selected_name = self.beams_ui.baseConMaterialComboBox.currentText()
        if selected_name in self.materials_dict:
            material_props = self.materials_dict[selected_name]
            self.run_section_check()

    def on_loading_scheme_changed(self, scheme_name):
        """
        -Описание: Метод-скрипт для реагирования мат-модели на действия пользователя при смене схемы нагружения
        """
        if self.loading_canvas:
            self.loading_canvas.set_scheme(scheme_name)
        self.run_section_check()

    def on_standart_changed(self):
        """
        -Описание: Метод-скрипт для реагирования мат-модели на действия пользователя при смене нормативов
        """
        self.standart_check()
        self.run_section_check()
        if self.loading_canvas:
            self.loading_canvas.set_standart(self.beams_ui.sectionCheckStandartComboBox.currentText())

        current = self.beams_ui.sectionCheckStandartComboBox.currentText()
        disable = current == "Beam loads"

        # Отключаем/включаем виджеты
        self.beams_ui.baseConUprHeightLineEdit.setEnabled(not disable)
        self.beams_ui.sectionCheckSupportComboBox.setEnabled(not disable)
        self.beams_ui.sectionCheckLineEdit.setEnabled(not disable)
        self.beams_ui.sectionCheckHorizontalSlider.setEnabled(not disable)

        # Сброс значений если выбран "Beam loads"
        if disable:
            self.beams_ui.baseConUprHeightLineEdit.setStyleSheet("background-color: #f0f0f0;")
            self.beams_ui.sectionCheckSupportComboBox.setCurrentIndex(0)
            self.beams_ui.sectionCheckLineEdit.setText("1")
        else:
            self.beams_ui.baseConUprHeightLineEdit.setStyleSheet("")

    def on_boundary_mode_changed(self, text: str):
        """Включает/отключает таблицу точечных нагрузок по выбранному режиму."""
        tw = self.beams_ui.baseConBoundaryTableWidget
        le = self.beams_ui.baseConLoadingLineEdit

        if text.strip() == "Свой тип нагружения":
            tw.setEnabled(True)
            if tw.rowCount() == 0:  # если пусто — пересоздать
                self.setup_boundary_table()
            le.clear()
            le.setEnabled(False)
        else:
            tw.setEnabled(False)
            tw.setRowCount(0)
            self.point_loads = []
            le.setEnabled(True)

    def sync_slider_to_lineedit(self, value):
        """
        -Описание: Обновляет LineEdit при изменении QSlider
        """
        float_value = value * 0.05
        self.beams_ui.sectionCheckLineEdit.blockSignals(True)
        self.beams_ui.sectionCheckLineEdit.setText(f"{float_value:.2f}")
        self.beams_ui.sectionCheckLineEdit.blockSignals(False)
        self.run_section_check()

    def sync_lineedit_to_slider(self, text):
        """
        -Описание: Обновляет QSlider при изменении LineEdit
        """
        try:
            float_value = float(text.replace(",", "."))
            if 0.0 <= float_value <= 1.0:
                slider_value = int(round(float_value / 0.05))
                self.beams_ui.sectionCheckHorizontalSlider.blockSignals(True)
                self.beams_ui.sectionCheckHorizontalSlider.setValue(slider_value)
                self.beams_ui.sectionCheckHorizontalSlider.blockSignals(False)
                self.run_section_check()
        except ValueError:
            pass  # если не число — игнорим

    def standart_check(self):
        """
        -Описание: Метод находит и сохраняет необходимые переменные из глобального словаря согласно выбранному
         нормативу в sectionCheckStandartComboBox
        """
        check_standart = self.beams_ui.sectionCheckStandartComboBox.currentText()
        params = STANDARDS.get(check_standart)
        if params:
            for attr, value in params.items():
                setattr(self, attr, value)

    def deflection_check(self):
        """
        -Описание: Метод находит и сохраняет необходимые переменные из глобального словаря согласно выбранному
        граничному условию по прогибу в sectionCheckDelComboBox
        """
        check_deflection = self.beams_ui.sectionCheckDelComboBox.currentText()
        params = DEFLECTIONS.get(check_deflection)
        if params:
            self.deflection_limit = params
        else:
            self.deflection_limit = 200  # Значение по умолчанию

    def load_condition_check(self):
        """
        -Описание: Метод находит и сохраняет необходимые переменные из глобального словаря согласно выбранной
        схемы нагружения в baseConBoundaryComboBox
        """
        check_loads = self.beams_ui.baseConBoundaryComboBox.currentText()
        params = LOAD_CONDITIONS.get(check_loads)
        if params:
            for attr, value in params.items():
                setattr(self, attr, value)

    def run_section_check(self):
        """
        -Описание: Основной метод браудкастящий расчет на датафрейм сечений. Передает в функцию calculate_all_beams
        все необходимые параметры
        """
        if not self._is_data_ready():
            return

        self.load_condition_check()
        self.deflection_check()

        coefficient_n = self._get_coefficient_n()
        material_props = self._get_material_props()
        if not material_props:
            return

        height = self._get_column_height()
        node_support = self.beams_ui.sectionCheckSupportComboBox.currentText()
        section_rotation = self.beams_ui.sectionCheckCheckBox.isChecked()

        df_sections = self._get_filtered_sections()
        df_all_sections = self.sections_data.original_df.copy()

        point_loads = []
        boundary_mode = self.beams_ui.baseConBoundaryComboBox.currentText().strip()
        if boundary_mode == "Свой тип нагружения":
            point_loads = self.get_point_loads_from_table()
        else:
            point_loads = []
        results_df = calculate_all_beams(
            df_sections=df_sections,
            df_all=df_all_sections,
            material_props=material_props,
            length=self.length,
            load=self.load,
            gamma_g=self.gamma_g,
            gamma_q_omega=self.gamma_q_omega,
            gamma_q_f=self.gamma_q_f,
            reduction_factor_i=self.reduction_factor_i,
            reduction_factor_w=self.reduction_factor_w,
            gamma_mb=self.gamma_mb,
            load_factor=self.load_factor,
            node_support=node_support,
            section_rotation=section_rotation,
            coefficient_n=coefficient_n,
            height=height,
            beta_m=self.beta_m,
            beta_teta=self.beta_teta,
            beta_delta=self.beta_delta,
            n_forces=self.n_forces,
            modulus_elasticity=self.modulus_elasticity,
            deflection_check=self.deflection_limit,
            point_loads=point_loads
        )

        model = SectionPandasModel(results_df)
        self.beams_ui.sectionCheckTableView.setModel(model)
        self.beams_ui.sectionCheckTableView.resizeColumnsToContents()

    def _is_data_ready(self) -> bool:
        """
        Проверка наличия данных
        """
        return self.materials_data and hasattr(self.materials_data, "original_df")

    def _get_coefficient_n(self) -> float:
        """
        Считывает значение из sectionCheckLineEdit и возвращает его
        """
        try:
            text = self.beams_ui.sectionCheckLineEdit.text().replace(",", ".")
            return float(text) if text else 1.0
        except ValueError:
            return 1.0

    def _get_material_props(self):
        """
        Считывает значение из baseConMaterialComboBox находит соответсвующую сталь в датафрейме
        и возвращает ее характеристики
        """
        selected_material = self.beams_ui.baseConMaterialComboBox.currentText()
        return self.materials_dict.get(selected_material)

    def _get_column_height(self) -> float:
        """
        Считывает значение из baseConUprHeightLineEdit и возвращает его
        """
        try:
            text = self.beams_ui.baseConUprHeightLineEdit.text().replace(",", ".")
            return float(text) if text else 0.0
        except ValueError:
            return 0.0

    def _get_filtered_sections(self) -> pd.DataFrame:
        df_sections = self.sections_data.original_df.copy()

        selected_man = self.beams_ui.sectionCheckManufacturComboBox.currentText()
        if selected_man not in ("", "Все", "*"):
            df_sections = df_sections[df_sections["Производитель"].astype(str).str.strip() == selected_man]

        selected_series = self.beams_ui.sectionCheckSeriesComboBox.currentText()
        if selected_series not in ("", "Все", "*"):
            df_sections = df_sections[df_sections["Серия"].astype(str).str.strip() == selected_series]

        selected_width = self.beams_ui.sectionCheckWidthComboBox.currentText()
        if selected_width not in ("", "Все", "*"):
            sw = pd.to_numeric(pd.Series([selected_width]), errors="coerce").iloc[0]
            if pd.notna(sw):
                colw = pd.to_numeric(df_sections["Ширина (mm)"], errors="coerce")
                df_sections = df_sections[colw == float(sw)]

        selected_thickness = self.beams_ui.sectionCheckThicknessComboBox.currentText()
        if selected_thickness not in ("", "Все", "*"):
            sel_th = pd.to_numeric(pd.Series([selected_thickness]), errors="coerce").iloc[0]
            if pd.notna(sel_th):
                col = pd.to_numeric(df_sections["Толщина стали (mm*10)"], errors="coerce").astype("Int64")
                df_sections = df_sections[col == int(sel_th)]

        return df_sections

    def on_support_changed(self, text):
        """
        -Описание: Метод-скрипт для реагирования мат-модели и холста на действия пользователя при смене узла соединения
        """
        if text == 'Шарнир':
            self.beams_ui.sectionVeiwUprLabel.clear()
            self.beams_ui.sectionVeiwUprLabel.setText(" ")
        else:
            self.sections_data.display_connection_image(
                connection_column_name=text,
                target_label=self.beams_ui.sectionVeiwUprLabel
            )
        if self.loading_canvas:
            self.loading_canvas.set_support(text)
        self.run_section_check()

    def on_deflection_changed(self):
        """
        Обрабатывает изменение предельного прогиба
        """
        self.deflection_check()
        self.run_section_check()

    def show_beam_image_from_results(self, index):
        """
        Отображает изображение сечения из результатов расчёта по строке sectionCheckTableView
        и показывает его в sectionBeamLabel.
        """
        if not index.isValid():
            return

        section_name = index.sibling(index.row(), 0).data()  # строка из колонки "Сечение"
        if not section_name:
            return

        try:
            # Используем регулярку для извлечения размеров (всегда в конце)
            match = re.search(r'(?P<series>[\w\-]+)\.(?P<height>\d+)\.(?P<width>\d+)\.(?P<thickness>\d+)$',
                              section_name)
            if not match:
                self.beams_ui.sectionBeamLabel.setText("Неверный формат названия сечения")
                return

            series = match.group("series")
            height = match.group("height")
            width = match.group("width")
            thickness = match.group("thickness")

            # Извлекаем производителя: всё, что до series
            manufacturer_part = section_name[:match.start()].strip()
            manufacturer = manufacturer_part  # он уже может включать спецификацию или нет

        except Exception as e:
            self.beams_ui.sectionBeamLabel.setText(f"Ошибка разбора: {e}")
            return

        # Поиск строки в базе
        df = self.sections_data.original_df
        match_df = df[df.apply(lambda r: format_section_name(r) == section_name, axis=1)]
        if match_df.empty:
            self.beams_ui.sectionBeamLabel.setText("Изображение не найдено")
            return

        row = match_df.iloc[0]
        relative_path = row.get("Изображение", "")
        if not relative_path or pd.isna(relative_path):
            self.beams_ui.sectionBeamLabel.setText("Путь к изображению отсутствует")
            return

        from utilities import PROJECT_ROOT
        image_dir = os.path.join(PROJECT_ROOT, "resources")
        filename = os.path.basename(str(relative_path)).strip()
        abs_path = os.path.join(image_dir, filename)

        if os.path.exists(abs_path):
            pixmap = QPixmap(abs_path)

            if self.beams_ui.sectionCheckCheckBox.isChecked():
                transform = QtGui.QTransform().rotate(90)
                pixmap = pixmap.transformed(transform, Qt.SmoothTransformation)

            scaled = pixmap.scaled(
                self.beams_ui.sectionBeamLabel.width(),
                self.beams_ui.sectionBeamLabel.height(),
                Qt.KeepAspectRatio
            )
            self.beams_ui.sectionBeamLabel.setPixmap(scaled)
        else:
            self.beams_ui.sectionBeamLabel.setText("Файл изображения не найден")

    def update_beam_image_rotation(self):
        """
        Обновляет отображение изображения сечения с учетом флага поворота.
        Использует текущую выделенную строку в таблице sectionCheckTableView.
        """
        index = self.beams_ui.sectionCheckTableView.currentIndex()
        if index.isValid():
            self.show_beam_image_from_results(index)

    def update_manufacturer_combobox(self):
        if self.sections_data and hasattr(self.sections_data, "original_df"):
            df = self.sections_data.original_df

            if "Производитель" not in df.columns:
                return  # Предохранитель

            manufacturers = sorted(df["Производитель"].dropna().astype(str).unique())
            manufacturers = [m for m in manufacturers if m.strip()]

            box = self.beams_ui.sectionCheckManufacturComboBox
            box.blockSignals(True)
            box.clear()
            box.addItem("Все")
            box.addItems(manufacturers)
            box.blockSignals(False)
        self.update_width_combobox()

    def update_series_combobox(self):
        """
        Метод заполняет sectionCheckSeriesComboBox сериями из базы данных
        """
        if self.sections_data and hasattr(self.sections_data, "original_df"):
            df = self.sections_data.original_df

            # Фильтрация только по балкам
            df = df[df["Классификация"].astype(str).str.lower().str.strip() == "балка"]

            selected_man = self.beams_ui.sectionCheckManufacturComboBox.currentText()
            if selected_man not in ("", "Все"):
                df = df[df["Производитель"].astype(str).str.strip() == selected_man]

            series_list = sorted(df["Серия"].dropna().astype(str).str.strip().unique())

            box = self.beams_ui.sectionCheckSeriesComboBox
            box.blockSignals(True)
            box.clear()
            box.addItem("Все")
            box.addItems(series_list)
            box.blockSignals(False)
        self.update_width_combobox()
        self.update_thickness_combobox()

    def update_width_combobox(self):
        """
        Метод заполняет sectionCheckWidthComboBox доступными ширинами (мм)
        с учётом выбранных производителя/серии (только по Балкам).
        """
        if self.sections_data and hasattr(self.sections_data, "original_df"):
            df = self.sections_data.original_df

            # Только балки
            df = df[df["Классификация"].astype(str).str.lower().str.strip() == "балка"]

            selected_man = self.beams_ui.sectionCheckManufacturComboBox.currentText()
            selected_series = self.beams_ui.sectionCheckSeriesComboBox.currentText()

            if selected_man not in ("", "Все"):
                df = df[df["Производитель"].astype(str).str.strip() == selected_man]
            if selected_series not in ("", "Все"):
                df = df[df["Серия"].astype(str).str.strip() == selected_series]

            widths = (
                pd.to_numeric(df["Ширина (mm)"], errors="coerce")
                .dropna()
                .astype(int)
                .sort_values()
                .astype(str)
                .unique()
                .tolist()
            )

            box = self.beams_ui.sectionCheckWidthComboBox
            box.blockSignals(True)
            box.clear()
            box.addItem("Все")
            box.addItems(widths)
            box.blockSignals(False)

    def update_thickness_combobox(self):
        if self.sections_data and hasattr(self.sections_data, "original_df"):
            df = self.sections_data.original_df

            df = df[df["Классификация"].astype(str).str.lower().str.strip() == "балка"]

            selected_man = self.beams_ui.sectionCheckManufacturComboBox.currentText()
            selected_series = self.beams_ui.sectionCheckSeriesComboBox.currentText()
            selected_width = self.beams_ui.sectionCheckWidthComboBox.currentText()

            if selected_man not in ("", "Все"):
                df = df[df["Производитель"].astype(str).str.strip() == selected_man]
            if selected_series not in ("", "Все"):
                df = df[df["Серия"].astype(str).str.strip() == selected_series]
            if selected_width not in ("", "Все", "*"):
                sw = pd.to_numeric(pd.Series([selected_width]), errors="coerce").iloc[0]
                if pd.notna(sw):
                    colw = pd.to_numeric(df["Ширина (mm)"], errors="coerce")
                    df = df[colw == float(sw)]

            thicknesses = (
                pd.to_numeric(df["Толщина стали (mm*10)"], errors="coerce")
                .dropna()
                .astype(int)
                .sort_values()
                .astype(str)  # для отображения в ComboBox
                .unique()
                .tolist()
            )

            box = self.beams_ui.sectionCheckThicknessComboBox
            box.blockSignals(True)
            box.clear()
            box.addItem("Все")
            box.addItems(thicknesses)
            box.blockSignals(False)

    # =========================================================================
    def setup_boundary_table(self):
        """Инициализация таблицы точечных нагрузок."""
        boundary_table = self.beams_ui.baseConBoundaryTableWidget
        boundary_table.blockSignals(True)
        boundary_table.setColumnCount(3)
        boundary_table.setHorizontalHeaderLabels(["Точка приложения силы (№)", "Расстояние (мм)", "Нагрузка (кг)"])
        boundary_table.setEditTriggers(QtWidgets.QAbstractItemView.AllEditTriggers)
        boundary_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        boundary_table.setAlternatingRowColors(True)
        boundary_table.horizontalHeader().setStretchLastSection(True)

        # Делегаты с валидаторами: расстояние и нагрузка — только числа
        boundary_table.setItemDelegateForColumn(1, _FloatDelegate(boundary_table, bottom=0.0, top=1e9, decimals=3))
        boundary_table.setItemDelegateForColumn(2, _FloatDelegate(boundary_table, bottom=0.0, top=1e9, decimals=3))

        # Создаём одну пустую строку
        boundary_table.setRowCount(0)
        self._append_empty_row()

        # 1-я колонка — только чтение
        boundary_table.setColumnWidth(0, 180)
        for row in range(boundary_table.rowCount()):
            item = boundary_table.item(row, 0) or QtWidgets.QTableWidgetItem()
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # без редактирования
            boundary_table.setItem(row, 0, item)

        boundary_table.blockSignals(False)

        # Сигнал изменения ячеек
        boundary_table.itemChanged.connect(self.on_boundary_cell_changed)
        self._boundary_delete_filter = _DeleteRowFilter(self._delete_selected_boundary_rows, boundary_table)
        boundary_table.installEventFilter(self._boundary_delete_filter)

    def _append_empty_row(self):
        """Добавляет пустую строку и корректно нумерует первую колонку."""
        boundary_table = self.beams_ui.baseConBoundaryTableWidget
        boundary_row = boundary_table.rowCount()
        boundary_table.insertRow(boundary_row)

        # № точки
        boundary_number = QtWidgets.QTableWidgetItem(str(boundary_row + 1))
        boundary_number.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        boundary_table.setItem(boundary_row, 0, boundary_number)

        # Расстояние, мм
        boundary_table.setItem(boundary_row, 1, QtWidgets.QTableWidgetItem(""))

        # Нагрузка, кг
        boundary_table.setItem(boundary_row, 2, QtWidgets.QTableWidgetItem(""))

    def _is_row_empty(self, boundary_row: int) -> bool:
        boundary_table = self.beams_ui.baseConBoundaryTableWidget
        distance = (boundary_table.item(boundary_row, 1).text().strip() if boundary_table.item(boundary_row, 1) else "")
        load = (boundary_table.item(boundary_row, 2).text().strip() if boundary_table.item(boundary_row, 2) else "")
        return distance == "" and load == ""

    def _renumber_points(self):
        boundary_table = self.beams_ui.baseConBoundaryTableWidget
        for row in range(boundary_table.rowCount()):
            item = boundary_table.item(row, 0) or QtWidgets.QTableWidgetItem()
            item.setText(str(row + 1))
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            boundary_table.setItem(row, 0, item)

    def _mark_cell(self, boundary_row, boundary_column, ok: bool, tooltip_ok: str = "", tooltip_err: str = ""):
        """Подсветка ошибки/сброс и tooltip."""
        boundary_table = self.beams_ui.baseConBoundaryTableWidget
        boundary_cell = boundary_table.item(boundary_row, boundary_column)
        if not boundary_cell:
            boundary_cell = QtWidgets.QTableWidgetItem("")
            boundary_table.setItem(boundary_row, boundary_column, boundary_cell)
        if ok:
            boundary_cell.setBackground(QtGui.QBrush(Qt.transparent))
            boundary_cell.setToolTip(tooltip_ok)
        else:
            boundary_cell.setBackground(QtGui.QBrush(QColor("#FA8072")))
            boundary_cell.setToolTip(tooltip_err)

    def on_boundary_cell_changed(self, item: QtWidgets.QTableWidgetItem):
        """Валидация ввода, автодобавление строки и обновление self.point_loads."""
        boundary_table = self.beams_ui.baseConBoundaryTableWidget
        if item.column() not in (1, 2):  # реагируем только на ввод расстояния/нагрузки
            return

        boundary_table.blockSignals(True)
        boundary_row, boundary_column = item.row(), item.column()

        # Чистка ввода
        boundary_text = (item.text() or "").replace(",", ".").strip()
        item.setText(boundary_text)

        # Проверки
        is_valid = True
        numeric_value = None
        if boundary_text != "":
            try:
                numeric_value = float(boundary_text)
                if numeric_value < 0:
                    is_valid = False
            except ValueError:
                is_valid = False

        # Доп. проверка для расстояния: не превышать длину балки (если она задана)
        if is_valid and boundary_column == 1 and self.length and numeric_value is not None:
            max_allowed_distance_mm = self.length * 1000.0
            if numeric_value > max_allowed_distance_mm:
                is_valid = False

        # Подсветка / tooltip
        if boundary_column == 1:
            tooltip_error_msg = "Введите расстояние в мм (0…L*1000)."
            self._mark_cell(boundary_row, boundary_column, is_valid, tooltip_ok="Расстояние, мм",
                            tooltip_err=tooltip_error_msg)
        else:
            tooltip_error_msg = "Введите положительную нагрузку, кг."
            self._mark_cell(boundary_row, boundary_column, is_valid, tooltip_ok="Нагрузка, кг",
                            tooltip_err=tooltip_error_msg)

        # Держим одну пустую строку внизу
        last = boundary_table.rowCount() - 1
        if not self._is_row_empty(last):
            self._append_empty_row()
        # Убираем лишние пустые хвостовые строки (оставляем одну)
        while boundary_table.rowCount() >= 2 and self._is_row_empty(
                boundary_table.rowCount() - 1) and self._is_row_empty(boundary_table.rowCount() - 2):
            boundary_table.removeRow(boundary_table.rowCount() - 1)

        self._renumber_points()
        boundary_table.blockSignals(False)

        # Обновляем кэш и перерисовку/расчёт при изменении валидных данных
        self.point_loads = self.get_point_loads_from_table()
        if hasattr(self.loading_canvas, "set_point_loads"):
            self.loading_canvas.set_point_loads(self.point_loads)  # ожидается список

        # Количество сил = число валидных строк
        self.n_forces = len(self.point_loads)

        self.run_section_check()

    def get_point_loads_from_table(self, x_mm_list_override=None):
        """
        Возвращает [(x_m, P_kg), ...] с кумулятивных координат.
        """
        boundary_table = self.beams_ui.baseConBoundaryTableWidget
        boundary_points = []

        if x_mm_list_override is None:
            beam_length_mm = (self.length or 0) * 1000.0
            cumulative_distance_mm = 0.0  # накопленное расстояние по пролёту
            absolute_positions_mm = []  # список абсолютных координат в мм
            for r in range(boundary_table.rowCount()):
                distance_text = (
                    boundary_table.item(r, 1).text().replace(",", ".").strip() if boundary_table.item(r, 1) else "")
                load_text = (
                    boundary_table.item(r, 2).text().replace(",", ".").strip() if boundary_table.item(r, 2) else "")
                if not distance_text or not load_text:
                    continue
                try:
                    distance = float(distance_text);
                    load = float(load_text)
                except ValueError:
                    continue
                if distance < 0 or load <= 0:
                    continue
                cumulative_distance_mm += distance
                if self.length and cumulative_distance_mm > beam_length_mm:
                    break
                absolute_positions_mm.append(cumulative_distance_mm)
        else:
            absolute_positions_mm = list(x_mm_list_override)

        # собрать пары (x, P)
        i = 0
        for r in range(boundary_table.rowCount()):
            load_text = (
                boundary_table.item(r, 2).text().replace(",", ".").strip() if boundary_table.item(r, 2) else "")
            if i >= len(absolute_positions_mm) or not load_text:
                continue
            try:
                load = float(load_text)
            except ValueError:
                continue
            if load <= 0:
                continue
            x_m = absolute_positions_mm[i] / 1000.0
            if self.length and x_m > self.length:
                break
            boundary_points.append((x_m, load))
            i += 1

        return boundary_points

    def _delete_selected_boundary_rows(self):
        """Удаляет выделенные строки таблицы точечных нагрузок.
        Гарантирует наличие одной пустой строки снизу, пере-нумеровывает точки,
        обновляет self.point_loads, n_forces и перезапускает расчёт.
        """
        boundary_table = self.beams_ui.baseConBoundaryTableWidget
        if not boundary_table or boundary_table.rowCount() == 0:
            return

        sel_model = boundary_table.selectionModel()
        if not sel_model:
            return

        # Сбор выделенных строк (работает и при выделении ячеек)
        rows = sorted({idx.row() for idx in sel_model.selectedRows()} |
                      {idx.row() for idx in sel_model.selectedIndexes()})
        if not rows:
            return

        boundary_table.blockSignals(True)

        # Удаляем снизу вверх, чтобы индексы не «плыли»
        for row in reversed(rows):
            # Если осталась единственная строка — просто очистим её, а не удалим
            if boundary_table.rowCount() <= 1:
                # гарантируем существование ячеек и очищаем поля «расстояние» и «нагрузка»
                for c in (1, 2):
                    item = boundary_table.item(row, c) or QtWidgets.QTableWidgetItem("")
                    item.setText("")
                    boundary_table.setItem(row, c, item)
                break
            boundary_table.removeRow(row)

        # Если всё удалили — создаём одну пустую
        if boundary_table.rowCount() == 0:
            self._append_empty_row()
        else:
            last = boundary_table.rowCount() - 1
            # Если последняя строка не пустая — добавим пустую
            if not self._is_row_empty(last):
                self._append_empty_row()
            # Держим ровно одну пустую строку хвостом
            while boundary_table.rowCount() >= 2 and self._is_row_empty(boundary_table.rowCount() - 1) \
                    and self._is_row_empty(boundary_table.rowCount() - 2):
                boundary_table.removeRow(boundary_table.rowCount() - 1)

        # Перенумеруем точки
        self._renumber_points()

        # Поставим курсор на валидную строку
        target_row = min(rows[0], boundary_table.rowCount() - 1)
        boundary_table.setCurrentCell(target_row, 0)

        boundary_table.blockSignals(False)

        # Обновим кэш/отрисовку/расчёт
        self.point_loads = self.get_point_loads_from_table()
        if hasattr(self.loading_canvas, "set_point_loads"):
            self.loading_canvas.set_point_loads(self.point_loads)
        self.n_forces = len(self.point_loads)
        self.run_section_check()

    def _on_boundary_mode_changed(self, text: str):
        own_mode = text.strip().lower() == "свой тип нагружения"

        # Показ/скрытие таблицы точечных нагрузок
        self.beams_ui.baseConBoundaryTableWidget.setVisible(own_mode)

        # Поле равномерной нагрузки: отключаем и чистим в режиме "свой тип"
        le = self.beams_ui.baseConLoadingLineEdit
        if own_mode:
            le.blockSignals(True)
            le.clear()
            le.setEnabled(False)
            le.blockSignals(False)
        else:
            le.setEnabled(True)

        # Обновляем внутреннее состояние нагрузок и перерисовку
        self.point_loads = self.get_point_loads_from_table() if own_mode else []
        self.n_forces = len(self.point_loads)

        if getattr(self, "loading_canvas", None) and hasattr(self.loading_canvas, "set_point_loads"):
            self.loading_canvas.set_point_loads(self.point_loads)

        # Пересчёт результатов с учётом нового режима
        self.run_section_check()
