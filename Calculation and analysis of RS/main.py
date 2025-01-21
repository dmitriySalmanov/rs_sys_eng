import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator, QDoubleValidator, QIntValidator
from PyQt5.QtWidgets import QLineEdit

from des import *
from convertorscr import convertor_math_module


class MyWin(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Валидаторы для lineEdit
        validator = QRegExpValidator(QRegExp(r'\d+\.\d+'))
        self.ui.lineEdit_kg.setValidator(validator)
        self.ui.lineEdit_kN.setValidator(validator)

        # Подключаем обработчики изменения текста
        self.ui.lineEdit_kg.textChanged.connect(lambda: self.convert_force('kg'))
        self.ui.lineEdit_kN.textChanged.connect(lambda: self.convert_force('kN'))

        self.testing_some_str()

    def convert_force(self, key_force):
        '''
        -Описание: Метод обрабатывает lineEdit'ы, пересчитывает единицы измерения силы и выводит их в соответствующую строку
        -Принимает: key - str значение/флаг соответствующее конкретной единице измерения
        -Возвращает: Ничего
        '''
        try:
            if key_force == 'kg':
                kn = convertor_math_module(float(self.ui.lineEdit_kg.text()))
                self.ui.lineEdit_kN.setText(f"{kn:.2f}".rstrip('0').rstrip('.')) #Выдает очень странное скругление
            elif key_force == 'kN':
                kn = float(self.ui.lineEdit_kN.text())
                kg = (kn * 1000) / 9.8
                self.ui.lineEdit_kg.setText(f"{kg:.0f}") #Выдает очень странное скругление
        except ValueError:
            self.ui.lineEdit_kg.setText("")

    def testing_some_str(self):
        for child in self.findChildren(QLineEdit):
            print('name - ', child.objectName().split('_')[-1])

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    myapp = MyWin()
    myapp.show()
    sys.exit(app.exec_())