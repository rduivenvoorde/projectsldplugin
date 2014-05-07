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
import requests
from requests.auth import HTTPBasicAuth

#http://localhost/cgi-bin/mapserv?map=/usr/lib/cgi-bin/b3p.map&&SERVICE=WMS&VERSION=1.3.0&REQUEST=GetMap&BBOX=4386.87996086938073859,304945.87847349571529776,286086.88017670798581094,621081.30985224642790854&CRS=EPSG:28992&WIDTH=388&HEIGHT=435&LAYERS=provincies,autowegen,plaatsen&STYLES=&FORMAT=image/png&TRANSPARENT=TRUE&sld=http://localhost/b3p.sld

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

        self.SETTINGS_SECTION = '/projectsldplugin/'
        self.filename = self.getSettingsValue('lastfile')

        # Create the dialog (after translation) and keep reference
        self.dlg = ProjectSldPluginDialog()
        self.dlg.ui.cbx_save_as_file.toggled.connect(self.saveAsFileToggled)
        self.dlg.ui.cbx_post_to_server.toggled.connect(self.postToServerToggled)
        self.dlg.ui.btn_filename.clicked.connect(self.filenameButtonClicked)

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
        self.dlg.ui.le_workspace.setText(self.getSettingsValue('default-workspace'))
        self.dlg.ui.le_post_url.setText(config.params['post-url'])
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result == 1:
            self.createProjectSld()

    def debug(self, string):
        print "###### DEBUG"
        print string

    def postToServerToggled(self):
        checked = self.dlg.ui.cbx_post_to_server.isChecked()
        self.dlg.ui.lbl_workspace.setEnabled(checked)
        self.dlg.ui.le_workspace.setEnabled(checked)

    def saveAsFileToggled(self):
        checked = self.dlg.ui.cbx_save_as_file.isChecked()
        # disable or enable the inputs
        self.dlg.ui.lbl_filename.setEnabled(checked)
        self.dlg.ui.le_filename.setEnabled(checked)
        self.dlg.ui.btn_filename.setEnabled(checked)
        if checked:
            self.dlg.ui.le_filename.setText(self.getSettingsValue('lastfile'))
        else:
            self.dlg.ui.le_filename.setText('')

    def getSettingsValue(self, key):
        if QSettings().contains(self.SETTINGS_SECTION + key):
            key = self.SETTINGS_SECTION + key
            if QGis.QGIS_VERSION_INT < 10900: # qgis <= 1.8
                return unicode(QSettings().value(key).toString())
            else:
                return unicode(QSettings().value(key))
        elif config.params.has_key(key):
            return config.params[key]
        else:
            return u''
    def setSettingsValue(self, key, value):
        key = self.SETTINGS_SECTION + key
        QSettings().setValue(key, value)

    def filenameButtonClicked(self):
        (self.filename, filter) = QFileDialog.getSaveFileNameAndFilter(
            self.iface.mainWindow(),
            "SLD bestand opslaan als...",
            os.path.realpath(self.filename),
            "sld files (*.sld)")
        fn, fileextension = os.path.splitext(unicode(self.filename))
        if len(fn) == 0: # user choose cancel
            return
        #if fileextension != '.sld':
        #    self.filename = fn + '.sld'
        # save this filename in settings for later
        self.dlg.ui.le_filename.setText(self.filename)

    def createProjectSld(self):
        if self.dlg.ui.cbx_save_as_file.isChecked() == False:
            file = QTemporaryFile(QDir.tempPath()+os.sep+'qgis_XXXXXX.sld')
            file.open()
            self.filename = file.fileName()
        else:
            try:
                file = open(self.filename, "w")
            except:
                self.iface.messageBar().pushMessage('Fout', 
                    'Kan het bestand "'+
                    unicode(self.filename) + '" niet opslaan. Is dit een geldige bestandsnaam en schrijfbaar?', level=QgsMessageBar.CRITICAL, duration=5)
                return

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
                self.addFillElementToGraphicMark(resultdom)
            else:
                layer_dom = parse(fname)
                namedlayer = layer_dom.getElementsByTagName('NamedLayer')[0]
                self.addFillElementToGraphicMark(namedlayer)
                resultdom.getElementsByTagName('StyledLayerDescriptor')[0].appendChild(namedlayer)

            # append both fname AND temporary file object (to prevent it being removed)
            layerslds.append((fname, f))

        if resultdom == None:
            self.iface.messageBar().pushMessage("Warning", "Geen sld bestand aangemaakt. Zijn er wel vector lagen aanwezig?", level=QgsMessageBar.WARNING, duration=510)
            return

        # multiplier for stroke width in sld
        self.multiplyStrokeWidth(resultdom)
        # multiplier for point size symbols
        self.multipyPointSize(resultdom)

        #print resultdom.toxml()
        # toprettyxml looks better, but has an awfull lot of whitespace, 
        # see: http://ronrothman.com/public/leftbraned/xml-dom-minidom-toprettyxml-and-silly-whitespace/
        #xml = resultdom.toprettyxml()
        xml = resultdom.toxml()

        # now replace all replacements from config
        for key in config.replace:
            xml = xml.replace(key, config.replace[key])
        file.write(xml)
        file.close()

        # only remember if checked and succesfull
        if self.dlg.ui.cbx_save_as_file.isChecked():
            self.setSettingsValue('lastfile', self.filename)
            self.iface.messageBar().pushMessage("Info", "Sld succesvol opgeslagen als: "+unicode(self.filename), level=QgsMessageBar.INFO, duration=2)

        if self.dlg.ui.cbx_post_to_server.isChecked():
            self.post_sld()

    def post_sld(self):
        url = config.params['post-url']
        files = {'file': open(self.filename, 'rb')}
        workspace = self.dlg.ui.le_workspace.text()
        workspacekey = config.params['post-workspace-param']
        self.setSettingsValue('default-workspace', workspace)
        username = config.params['post-username']
        password = config.params['post-password']
        try:
            r = requests.post(url,
                timeout=10,
                data={workspacekey:workspace},
                files=files,
                auth=HTTPBasicAuth(username, password))
            if r.status_code == 200:
                self.iface.messageBar().pushMessage("Info", "Sld succesvol verstuurd... ", level=QgsMessageBar.INFO, duration=2)
            else:
                self.iface.messageBar().pushMessage("Fout", 
                    "Probleem bij het versturen van de sld: "+
                    unicode(r.status_code), level=QgsMessageBar.CRITICAL, duration=5)
        except requests.exceptions.Timeout:
            self.iface.messageBar().pushMessage("Fout", 
                "Timout bij posten naar: "+
                unicode(url) + ". Is de url wel juist?", level=QgsMessageBar.CRITICAL, duration=5)


    # <se:SvgParameter name="stroke-width">2</se:SvgParameter>
    def multiplyStrokeWidth(self, dom):
        strokeWidthMultiplier = float(config.params['stroke-width-multiplier'])
        svgparams = dom.getElementsByTagName('se:SvgParameter')
        if len(svgparams)>0:
            for svgparam in svgparams:
                if svgparam.getAttribute('name')=='stroke-width':
                    width = float(svgparam.childNodes[0].nodeValue)
                    svgparam.childNodes[0].nodeValue=width*strokeWidthMultiplier

    # <se:PointSymbolizer>..<se:Size>2</se:Size>
    def multipyPointSize(self, dom):
        pointSizeMultiplier = float(config.params['point-size-multiplier'])
        pointsyms = dom.getElementsByTagName('se:PointSymbolizer')
        if len(pointsyms)>0:
            for pointsym in pointsyms:
                size = float(self.childNodeValue(pointsym, 'se:Size'))
                sizeElement = pointsym.getElementsByTagName('se:Size')
                sizeElement[0].childNodes[0].nodeValue=size*pointSizeMultiplier

    def addFillElementToGraphicMark(self, dom):
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
