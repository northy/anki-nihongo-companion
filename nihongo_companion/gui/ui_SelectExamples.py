# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\SelectExamples.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_diagSelectExamples(object):
    def setupUi(self, diagSelectExamples):
        diagSelectExamples.setObjectName("diagSelectExamples")
        diagSelectExamples.resize(600, 400)
        diagSelectExamples.setMinimumSize(QtCore.QSize(600, 400))
        diagSelectExamples.setMaximumSize(QtCore.QSize(600, 400))
        diagSelectExamples.setContextMenuPolicy(QtCore.Qt.PreventContextMenu)
        self.pbSearch = QtWidgets.QProgressBar(diagSelectExamples)
        self.pbSearch.setGeometry(QtCore.QRect(10, 10, 581, 23))
        self.pbSearch.setProperty("value", 0)
        self.pbSearch.setTextVisible(False)
        self.pbSearch.setObjectName("pbSearch")
        self.tExamples = QtWidgets.QTableWidget(diagSelectExamples)
        self.tExamples.setEnabled(False)
        self.tExamples.setGeometry(QtCore.QRect(10, 40, 581, 311))
        self.tExamples.setObjectName("tExamples")
        self.tExamples.setColumnCount(2)
        self.tExamples.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tExamples.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tExamples.setHorizontalHeaderItem(1, item)
        self.cbField_out = QtWidgets.QComboBox(diagSelectExamples)
        self.cbField_out.setGeometry(QtCore.QRect(130, 360, 261, 22))
        self.cbField_out.setObjectName("cbField_out")
        self.labelField_out = QtWidgets.QLabel(diagSelectExamples)
        self.labelField_out.setGeometry(QtCore.QRect(10, 360, 111, 16))
        self.labelField_out.setObjectName("labelField_out")
        self.bConfirm = QtWidgets.QPushButton(diagSelectExamples)
        self.bConfirm.setEnabled(False)
        self.bConfirm.setGeometry(QtCore.QRect(500, 360, 93, 28))
        self.bConfirm.setObjectName("bConfirm")
        self.bCancel = QtWidgets.QPushButton(diagSelectExamples)
        self.bCancel.setGeometry(QtCore.QRect(400, 360, 93, 28))
        self.bCancel.setObjectName("bCancel")

        self.retranslateUi(diagSelectExamples)
        QtCore.QMetaObject.connectSlotsByName(diagSelectExamples)

    def retranslateUi(self, diagSelectExamples):
        _translate = QtCore.QCoreApplication.translate
        diagSelectExamples.setWindowTitle(_translate("diagSelectExamples", "Dialog"))
        item = self.tExamples.horizontalHeaderItem(0)
        item.setText(_translate("diagSelectExamples", "Japanese"))
        item = self.tExamples.horizontalHeaderItem(1)
        item.setText(_translate("diagSelectExamples", "English"))
        self.labelField_out.setText(_translate("diagSelectExamples", "Field to append to:"))
        self.bConfirm.setText(_translate("diagSelectExamples", "Confirm"))
        self.bCancel.setText(_translate("diagSelectExamples", "Cancel"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    diagSelectExamples = QtWidgets.QDialog()
    ui = Ui_diagSelectExamples()
    ui.setupUi(diagSelectExamples)
    diagSelectExamples.show()
    sys.exit(app.exec_())
