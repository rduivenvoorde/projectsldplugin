# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ProjectSldPlugin
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
 This script initializes the plugin, making it known to QGIS.
"""
import os
import site

site.addsitedir(os.path.abspath('%s/ext-libs' % os.path.dirname(__file__)))

def classFactory(iface):
    # load ProjectSldPlugin class from file ProjectSldPlugin
    from projectsldplugin import ProjectSldPlugin
    return ProjectSldPlugin(iface)
