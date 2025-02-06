import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator, QDoubleValidator, QIntValidator
from PyQt5.QtWidgets import QLineEdit
from convertor_branch import ConvertorBranch


from ui_designe import *

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    myapp = ConvertorBranch()
    myapp.show()
    sys.exit(app.exec_())
