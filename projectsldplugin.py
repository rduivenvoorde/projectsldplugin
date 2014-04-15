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
"""
# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
# Initialize Qt resources from file resources.py
import resources_rc
# Import the code for the dialog
from projectsldplugindialog import ProjectSldPluginDialog
import os
from xml.dom.minidom import parse, parseString

import config

# http://localhost/cgi-bin/mapserv?map=/usr/lib/cgi-bin/nl.map&SERVICE=WMS&VERSION=1.3.0&REQUEST=GetMap&BBOX=-15772.44905833539087325,339281.98529863281873986,335233.03839986532693729,606016.84424390434287488&CRS=EPSG:28992&WIDTH=479&HEIGHT=364&LAYERS=provincies,autowegen,plaatsen&STYLES=&FORMAT=image/png&SLD=http://localhost/kaas.sld

class ProjectSldPlugin:

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value("locale/userLocale")[0:2]
        localePath = os.path.join(self.plugin_dir, 'i18n', 'projectsldplugin_{}.qm'.format(locale))

        if os.path.exists(localePath):
            self.translator = QTranslator()
            self.translator.load(localePath)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = ProjectSldPluginDialog()

    def initGui(self):
        # Create action that will start plugin configuration
        self.action = QAction(
            QIcon(":/plugins/projectsldplugin/icon.png"),
            u"Project SLD plugin", self.iface.mainWindow())
        # connect the action to the run method
        self.action.triggered.connect(self.run)

        # Add toolbar button and menu item
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu(u"&projectsldplugin", self.action)

    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removePluginMenu(u"&projectsldplugin", self.action)
        self.iface.removeToolBarIcon(self.action)

    # run method that performs all the real work
    def run(self):
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result == 1:
            # TODO: check IF there are any vector layers here!!!
            self.createProjectSld()

    def debug(self, string):
        print "###### DEBUG"
        print string

    def createProjectSld(self):

        filename = "."
        if QSettings().contains("/projectsldplugin/lastfile"):
            if QGis.QGIS_VERSION_INT < 10900:
                # qgis <= 1.8
                filename = unicode(QSettings().value('/projectsldplugin/lastfile').toString())
            else:
                filename = unicode(QSettings().value('/projectsldplugin/lastfile'))
        (filename, filter) = QFileDialog.getSaveFileNameAndFilter(self.iface.mainWindow(),
                    "SLD bestand opslaan als...",
                    os.path.realpath(filename),
                    "sld files (*.sld)")
        fn, fileextension = os.path.splitext(unicode(filename))
        if len(fn) == 0: # user choose cancel
            return
        #if fileextension != '.sld':
        #    filename = fn + '.sld'
        # save this filename in settings for later
        QSettings().setValue('/projectsldplugin/lastfile', filename)
        file = open(filename, "w")

        resultdom = None

        # holding the QTemporaryFile handles here, just to be sure they are not
        # removed while working on the layerlist
        layerslds = []
        # for every layer
        for i in range (self.iface.mapCanvas().layerCount()-1, -1, -1):
            layer = self.iface.mapCanvas().layer(i)
            # for now: only vector layers (== type=0) style can be saved to sld
            if layer.type() >0:
                continue
            f = QTemporaryFile(QDir.tempPath()+os.sep+'qgis_XXXXXX.sld')
            f.open()
            fname = f.fileName()
            # create a sld in temporary dir
            layer.saveSldStyle(fname)
            if resultdom == None:
                resultdom = parse(fname) # is now holding a DOM of the first sld
                self.addFillElement2GraphicMark(resultdom)
            else:
                layer_dom = parse(fname)
                namedlayer = layer_dom.getElementsByTagName('NamedLayer')[0]
                self.addFillElement2GraphicMark(namedlayer)
                resultdom.getElementsByTagName('StyledLayerDescriptor')[0].appendChild(namedlayer)


            # append both fname AND temporary file object (to prevent it being removed)
            layerslds.append((fname, f))
        # create the sld wrapper tail
        #print layerslds
        #for filename, sldfile in layerslds:
        #    #print filename
        #    dom = parse(sldfile)
        #    # todo check length
        #    namedLayer = dom.getElementsByTagName('NamedLayer')[0]
        #    print namedLayer.toxml() # unicode

        #print resultdom.toxml()
        # toprettyxml looked better, but has an awfull lot of whitespace, 
        # see: http://ronrothman.com/public/leftbraned/xml-dom-minidom-toprettyxml-and-silly-whitespace/
        #xml = resultdom.toprettyxml()
        if resultdom == None:
            self.iface.messageBar().pushMessage("Warning", "Geen sld bestand aangemaakt. Zijn er wel vector lagen aanwezig?", level=QgsMessageBar.WARNING, duration=510)
            return
        xml = resultdom.toxml()


        #van = '<se:WellKnownName>x</se:WellKnownName>'
        #naar = '<se:WellKnownName>shape://times</se:WellKnownName>'
        #xml = xml.replace(van, naar)

        for keyvalue in config.replace:
            xml = xml.replace(keyvalue[0], keyvalue[1])

        file.write(xml)
        file.close()

        self.iface.messageBar().pushMessage("Info", "Succes: "+filename, level=QgsMessageBar.INFO, duration=5)

    def addFillElement2GraphicMark(self, dom):
        marks = dom.getElementsByTagName('se:Mark')
        if len(marks)>0:
            for mark in marks:
                mark_type = self.childNodeValue(mark, 'se:WellKnownName')
                # only adding fill for following 'wellknowname' types:
                # QGIS: only do: horline, line, cross, slash, backslash, x
                if mark_type in ['horline', 'line', 'cross', 'slash', 'backslash', 'x']:
                    stroke = mark.getElementsByTagName('se:Stroke')
                    if len(stroke):
                        stroke_color = self.childNodeValue(stroke[0], 'se:SvgParameter')
                        fill = parseString(u'<se:Fill xmlns:se="http://www.opengis.net/se"><se:CssParameter name="fill">'+stroke_color+u'</se:CssParameter></se:Fill>')
                        fill_elm = fill.getElementsByTagName('se:Fill')[0]
                        mark.appendChild(fill_elm)

    def childNodeValue(self, node, childName):
        nodes = node.getElementsByTagName(childName)
        if len(nodes)==1 and nodes[0].hasChildNodes():
            return nodes[0].childNodes[0].nodeValue
        if len(nodes)>1:
            arr = u''
            for child in nodes:
                # extra check, we only want direct childs
                if child.parentNode.nodeName==node.nodeName and child.hasChildNodes():
                    arr+=(child.childNodes[0].nodeValue)
                    arr+=','
            return arr.rstrip(',')
        return ''
