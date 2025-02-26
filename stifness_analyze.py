import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QListWidget, QFileDialog, QMessageBox, \
    QHBoxLayout
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, \
    NavigationToolbar2QT as NavigationToolbar
from scipy.signal import savgol_filter
from scipy.ndimage import median_filter
from matplotlib.figure import Figure
from ui_designe import *


class StifnessBranch:
    def __init__(self):
        self.canvas = None
        self.toolbar = None
        self.stifness_analyze_ui = None  # Настройка интерфейса
        self.dataframes = {}  # Словарь для хранения датафреймов
        self.setup_connections()  # Вызов метода для подключения сигналов и слотов

    def setup_connections(self):
        if self.stifness_analyze_ui:
            self.stifness_analyze_ui.addButton.clicked.connect(self.add_files)
            self.stifness_analyze_ui.removeButton.clicked.connect(self.remove_file)
            self.stifness_analyze_ui.plotButton.clicked.connect(self.plot_selected_file)

    def add_files(self):
        files, _ = QFileDialog.getOpenFileNames(None, "Выберите файлы Excel", "", "Excel Files (*.xlsx *.xls)")
        if files:
            for file in files:
                self.stifness_analyze_ui.listWidget.addItem(file)
                df = pd.read_excel(file)
                self.dataframes[file] = df

    def remove_file(self):
        current_item = self.stifness_analyze_ui.listWidget.currentItem()
        if current_item:
            file_path = current_item.text()
            self.stifness_analyze_ui.listWidget.takeItem(self.stifness_analyze_ui.listWidget.row(current_item))
            del self.dataframes[file_path]
        else:
            QMessageBox.warning(None, "Ошибка", "Выберите файл для удаления")

    def plot_selected_file(self):
        current_item = self.stifness_analyze_ui.listWidget.currentItem()
        if current_item:
            file_path = current_item.text()
            df = self.dataframes.get(file_path)
            if df is not None and "ky" in df.columns and "M" in df.columns:
                if df["ky"].isnull().any() or df["M"].isnull().any():
                    QMessageBox.warning(None, "Ошибка", "Файл содержит некорректные данные (NaN)")
                    return

                self.clear_chart_widget()

                df["ky_filtered"] = median_filter(df["ky"], size=10)
                df["M_filtered"] = median_filter(df["M"], size=10)
                df["ky_savfilt"] = savgol_filter(df["ky_filtered"], window_length=15, polyorder=3)
                df["M_savfilt"] = savgol_filter(df["M_filtered"], window_length=15, polyorder=3)

                ky = df["ky"].to_numpy()
                m = df["M"].to_numpy()
                ky_savfilt = df["ky_savfilt"].to_numpy()
                m_savfilt = df["M_savfilt"].to_numpy()

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
                    if event.inaxes == ax:
                        scale_factor = 1.1 if event.button == 'up' else 0.9
                        ax.set_xlim(ax.get_xlim()[0] * scale_factor, ax.get_xlim()[1] * scale_factor)
                        ax.set_ylim(ax.get_ylim()[0] * scale_factor, ax.get_ylim()[1] * scale_factor)
                        event.canvas.draw()

                fig.canvas.mpl_connect('scroll_event', on_scroll)
                self.toolbar = NavigationToolbar(self.canvas, self.stifness_analyze_ui.chartWidget)

                self.stifness_analyze_ui.chartLayout.addWidget(self.toolbar)
                self.stifness_analyze_ui.chartLayout.addWidget(self.canvas)
                self.stifness_analyze_ui.chartWidget.setLayout(self.stifness_analyze_ui.chartLayout)
            else:
                QMessageBox.warning(None, "Ошибка", "Файл не содержит столбцов 'ky' и 'M' или данные повреждены")
        else:
            QMessageBox.warning(None, "Ошибка", "Выберите файл для построения графика")

    def clear_chart_widget(self):
        while self.stifness_analyze_ui.chartLayout.count():
            item = self.stifness_analyze_ui.chartLayout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

