# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UIdes.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
import res


class Ui_RosmaryCandA(object):
    def setupUi(self, RosmaryCandA):
        RosmaryCandA.setObjectName("RosmaryCandA")
        RosmaryCandA.resize(800, 700)
        RosmaryCandA.setMinimumSize(QtCore.QSize(700, 700))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icon/resources/RosmaryC&A.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        RosmaryCandA.setWindowIcon(icon)
        RosmaryCandA.setIconSize(QtCore.QSize(24, 24))
        self.centralwidget = QtWidgets.QWidget(RosmaryCandA)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget_convertor = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget_convertor.setGeometry(QtCore.QRect(10, 10, 581, 451))
        self.tabWidget_convertor.setObjectName("tabWidget_convertor")
        self.tab_forces_and_moments = QtWidgets.QWidget()
        self.tab_forces_and_moments.setObjectName("tab_forces_and_moments")
        self.groupBox_force = QtWidgets.QGroupBox(self.tab_forces_and_moments)
        self.groupBox_force.setGeometry(QtCore.QRect(10, 10, 220, 301))
        self.groupBox_force.setObjectName("groupBox_force")
        self.lineEdit_kg = QtWidgets.QLineEdit(self.groupBox_force)
        self.lineEdit_kg.setGeometry(QtCore.QRect(10, 20, 150, 20))
        self.lineEdit_kg.setText("")
        self.lineEdit_kg.setObjectName("lineEdit_kg")
        self.lineEdit_kN = QtWidgets.QLineEdit(self.groupBox_force)
        self.lineEdit_kN.setGeometry(QtCore.QRect(10, 110, 150, 20))
        self.lineEdit_kN.setObjectName("lineEdit_kN")
        self.label_kg = QtWidgets.QLabel(self.groupBox_force)
        self.label_kg.setGeometry(QtCore.QRect(160, 20, 31, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(True)
        font.setUnderline(False)
        font.setStrikeOut(False)
        self.label_kg.setFont(font)
        self.label_kg.setObjectName("label_kg")
        self.label_kN = QtWidgets.QLabel(self.groupBox_force)
        self.label_kN.setGeometry(QtCore.QRect(160, 110, 31, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(True)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        self.label_kN.setFont(font)
        self.label_kN.setObjectName("label_kN")
        self.lineEdit_N = QtWidgets.QLineEdit(self.groupBox_force)
        self.lineEdit_N.setGeometry(QtCore.QRect(10, 80, 150, 20))
        self.lineEdit_N.setObjectName("lineEdit_N")
        self.label_N = QtWidgets.QLabel(self.groupBox_force)
        self.label_N.setGeometry(QtCore.QRect(160, 80, 31, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(True)
        self.label_N.setFont(font)
        self.label_N.setObjectName("label_N")
        self.lineEdit_mN = QtWidgets.QLineEdit(self.groupBox_force)
        self.lineEdit_mN.setGeometry(QtCore.QRect(10, 170, 150, 20))
        self.lineEdit_mN.setObjectName("lineEdit_mN")
        self.label_mN = QtWidgets.QLabel(self.groupBox_force)
        self.label_mN.setGeometry(QtCore.QRect(160, 170, 31, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(True)
        self.label_mN.setFont(font)
        self.label_mN.setObjectName("label_mN")
        self.lineEdit_daN = QtWidgets.QLineEdit(self.groupBox_force)
        self.lineEdit_daN.setGeometry(QtCore.QRect(10, 200, 150, 20))
        self.lineEdit_daN.setObjectName("lineEdit_daN")
        self.label_daN = QtWidgets.QLabel(self.groupBox_force)
        self.label_daN.setGeometry(QtCore.QRect(160, 200, 31, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(True)
        self.label_daN.setFont(font)
        self.label_daN.setObjectName("label_daN")
        self.lineEdit_ib = QtWidgets.QLineEdit(self.groupBox_force)
        self.lineEdit_ib.setGeometry(QtCore.QRect(10, 230, 150, 20))
        self.lineEdit_ib.setObjectName("lineEdit_ib")
        self.label_ib = QtWidgets.QLabel(self.groupBox_force)
        self.label_ib.setGeometry(QtCore.QRect(160, 230, 41, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(True)
        self.label_ib.setFont(font)
        self.label_ib.setObjectName("label_ib")
        self.lineEdit_T = QtWidgets.QLineEdit(self.groupBox_force)
        self.lineEdit_T.setGeometry(QtCore.QRect(10, 50, 150, 20))
        self.lineEdit_T.setObjectName("lineEdit_T")
        self.label_T = QtWidgets.QLabel(self.groupBox_force)
        self.label_T.setGeometry(QtCore.QRect(160, 50, 31, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(True)
        self.label_T.setFont(font)
        self.label_T.setObjectName("label_T")
        self.lineEdit_MN = QtWidgets.QLineEdit(self.groupBox_force)
        self.lineEdit_MN.setGeometry(QtCore.QRect(10, 140, 150, 20))
        self.lineEdit_MN.setObjectName("lineEdit_MN")
        self.label_MN = QtWidgets.QLabel(self.groupBox_force)
        self.label_MN.setGeometry(QtCore.QRect(160, 140, 31, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(True)
        self.label_MN.setFont(font)
        self.label_MN.setObjectName("label_MN")
        self.lineEdit_kip = QtWidgets.QLineEdit(self.groupBox_force)
        self.lineEdit_kip.setGeometry(QtCore.QRect(10, 260, 150, 20))
        self.lineEdit_kip.setObjectName("lineEdit_kip")
        self.label_kip = QtWidgets.QLabel(self.groupBox_force)
        self.label_kip.setGeometry(QtCore.QRect(160, 260, 41, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(True)
        self.label_kip.setFont(font)
        self.label_kip.setObjectName("label_kip")
        self.groupBox_moment = QtWidgets.QGroupBox(self.tab_forces_and_moments)
        self.groupBox_moment.setGeometry(QtCore.QRect(240, 9, 220, 301))
        self.groupBox_moment.setObjectName("groupBox_moment")
        self.lineEdit_moment1 = QtWidgets.QLineEdit(self.groupBox_moment)
        self.lineEdit_moment1.setGeometry(QtCore.QRect(10, 20, 90, 20))
        self.lineEdit_moment1.setObjectName("lineEdit_moment1")
        self.lineEdit_moment2 = QtWidgets.QLineEdit(self.groupBox_moment)
        self.lineEdit_moment2.setGeometry(QtCore.QRect(10, 50, 90, 20))
        self.lineEdit_moment2.setObjectName("lineEdit_moment2")
        self.comboBox_moment_f1 = QtWidgets.QComboBox(self.groupBox_moment)
        self.comboBox_moment_f1.setGeometry(QtCore.QRect(110, 20, 40, 20))
        self.comboBox_moment_f1.setObjectName("comboBox_moment_f1")
        self.comboBox_moment_f1.addItem("")
        self.comboBox_moment_f1.addItem("")
        self.comboBox_moment_f1.addItem("")
        self.comboBox_moment_f1.addItem("")
        self.comboBox_moment_f1.addItem("")
        self.comboBox_moment_f1.addItem("")
        self.comboBox_moment_f1.addItem("")
        self.comboBox_moment_f1.addItem("")
        self.comboBox_moment_f1.addItem("")
        self.label_moment1 = QtWidgets.QLabel(self.groupBox_moment)
        self.label_moment1.setGeometry(QtCore.QRect(150, 20, 20, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        font.setStyleStrategy(QtGui.QFont.NoAntialias)
        self.label_moment1.setFont(font)
        self.label_moment1.setObjectName("label_moment1")
        self.comboBox_moment_f2 = QtWidgets.QComboBox(self.groupBox_moment)
        self.comboBox_moment_f2.setGeometry(QtCore.QRect(110, 50, 40, 20))
        self.comboBox_moment_f2.setObjectName("comboBox_moment_f2")
        self.comboBox_moment_f2.addItem("")
        self.comboBox_moment_f2.addItem("")
        self.comboBox_moment_f2.addItem("")
        self.comboBox_moment_f2.addItem("")
        self.comboBox_moment_f2.addItem("")
        self.comboBox_moment_f2.addItem("")
        self.comboBox_moment_f2.addItem("")
        self.comboBox_moment_f2.addItem("")
        self.comboBox_moment_f2.addItem("")
        self.label_moment2 = QtWidgets.QLabel(self.groupBox_moment)
        self.label_moment2.setGeometry(QtCore.QRect(150, 50, 20, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        font.setStyleStrategy(QtGui.QFont.NoAntialias)
        self.label_moment2.setFont(font)
        self.label_moment2.setObjectName("label_moment2")
        self.comboBox_moment_ld1 = QtWidgets.QComboBox(self.groupBox_moment)
        self.comboBox_moment_ld1.setGeometry(QtCore.QRect(170, 20, 40, 20))
        self.comboBox_moment_ld1.setObjectName("comboBox_moment_ld1")
        self.comboBox_moment_ld1.addItem("")
        self.comboBox_moment_ld1.addItem("")
        self.comboBox_moment_ld1.addItem("")
        self.comboBox_moment_ld1.addItem("")
        self.comboBox_moment_ld1.addItem("")
        self.comboBox_moment_ld2 = QtWidgets.QComboBox(self.groupBox_moment)
        self.comboBox_moment_ld2.setGeometry(QtCore.QRect(170, 50, 40, 20))
        self.comboBox_moment_ld2.setObjectName("comboBox_moment_ld2")
        self.comboBox_moment_ld2.addItem("")
        self.comboBox_moment_ld2.addItem("")
        self.comboBox_moment_ld2.addItem("")
        self.comboBox_moment_ld2.addItem("")
        self.comboBox_moment_ld2.addItem("")
        self.tabWidget_convertor.addTab(self.tab_forces_and_moments, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget_convertor.addTab(self.tab_2, "")
        RosmaryCandA.setCentralWidget(self.centralwidget)
        self.menuBar = QtWidgets.QMenuBar(RosmaryCandA)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menuBar.setObjectName("menuBar")
        RosmaryCandA.setMenuBar(self.menuBar)
        self.statusBar = QtWidgets.QStatusBar(RosmaryCandA)
        self.statusBar.setObjectName("statusBar")
        RosmaryCandA.setStatusBar(self.statusBar)

        self.retranslateUi(RosmaryCandA)
        self.tabWidget_convertor.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(RosmaryCandA)

    def retranslateUi(self, RosmaryCandA):
        _translate = QtCore.QCoreApplication.translate
        RosmaryCandA.setWindowTitle(_translate("RosmaryCandA", "MainWindow"))
        self.groupBox_force.setTitle(_translate("RosmaryCandA", "Силы"))
        self.label_kg.setText(_translate("RosmaryCandA", ":кг"))
        self.label_kN.setText(_translate("RosmaryCandA", ":кН"))
        self.label_N.setText(_translate("RosmaryCandA", ":Н"))
        self.label_mN.setText(_translate("RosmaryCandA", ":мН"))
        self.label_daN.setText(_translate("RosmaryCandA", ":даН"))
        self.label_ib.setText(_translate("RosmaryCandA", ":фунт"))
        self.label_T.setText(_translate("RosmaryCandA", ":T"))
        self.label_MN.setText(_translate("RosmaryCandA", ":МН"))
        self.label_kip.setText(_translate("RosmaryCandA", ":кип"))
        self.groupBox_moment.setTitle(_translate("RosmaryCandA", "Моменты сил"))
        self.comboBox_moment_f1.setItemText(0, _translate("RosmaryCandA", "кг"))
        self.comboBox_moment_f1.setItemText(1, _translate("RosmaryCandA", "Т"))
        self.comboBox_moment_f1.setItemText(2, _translate("RosmaryCandA", "Н"))
        self.comboBox_moment_f1.setItemText(3, _translate("RosmaryCandA", "кН"))
        self.comboBox_moment_f1.setItemText(4, _translate("RosmaryCandA", "МН"))
        self.comboBox_moment_f1.setItemText(5, _translate("RosmaryCandA", "мН"))
        self.comboBox_moment_f1.setItemText(6, _translate("RosmaryCandA", "даН"))
        self.comboBox_moment_f1.setItemText(7, _translate("RosmaryCandA", "фунт"))
        self.comboBox_moment_f1.setItemText(8, _translate("RosmaryCandA", "кип"))
        self.label_moment1.setText(_translate("RosmaryCandA", " *"))
        self.comboBox_moment_f2.setItemText(0, _translate("RosmaryCandA", "кг"))
        self.comboBox_moment_f2.setItemText(1, _translate("RosmaryCandA", "Т"))
        self.comboBox_moment_f2.setItemText(2, _translate("RosmaryCandA", "Н"))
        self.comboBox_moment_f2.setItemText(3, _translate("RosmaryCandA", "кН"))
        self.comboBox_moment_f2.setItemText(4, _translate("RosmaryCandA", "МН"))
        self.comboBox_moment_f2.setItemText(5, _translate("RosmaryCandA", "мН"))
        self.comboBox_moment_f2.setItemText(6, _translate("RosmaryCandA", "даН"))
        self.comboBox_moment_f2.setItemText(7, _translate("RosmaryCandA", "фунт"))
        self.comboBox_moment_f2.setItemText(8, _translate("RosmaryCandA", "кип"))
        self.label_moment2.setText(_translate("RosmaryCandA", " *"))
        self.comboBox_moment_ld1.setItemText(0, _translate("RosmaryCandA", "мм"))
        self.comboBox_moment_ld1.setItemText(1, _translate("RosmaryCandA", "см"))
        self.comboBox_moment_ld1.setItemText(2, _translate("RosmaryCandA", "м"))
        self.comboBox_moment_ld1.setItemText(3, _translate("RosmaryCandA", "дюйм"))
        self.comboBox_moment_ld1.setItemText(4, _translate("RosmaryCandA", "фут"))
        self.comboBox_moment_ld2.setItemText(0, _translate("RosmaryCandA", "мм"))
        self.comboBox_moment_ld2.setItemText(1, _translate("RosmaryCandA", "см"))
        self.comboBox_moment_ld2.setItemText(2, _translate("RosmaryCandA", "м"))
        self.comboBox_moment_ld2.setItemText(3, _translate("RosmaryCandA", "дюйм"))
        self.comboBox_moment_ld2.setItemText(4, _translate("RosmaryCandA", "фут"))
        self.tabWidget_convertor.setTabText(self.tabWidget_convertor.indexOf(self.tab_forces_and_moments), _translate("RosmaryCandA", "Силы и моменты"))
        self.tabWidget_convertor.setTabText(self.tabWidget_convertor.indexOf(self.tab_2), _translate("RosmaryCandA", "Tab 2"))



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    RosmaryCandA = QtWidgets.QMainWindow()
    ui = Ui_RosmaryCandA()
    ui.setupUi(RosmaryCandA)
    RosmaryCandA.show()
    sys.exit(app.exec_())
