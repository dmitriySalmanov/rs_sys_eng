import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QVBoxLayout

class UnitConverter(QWidget):
    def __init__(self):
        super().__init__()

        # Создаем два QLineEdit
        self.line_edit1 = QLineEdit(self)
        self.line_edit2 = QLineEdit(self)

        # Подключаем обработчики изменения текста
        self.line_edit1.textChanged.connect(self.update_from_first)
        self.line_edit2.textChanged.connect(self.update_from_second)

        # Создаем макет
        layout = QVBoxLayout()
        layout.addWidget(self.line_edit1)
        layout.addWidget(self.line_edit2)
        self.setLayout(layout)

        # Устанавливаем начальные значения
        self.setWindowTitle("Конвертер единиц")
        self.setGeometry(100, 100, 250, 100)

    def update_from_first(self):
        """Обновляем второй QLineEdit на основе первого."""
        try:
            # Конвертируем значение из метры в километры
            meters = float(self.line_edit1.text())
            kilometers = meters / 1000
            self.line_edit2.setText(str(kilometers))
        except ValueError:
            self.line_edit2.setText("Ошибка")

    def update_from_second(self):
        """Обновляем первый QLineEdit на основе второго."""
        try:
            # Конвертируем значение из километры в метры
            kilometers = float(self.line_edit2.text())
            meters = kilometers * 1000
            self.line_edit1.setText(str(meters))
        except ValueError:
            self.line_edit1.setText("Ошибка")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UnitConverter()
    window.show()
    sys.exit(app.exec_())