import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QListWidget, QFileDialog, QMessageBox, \
    QHBoxLayout, QSlider
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, \
    NavigationToolbar2QT as NavigationToolbar
from scipy.signal import savgol_filter
from scipy.ndimage import median_filter
from matplotlib.figure import Figure
from ui_designe import *


def filter_max_step(df):
    """
    -Описание: Функция проверяет длину датафрейма
    -Принимает: датафрейм
    -Возвращает: int
    """
    if 50 <= len(df) < 150:
        return int(len(df) / 3)
    elif 150 <= len(df) < 250:
        return int(len(df) / 6)
    elif 250 <= len(df) < 300:
        return int(len(df) / 9)
    else:
        return 50


class StifnessBranch:
    def __init__(self):
        self.canvas = None
        self.toolbar = None
        self.stifness_analyze_ui = None
        self.dataframes = {}  # Словарь для хранения датафреймов
        self.setup_connections()

    def setup_connections(self):
        """
        -Описание: Метод подключает оброботчкики
        -Принимает: Ничего
        -Возвращает: Ничего
        """
        if self.stifness_analyze_ui:
            self.stifness_analyze_ui.addButton_stifness_experiment.clicked.connect(self.add_files)
            self.stifness_analyze_ui.removeButton_stifness_experiment.clicked.connect(self.remove_file)
            self.stifness_analyze_ui.plotButton_stifness_experiment.clicked.connect(self.build_plot)
            self.stifness_analyze_ui.horizontalSlider_Median_step.valueChanged.connect(self.build_plot)
            self.stifness_analyze_ui.horizontalSlider_Sav_Gol_step.valueChanged.connect(self.build_plot)

    def add_files(self):
        """
        -Описание: Метод добавляет excel файлы в listWidget, преобразует их в датафреймы и добавляет их в словарь dataframes
        -Принимает: Ничего
        -Возвращает: Ничего
        """
        files, _ = QFileDialog.getOpenFileNames(None, "Выберите файлы Excel", "", "Excel Files (*.xlsx *.xls)")
        if files:
            for file in files:
                self.stifness_analyze_ui.listWidget_stifness_experiment.addItem(file)
                df = pd.read_excel(file)
                self.dataframes[file] = df

    def remove_file(self):
        """
        -Описание: Метод удаляет итемы из listWidget и словаря dataframes
        -Принимает: Ничего
        -Возвращает: Ничего
        """
        current_item = self.stifness_analyze_ui.listWidget_stifness_experiment.currentItem()
        if current_item:
            file_path = current_item.text()
            self.stifness_analyze_ui.listWidget_stifness_experiment.takeItem(self.stifness_analyze_ui.listWidget_stifness_experiment.row(current_item))
            del self.dataframes[file_path]
        else:
            QMessageBox.warning(None, "Ошибка", "Выберите файл для удаления")

    def build_plot(self):
        """
        -Описание: Метод строит графики по выбранным в listWidget датафреймам
        -Принимает: Ничего
        -Возвращает: Ничего
        """
        current_item = self.stifness_analyze_ui.listWidget_stifness_experiment.currentItem()

        # Проверка датафрейма на содержание столбцов ky и M
        if current_item:
            file_path = current_item.text()
            df = self.dataframes.get(file_path)
            if df is not None and "ky" in df.columns and "M" in df.columns:
                if df["ky"].isnull().any() or df["M"].isnull().any():
                    QMessageBox.warning(None, "Ошибка", "Файл содержит некорректные данные (NaN)")
                    return
                # Задаем шаги для фильтров
                self.stifness_analyze_ui.horizontalSlider_Median_step.setMaximum(filter_max_step(df))
                self.stifness_analyze_ui.horizontalSlider_Sav_Gol_step.setMaximum(filter_max_step(df))
                self.stifness_analyze_ui.lineEdit_Median_step.setText(str(self.stifness_analyze_ui.horizontalSlider_Median_step.value()))
                self.stifness_analyze_ui.lineEdit_Sav_Gol_step.setText(str(self.stifness_analyze_ui.horizontalSlider_Sav_Gol_step.value()))
                mediann_step = self.stifness_analyze_ui.horizontalSlider_Median_step.value()
                savgol_step = self.stifness_analyze_ui.horizontalSlider_Sav_Gol_step.value()

                # Очищаем виджет перед построением
                self.clear_chart_widget()

                # Применяем фильтры: медианный и Савицкого-Голея
                df["ky_filtered"] = median_filter(df["ky"], size=mediann_step)
                df["M_filtered"] = median_filter(df["M"], size=mediann_step)
                df["ky_savfilt"] = savgol_filter(df["ky_filtered"], window_length=savgol_step, polyorder=3)
                df["M_savfilt"] = savgol_filter(df["M_filtered"], window_length=savgol_step, polyorder=3)

                # Создаем массивы значений X и Y для построения диаграммы
                ky, m = (df["ky"].to_numpy(), df["M"].to_numpy())
                ky_savfilt, m_savfilt = (df["ky_savfilt"].to_numpy(), df["M_savfilt"].to_numpy())

                # Построение диаграммы
                fig = Figure()
                ax = fig.add_subplot(111)
                ax.plot(ky, m, color='blue', marker='.', label="Исходные данные", alpha=0.1)
                ax.plot(ky_savfilt, m_savfilt, 'r', label=f"Фильтр Медиан и Савицкого-Голея")
                ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)
                ax.set_xlabel("ky")
                ax.set_ylabel("M")
                ax.set_title(f"График для файла: {file_path}")
                ax.legend()

                self.canvas = FigureCanvas(fig)

                def on_scroll(event):
                    """
                    -Описание: Метод обработки события - приближение диаграммы при прокрутки колеса мыши
                    -Принимает: event
                    -Возвращает: Ничего
                    """
                    if event.inaxes == ax:
                        scale_factor = 1.1 if event.button == 'up' else 0.9
                        ax.set_xlim(ax.get_xlim()[0] * scale_factor, ax.get_xlim()[1] * scale_factor)
                        ax.set_ylim(ax.get_ylim()[0] * scale_factor, ax.get_ylim()[1] * scale_factor)
                        event.canvas.draw()

                # Добавляем инструментарий для диаграмм
                fig.canvas.mpl_connect('scroll_event', on_scroll)
                self.toolbar = NavigationToolbar(self.canvas, self.stifness_analyze_ui.chartWidget_stifness_experiment)
                self.stifness_analyze_ui.chartLayout_stifness_experiment.addWidget(self.toolbar)
                self.stifness_analyze_ui.chartLayout_stifness_experiment.addWidget(self.canvas)
                self.stifness_analyze_ui.chartWidget_stifness_experiment.setLayout(self.stifness_analyze_ui.chartLayout_stifness_experiment)
            else:
                QMessageBox.warning(None, "Ошибка", "Файл не содержит столбцов 'ky' и 'M' или данные повреждены")
        else:
            QMessageBox.warning(None, "Ошибка", "Выберите файл для построения графика")

    def clear_chart_widget(self):
        """
        -Описание: Метод очищает виджет от графика
        -Принимает: Ничего
        -Возвращает: Ничего
        """
        while self.stifness_analyze_ui.chartLayout_stifness_experiment.count():
            item = self.stifness_analyze_ui.chartLayout_stifness_experiment.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
