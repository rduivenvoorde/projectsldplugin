# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_projectsldplugin.ui'
#
# Created: Tue Apr 15 17:06:51 2014
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
        ProjectSldPlugin.resize(566, 240)
        self.gridLayout = QtGui.QGridLayout(ProjectSldPlugin)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.buttonBox = QtGui.QDialogButtonBox(ProjectSldPlugin)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 7, 3, 1, 2)
        self.lbl_filename = QtGui.QLabel(ProjectSldPlugin)
        self.lbl_filename.setEnabled(False)
        self.lbl_filename.setObjectName(_fromUtf8("lbl_filename"))
        self.gridLayout.addWidget(self.lbl_filename, 6, 1, 1, 1)
        self.cbx_save_as_file = QtGui.QCheckBox(ProjectSldPlugin)
        self.cbx_save_as_file.setChecked(False)
        self.cbx_save_as_file.setObjectName(_fromUtf8("cbx_save_as_file"))
        self.gridLayout.addWidget(self.cbx_save_as_file, 5, 1, 1, 2)
        self.btn_filename = QtGui.QPushButton(ProjectSldPlugin)
        self.btn_filename.setEnabled(False)
        self.btn_filename.setObjectName(_fromUtf8("btn_filename"))
        self.gridLayout.addWidget(self.btn_filename, 6, 4, 1, 1)
        self.le_filename = QtGui.QLineEdit(ProjectSldPlugin)
        self.le_filename.setEnabled(False)
        self.le_filename.setObjectName(_fromUtf8("le_filename"))
        self.gridLayout.addWidget(self.le_filename, 6, 2, 1, 2)
        self.le_post_url = QtGui.QLineEdit(ProjectSldPlugin)
        self.le_post_url.setEnabled(False)
        self.le_post_url.setReadOnly(True)
        self.le_post_url.setObjectName(_fromUtf8("le_post_url"))
        self.gridLayout.addWidget(self.le_post_url, 3, 2, 1, 3)
        self.cbx_post_to_server = QtGui.QCheckBox(ProjectSldPlugin)
        self.cbx_post_to_server.setChecked(True)
        self.cbx_post_to_server.setObjectName(_fromUtf8("cbx_post_to_server"))
        self.gridLayout.addWidget(self.cbx_post_to_server, 3, 1, 1, 1)
        self.lbl_workspace = QtGui.QLabel(ProjectSldPlugin)
        self.lbl_workspace.setObjectName(_fromUtf8("lbl_workspace"))
        self.gridLayout.addWidget(self.lbl_workspace, 4, 1, 1, 1)
        self.le_workspace = QtGui.QLineEdit(ProjectSldPlugin)
        self.le_workspace.setText(_fromUtf8(""))
        self.le_workspace.setObjectName(_fromUtf8("le_workspace"))
        self.gridLayout.addWidget(self.le_workspace, 4, 2, 1, 3)

        self.retranslateUi(ProjectSldPlugin)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ProjectSldPlugin.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ProjectSldPlugin.reject)
        QtCore.QMetaObject.connectSlotsByName(ProjectSldPlugin)

    def retranslateUi(self, ProjectSldPlugin):
        ProjectSldPlugin.setWindowTitle(_translate("ProjectSldPlugin", "Project Sld Plugin", None))
        self.lbl_filename.setText(_translate("ProjectSldPlugin", "Bestand", None))
        self.cbx_save_as_file.setText(_translate("ProjectSldPlugin", "Opslaan als bestand", None))
        self.btn_filename.setText(_translate("ProjectSldPlugin", "Browse", None))
        self.cbx_post_to_server.setText(_translate("ProjectSldPlugin", "POST naar server", None))
        self.lbl_workspace.setText(_translate("ProjectSldPlugin", "Workspace", None))

