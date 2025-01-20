import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator, QDoubleValidator, QIntValidator
from des import *
from convertorscr import convert_kg


class MyWin(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Валидаторы для lineEdit
        validator = QRegExpValidator(QRegExp(r'\d+\.\d+'))
        #validator_for_int = QIntValidator(0,10000)
        self.ui.lineEdit_kg.setValidator(validator)
        self.ui.lineEdit_kn.setValidator(validator)

        # Подключаем обработчики изменения текста
        self.ui.lineEdit_kg.textChanged.connect(self.from_kg_to_kn)
        self.ui.lineEdit_kn.textChanged.connect(self.from_kn_to_kg)


    def from_kg_to_kn(self):
        """Обновляем второй QLineEdit на основе первого."""
        try:
            #kg = float(self.ui.lineEdit_kg.text())
            kn = convert_kg(float(self.ui.lineEdit_kg.text()))
            self.ui.lineEdit_kn.setText(f"{kn:.2f}".rstrip('0').rstrip('.'))
        except ValueError:
            self.ui.lineEdit_kn.setText("")

    def from_kn_to_kg(self):
        """Обновляем первый QLineEdit на основе второго."""
        try:
            kn = float(self.ui.lineEdit_kn.text())
            kg = (kn * 1000) / 9.8
            #self.ui.lineEdit_kg.setText(str(int(kg)))
            #self.ui.lineEdit_kg.setText(f"{kg:.2f}".rstrip('0').rstrip('.'))
            self.ui.lineEdit_kg.setText(f"{kg:.0f}")
        except ValueError:
            self.ui.lineEdit_kg.setText("")


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    myapp = MyWin()
    myapp.show()
    sys.exit(app.exec_())