# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ProjectSldPluginDialog
                                 SLD Export

 Create one combined SLD file for all layers in the current project. Save
 the file locally or publish it to B3P Kaartenbalie or Geoserver.

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
