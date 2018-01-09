# -*- coding: utf-8 -*-
"""
/***************************************************************************
 MyPluginDockWidget
                                 A QGIS plugin
 Green Housing Search
                             -------------------
        begin                : 2018-01-09
        git sha              : $Format:%H$
        copyright            : (C) 2018 by Elias Vetter
        email                : vetterelias@gmail.com
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



import os
from PyQt4 import QtGui, uic
from PyQt4.QtCore import pyqtSignal

import os.path


FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'suburbia_search_tool_dockwidget_base.ui'))


class MyPluginDockWidget(QtGui.QDockWidget, FORM_CLASS):

    closingPlugin = pyqtSignal()

    def __init__(self, iface, parent=None):
        """Constructor."""
        super(MyPluginDockWidget, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)

        # define globals
        self.iface = iface

        #data
        self.loadDataRotterdam()

        self.layers = self.iface.legendInterface().layers()
        self.layer_list = []
        for layer in self.layers:
            self.layer_list.append(layer.name())







    def closeEvent(self, event):
        self.closingPlugin.emit()
        event.accept()

#######
#    Visulisation
#######

#######
#    Analysis functions
#######


    def explore(self):
        if People > 0:
            Peop


#######
#   Data functions
#######
    def loadDataRotterdam(self):
        try:
            data_path = os.path.join(os.path.dirname(__file__), 'sampledata','2018-01-09_Suburbia_2016.qgs')
        except:
            self.errorOccurs()
        self.iface.addProject(data_path)
        self.updateLayers()


    def updateLayers(self):
        self.layers = self.iface.legendInterface().layers()
        self.layer_list = []
        for layer in self.layers:
            self.layer_list.append(layer.name())

    def baseAttributes(self):
        # get summary of the attribute
        layer = uf.getLegendLayerByName(self.iface, "Rotterdam_gridStatistics")
        summary = []
        self.scenarioAttributes["Rotterdam"] = summary
        # send this to the table
        self.clearTable()
        self.updateTable()

    def addLayer(self, features):
        layers = self.iface.legendInterface().layers()
        layer_list = []
        for layer in layers:
            layer_list.append(layer.name())
        if 'Result' not in layer_list:
            self.active_layer = self.iface.activeLayer()
            if self.active_layer != None:
                self.layercrs = self.active_layer.crs()
            else:
                self.layercrs = self.layers[0].crs()
            #Create the memory layer for the result
            layeruri = 'Polygon?'
            #CRS needs to be specified
            crstext = 'PROJ4:%s' % self.layercrs.toProj4()
            layeruri = layeruri + 'crs=' + crstext
            self.memresult = QgsVectorLayer(layeruri, 'Result', 'memory')
            self.provider = self.memresult.dataProvider()
            fields = []
            self.memresult.startEditing()
            for i in range(len(self.titleList)):
                fields.append(QgsField(self.titleList[i], self.variantList[i]))
            self.provider.addAttributes(fields)
            self.memresult.setLayerTransparency(50)
            self.memresult.updateFields()
            self.memresult.commitChanges()
            QgsMapLayerRegistry.instance().addMapLayers([self.memresult])
        self.memresult.startEditing()
        self.provider.addFeatures(features)
        self.memresult.updateExtents()
        self.memresult.commitChanges()