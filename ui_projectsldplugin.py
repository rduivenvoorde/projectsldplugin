# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_projectsldplugin.ui'
#
# Created: Mon Nov 25 21:31:31 2013
#      by: PyQt4 UI code generator 4.10.3
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

class Ui_ProjectSldPlugin(object):
    def setupUi(self, ProjectSldPlugin):
        ProjectSldPlugin.setObjectName(_fromUtf8("ProjectSldPlugin"))
        ProjectSldPlugin.resize(400, 300)
        self.buttonBox = QtGui.QDialogButtonBox(ProjectSldPlugin)
        self.buttonBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))

        self.retranslateUi(ProjectSldPlugin)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ProjectSldPlugin.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ProjectSldPlugin.reject)
        QtCore.QMetaObject.connectSlotsByName(ProjectSldPlugin)

    def retranslateUi(self, ProjectSldPlugin):
        ProjectSldPlugin.setWindowTitle(_translate("ProjectSldPlugin", "ProjectSldPlugin", None))

