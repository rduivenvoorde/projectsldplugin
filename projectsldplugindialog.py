# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ProjectSldPluginDialog
                                 A QGIS plugin
 Merges the sld for all layers in a project to one sld file.
                             -------------------
        begin                : 2013-11-25
        copyright            : (C) 2013 by B3Partners
        email                : info@b3p.nl
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

from PyQt4 import QtCore, QtGui
from ui_projectsldplugin import Ui_ProjectSldPlugin
# create the dialog for zoom to point


class ProjectSldPluginDialog(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.ui = Ui_ProjectSldPlugin()
        self.ui.setupUi(self)
