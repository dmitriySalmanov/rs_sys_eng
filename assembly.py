import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator, QDoubleValidator, QIntValidator, QIcon
from PyQt5.QtWidgets import QLineEdit, QMainWindow, QStackedWidget, QVBoxLayout, QWidget, qApp, QStyledItemDelegate
from gui_designe import *
from section_logic import SectionsData
from material_logic import MaterialsData
from beam_calculation import BeamCalc, LoadingSchemeCanvas
from weakref import WeakKeyDictionary
import os


class RequiredFieldBlinker(QtCore.QObject):
    """
    Безопасное мерцание рамки QLineEdit с валидаторами:
    - watch_required(line_edit)
    - watch_numeric(line_edit, ...)
    """
    def __init__(self, parent=None, interval_ms=450):
        super().__init__(parent)
        self._interval = interval_ms
        self._timers = WeakKeyDictionary()     # {QLineEdit -> QTimer}
        self._validators = WeakKeyDictionary() # {QLineEdit -> callable(str)->bool}

    # публичные API
    def watch_required(self, line_edit: QtWidgets.QLineEdit):
        self._validators[line_edit] = lambda s: bool(s and s.strip())
        self._wire_up(line_edit)

    def watch_numeric(
        self, line_edit: QtWidgets.QLineEdit, *,
        integer=False, allow_negative=False, allow_empty=False,
        min_value: float | None = None, max_value: float | None = None,
        comma_decimal=True
    ):
        def _validator(text: str) -> bool:
            if text is None:
                text = ""
            t = text.strip()
            if not t:
                return allow_empty
            t = t.replace(" ", "")
            if comma_decimal:
                t = t.replace(",", ".")
            try:
                val = int(t) if integer else float(t)
            except Exception:
                return False
            if not allow_negative and val < 0:
                return False
            if min_value is not None and val < min_value:
                return False
            if max_value is not None and val > max_value:
                return False
            return True

        self._validators[line_edit] = _validator
        self._wire_up(line_edit)

    def mark_invalid(self, line_edit: QtWidgets.QLineEdit):
        self._set_error(line_edit, True)

    def mark_valid(self, line_edit: QtWidgets.QLineEdit):
        self._set_error(line_edit, False)

    # внутренняя обвязка
    def _wire_up(self, le: QtWidgets.QLineEdit):
        le.textChanged.connect(lambda _=None, le=le: self._update(le))
        # ВАЖНО: НЕ подключаемся к destroyed с попытками трогать le.
        le.installEventFilter(self)
        self._update(le)

    def eventFilter(self, obj, event):
        if isinstance(obj, QtWidgets.QLineEdit) and event.type() in (
            QtCore.QEvent.EnabledChange, QtCore.QEvent.Show
        ):
            if obj.isEnabled():
                self._update(obj)
            else:
                self._stop(obj, skip_props=True)  # не трогаем свойства/стили
            return False
        return super().eventFilter(obj, event)

    # логика состояния
    def _update(self, le: QtWidgets.QLineEdit):
        validator = self._validators.get(le)
        text = le.text() if le else ""
        is_valid = validator(text) if validator else bool(text and text.strip())
        self._set_error(le, not is_valid)

    def _set_error(self, le: QtWidgets.QLineEdit, on: bool):
        # если приложение сворачивается — ничего не делаем
        if QtCore.QCoreApplication.closingDown():
            return

        # не мигаем на disabled
        if not le.isEnabled():
            on = False

        # свойства меняем только когда приложение живо
        le.setProperty("error", on)
        self._repolish(le)

        if on:
            self._start(le)
        else:
            self._stop(le)

    def _start(self, le: QtWidgets.QLineEdit):
        if le in self._timers:
            return
        # КЛЮЧЕВОЕ: таймер — ребёнок lineEdit, умрёт вместе с ним
        t = QtCore.QTimer(le)
        t.setInterval(self._interval)
        t.timeout.connect(lambda le=le: self._toggle_pulse(le))
        t.start()
        self._timers[le] = t
        le.setProperty("pulse", True)
        self._repolish(le)

    def _stop(self, le: QtWidgets.QLineEdit, *, skip_props: bool = False):
        # Остановить и забыть таймер (без обращения к уже удалённому виджету)
        t = self._timers.pop(le, None)
        if t:
            t.stop()
            t.deleteLater()
        if not skip_props and not QtCore.QCoreApplication.closingDown():
            le.setProperty("pulse", False)
            self._repolish(le)

    def _toggle_pulse(self, le: QtWidgets.QLineEdit):
        if QtCore.QCoreApplication.closingDown():
            return
        cur = bool(le.property("pulse"))
        le.setProperty("pulse", not cur)
        self._repolish(le)

    @staticmethod
    def _repolish(w: QtWidgets.QWidget):
        if QtCore.QCoreApplication.closingDown():
            return
        try:
            w.style().unpolish(w)
            w.style().polish(w)
            w.update()
        except RuntimeError:
            # На всякий случай, если Qt уже умирает
            pass


class MainWin(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.font_size = 10  # начальный размер

        # Загружаем интерфейс
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setup_font_menu()

        # Экземпляры модулей
        self.sections_data = SectionsData()
        self.materials_data = MaterialsData()
        self.beam_calculation = BeamCalc()
        self.required_blinker = RequiredFieldBlinker(self)

        self.sections_data.main_win = self  # Передаём ссылку на MainWin

        # Передаём интерфейс
        self.sections_data.sections_ui = self.ui
        self.materials_data.materials_ui = self.ui
        self.beam_calculation.beams_ui = self.ui

        self.beam_calculation.apply_styles()

        # Передаём доступ beam_calculation к materials_data и sections_data
        self.beam_calculation.materials_data = self.materials_data
        self.beam_calculation.sections_data = self.sections_data

        # Загружаем и подключаем
        self.sections_data.load_section_data()
        self.sections_data.setup_connections()
        self.update_support_combobox()

        self.materials_data.load_materials_data()
        self.materials_data.setup_connections()

        self.beam_calculation.initialize_materials()
        self.beam_calculation.setup_connections()

        self.ui.loadingSchemeCanvas = LoadingSchemeCanvas(self.ui.loadingSchemeGroupBox)
        self.ui.gridLayout_5.addWidget(self.ui.loadingSchemeCanvas, 0, 0, 1, 2)

        self.beam_calculation.loading_canvas = self.ui.loadingSchemeCanvas

        # Подключаем обновление от UI
        self.ui.baseConBoundaryComboBox.currentTextChanged.connect(
            self.ui.loadingSchemeCanvas.set_scheme
        )

        # Устанавливаем начальное значение схемы
        initial_scheme = self.ui.baseConBoundaryComboBox.currentText()
        self.ui.loadingSchemeCanvas.set_scheme(initial_scheme)

        self.setWindowTitle("Malachite v0.23")
        self.setWindowIcon(QIcon('resources/malachite.png'))
        # self.setStyleSheet("background-color: #228B22;")
        self.setStyleSheet("""
            QMainWindow {
                border-image: url(resources/background) 0 0 0 0 stretch stretch;
                background-repeat: no-repeat;
                background-position: center;
            }
        """)

        self.required_blinker.watch_required(self.ui.baseConLenghtLineEdit)
        self.required_blinker.watch_required(self.ui.baseConLoadingLineEdit)
        self.required_blinker.watch_required(self.ui.baseConUprHeightLineEdit)

    def setup_font_menu(self):
        font_menu = self.ui.menu  # Меню "Настройка шрифта"

        increase_font = QtWidgets.QAction("Увеличить шрифт", self)
        decrease_font = QtWidgets.QAction("Уменьшить шрифт", self)
        reset_font = QtWidgets.QAction("Сбросить размер", self)

        increase_font.triggered.connect(self.increase_font_size)
        decrease_font.triggered.connect(self.decrease_font_size)
        reset_font.triggered.connect(self.reset_font_size)

        font_menu.addAction(increase_font)
        font_menu.addAction(decrease_font)
        font_menu.addAction(reset_font)

    def apply_font_size(self):
        font = QtGui.QFont()
        font.setPointSize(self.font_size)
        qApp.setFont(font)

        # Принудительно обновим все виджеты
        def update_fonts(widget):
            widget.setFont(font)
            for child in widget.findChildren(QtWidgets.QWidget):
                child.setFont(font)
                if isinstance(child, QtWidgets.QTableView):
                    child.resizeColumnsToContents()

        update_fonts(self)

    def increase_font_size(self):
        self.font_size += 1
        self.apply_font_size()

    def decrease_font_size(self):
        self.font_size = max(6, self.font_size - 1)
        self.apply_font_size()

    def reset_font_size(self):
        self.font_size = 10
        self.apply_font_size()

    def update_support_combobox(self):
        """
        Обновляет sectionCheckSupportComboBox, добавляя все найденные 'Узел соединения ...'
        """
        box = self.ui.sectionCheckSupportComboBox
        box.blockSignals(True)
        box.clear()

        # Базовая опция
        box.addItem('Шарнир')

        # Получаем колонки соединений из sections_data
        if self.sections_data:
            connection_columns = self.sections_data.get_connection_columns()
            box.addItems(connection_columns)

        box.blockSignals(False)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet("QMessageBox { messagebox-icon: none; }")
    app.setStyleSheet(app.styleSheet() + """
    /* Пульсирующая рамка для обязательных полей */
    QLineEdit[error="true"][pulse="true"]  { border: 2px solid #fd778b; border-radius: 6px; }
    QLineEdit[error="true"][pulse="false"] { border: 2px solid transparent; border-radius: 6px; }
    """)
    window = MainWin()
    window.showMaximized()
    sys.exit(app.exec_())
