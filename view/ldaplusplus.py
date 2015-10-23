# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ldaplusplus.ui'
#
# Created: Fri Feb 20 14:39:16 2015
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_LDAPlusPlus(object):
    def setupUi(self, LDAPlusPlus):
        LDAPlusPlus.setObjectName(_fromUtf8("LDAPlusPlus"))
        LDAPlusPlus.resize(383, 445)
        self.centralWidget = QtGui.QWidget(LDAPlusPlus)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.label = QtGui.QLabel(self.centralWidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 59, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.line = QtGui.QFrame(self.centralWidget)
        self.line.setGeometry(QtCore.QRect(50, 20, 118, 3))
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.saxDuration = QtGui.QLineEdit(self.centralWidget)
        self.saxDuration.setGeometry(QtCore.QRect(260, 30, 113, 21))
        self.saxDuration.setObjectName(_fromUtf8("saxDuration"))
        self.label_2 = QtGui.QLabel(self.centralWidget)
        self.label_2.setGeometry(QtCore.QRect(10, 30, 151, 16))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.alphabetSize = QtGui.QLineEdit(self.centralWidget)
        self.alphabetSize.setGeometry(QtCore.QRect(260, 60, 113, 21))
        self.alphabetSize.setObjectName(_fromUtf8("alphabetSize"))
        self.label_3 = QtGui.QLabel(self.centralWidget)
        self.label_3.setGeometry(QtCore.QRect(10, 60, 151, 16))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.wordLength = QtGui.QLineEdit(self.centralWidget)
        self.wordLength.setGeometry(QtCore.QRect(260, 90, 113, 21))
        self.wordLength.setObjectName(_fromUtf8("wordLength"))
        self.label_4 = QtGui.QLabel(self.centralWidget)
        self.label_4.setGeometry(QtCore.QRect(10, 90, 151, 16))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.distributionWindow = QtGui.QLineEdit(self.centralWidget)
        self.distributionWindow.setGeometry(QtCore.QRect(260, 120, 113, 21))
        self.distributionWindow.setObjectName(_fromUtf8("distributionWindow"))
        self.label_5 = QtGui.QLabel(self.centralWidget)
        self.label_5.setGeometry(QtCore.QRect(10, 120, 181, 16))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.label_6 = QtGui.QLabel(self.centralWidget)
        self.label_6.setGeometry(QtCore.QRect(10, 150, 59, 16))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.trainingTime = QtGui.QLineEdit(self.centralWidget)
        self.trainingTime.setGeometry(QtCore.QRect(260, 200, 113, 21))
        self.trainingTime.setObjectName(_fromUtf8("trainingTime"))
        self.documentWindow = QtGui.QLineEdit(self.centralWidget)
        self.documentWindow.setGeometry(QtCore.QRect(260, 170, 113, 21))
        self.documentWindow.setObjectName(_fromUtf8("documentWindow"))
        self.label_7 = QtGui.QLabel(self.centralWidget)
        self.label_7.setGeometry(QtCore.QRect(10, 170, 191, 16))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.line_2 = QtGui.QFrame(self.centralWidget)
        self.line_2.setGeometry(QtCore.QRect(50, 160, 118, 3))
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.label_8 = QtGui.QLabel(self.centralWidget)
        self.label_8.setGeometry(QtCore.QRect(10, 200, 151, 16))
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.chooseContextFolder = QtGui.QPushButton(self.centralWidget)
        self.chooseContextFolder.setGeometry(QtCore.QRect(260, 270, 115, 32))
        self.chooseContextFolder.setObjectName(_fromUtf8("chooseContextFolder"))
        self.label_9 = QtGui.QLabel(self.centralWidget)
        self.label_9.setGeometry(QtCore.QRect(10, 280, 151, 16))
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.line_3 = QtGui.QFrame(self.centralWidget)
        self.line_3.setGeometry(QtCore.QRect(50, 240, 118, 3))
        self.line_3.setFrameShape(QtGui.QFrame.HLine)
        self.line_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_3.setObjectName(_fromUtf8("line_3"))
        self.label_10 = QtGui.QLabel(self.centralWidget)
        self.label_10.setGeometry(QtCore.QRect(10, 250, 191, 16))
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.label_11 = QtGui.QLabel(self.centralWidget)
        self.label_11.setGeometry(QtCore.QRect(10, 230, 59, 16))
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.chooseMainFolder = QtGui.QPushButton(self.centralWidget)
        self.chooseMainFolder.setGeometry(QtCore.QRect(260, 240, 115, 32))
        self.chooseMainFolder.setObjectName(_fromUtf8("chooseMainFolder"))
        self.startButton = QtGui.QPushButton(self.centralWidget)
        self.startButton.setGeometry(QtCore.QRect(260, 350, 115, 32))
        self.startButton.setObjectName(_fromUtf8("startButton"))
        LDAPlusPlus.setCentralWidget(self.centralWidget)
        self.menuBar = QtGui.QMenuBar(LDAPlusPlus)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 383, 22))
        self.menuBar.setObjectName(_fromUtf8("menuBar"))
        self.menuLDAPlusPlus = QtGui.QMenu(self.menuBar)
        self.menuLDAPlusPlus.setObjectName(_fromUtf8("menuLDAPlusPlus"))
        LDAPlusPlus.setMenuBar(self.menuBar)
        self.mainToolBar = QtGui.QToolBar(LDAPlusPlus)
        self.mainToolBar.setObjectName(_fromUtf8("mainToolBar"))
        LDAPlusPlus.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtGui.QStatusBar(LDAPlusPlus)
        self.statusBar.setObjectName(_fromUtf8("statusBar"))
        LDAPlusPlus.setStatusBar(self.statusBar)
        self.menuBar.addAction(self.menuLDAPlusPlus.menuAction())

        self.retranslateUi(LDAPlusPlus)
        QtCore.QMetaObject.connectSlotsByName(LDAPlusPlus)

    def retranslateUi(self, LDAPlusPlus):
        LDAPlusPlus.setWindowTitle(_translate("LDAPlusPlus", "LDAPlusPlus", None))
        self.label.setText(_translate("LDAPlusPlus", "SAX", None))
        self.saxDuration.setText(_translate("LDAPlusPlus", "1", None))
        self.label_2.setText(_translate("LDAPlusPlus", "Duration (hours)", None))
        self.alphabetSize.setText(_translate("LDAPlusPlus", "5", None))
        self.label_3.setText(_translate("LDAPlusPlus", "Alphabet Size", None))
        self.wordLength.setText(_translate("LDAPlusPlus", "3", None))
        self.label_4.setText(_translate("LDAPlusPlus", "Word length", None))
        self.distributionWindow.setText(_translate("LDAPlusPlus", "24", None))
        self.label_5.setText(_translate("LDAPlusPlus", "Distribution Window (hours)", None))
        self.label_6.setText(_translate("LDAPlusPlus", "LDA", None))
        self.trainingTime.setText(_translate("LDAPlusPlus", "24", None))
        self.documentWindow.setText(_translate("LDAPlusPlus", "4", None))
        self.label_7.setText(_translate("LDAPlusPlus", "Document Window (hours)", None))
        self.label_8.setText(_translate("LDAPlusPlus", "Training Time", None))
        self.chooseContextFolder.setText(_translate("LDAPlusPlus", "Choose", None))
        self.label_9.setText(_translate("LDAPlusPlus", "Correlated Data Stream", None))
        self.label_10.setText(_translate("LDAPlusPlus", "Main Data Stream", None))
        self.label_11.setText(_translate("LDAPlusPlus", "Data", None))
        self.chooseMainFolder.setText(_translate("LDAPlusPlus", "Choose", None))
        self.startButton.setText(_translate("LDAPlusPlus", "Start", None))
        self.menuLDAPlusPlus.setTitle(_translate("LDAPlusPlus", "LDAPlusPlus", None))

