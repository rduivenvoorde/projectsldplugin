# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ProjectSldPlugin
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
 This script initializes the plugin, making it known to QGIS.
"""
import os
import site

site.addsitedir(os.path.abspath('%s/ext-libs' % os.path.dirname(__file__)))

def classFactory(iface):
    # load ProjectSldPlugin class from file ProjectSldPlugin
    from projectsldplugin import ProjectSldPlugin
    return ProjectSldPlugin(iface)
