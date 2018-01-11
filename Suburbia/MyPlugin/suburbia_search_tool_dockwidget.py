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
from PyQt4.QtCore import pyqtSignal,pyqtSlot
from PyQt4 import QtGui, QtCore, uic
from qgis.core import *
from qgis.networkanalysis import *
from qgis.gui import *

import os.path

import resources

import os
import os.path
import random
import csv
import time

from . import utility_functions as uf


FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'suburbia_search_tool_dockwidget_base.ui'))


class MyPluginDockWidget(QtGui.QDockWidget, FORM_CLASS):

    closingPlugin = pyqtSignal()

    updateAttribute = QtCore.pyqtSignal(str)


    def __init__(self, iface, parent=None):
        """Constructor."""
        super(MyPluginDockWidget, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.TabPreferences.setEnabled(False)
        self.TabMetrics.setEnabled(False)

        # define globals
        self.iface = iface
        self.pref =[0,0,0,0]
        self.plugin_dir = os.path.dirname(__file__)
        self.canvas = self.iface.mapCanvas()

        #data
        self.loadDataRotterdam()
        self.iface.projectRead.connect(self.updateLayers)
        self.iface.newProjectCreated.connect(self.updateLayers)
        self.layers = self.iface.legendInterface().layers()



        #input
        self.ButtonConfirm.clicked.connect(self.Confirm)
        self.ButtonExplore.clicked.connect(self.Explore)
        self.ButtonLocate.clicked.connect(self.Locate)
        self.ButtonAdjustPreferences.clicked.connect(self.Confirm)





    def closeEvent(self, event):
        self.closingPlugin.emit()
        event.accept()

#######
#    Visulisation
#######

#######
#    Analysis functions
#######

    def Confirm(self):
        if self.ButtonAgree.isChecked():
            self.TabTerms.setEnabled(False)
            self.TabPreferences.setEnabled(True)
            self.TabMetrics.setEnabled(False)



    def Explore(self):
        self.pref[0] = self.SliderPeople.value()
        self.pref[1] = self.SliderChild.value()
        self.pref[2] = self.SliderAccess.value()
        self.pref[3] = self.SliderAfford.value()
        self.TabPreferences.setEnabled(False)
        self.TabMetrics.setEnabled(True)

    def Locate(self):
        if not self.EnterPostalCode == "":
            self.pref[0] = self.SliderPeople.value()
            self.pref[1] = self.SliderChild.value()
            self.pref[2] = self.SliderAccess.value()
            self.pref[3] = self.SliderAfford.value()
            self.TabPreferences.setEnabled(False)
            self.TabMetrics.setEnabled(True)



#######
#   Data functions
#######

    def loadDataRotterdam(self, filename=""):
        scenario_open = False
        scenario_file = os.path.join(os.path.dirname(__file__), 'sampledata', '2018-01-09_Suburbia_2016_v3.qgs')
        # check if file exists
        if os.path.isfile(scenario_file):
            self.iface.addProject(scenario_file)
            scenario_open = True
        else:
            last_dir = uf.getLastDir("SDSS")
            new_file = QtGui.QFileDialog.getOpenFileName(self, "", last_dir, "(*.qgs)")
            if new_file:
                self.iface.addProject(unicode(new_file))
                scenario_open = True
        if scenario_open:
            self.updateLayers()

    def updateLayers(self):
        layers = uf.getLegendLayers(self.iface, 'all', 'all')
        if layers:
            layer_names = uf.getLayersListNames(layers)
            self.setSelectedLayer()
        else:
            self.clearChart()

    def baseAttributes(self):
        # get summary of the attribute
        layer = uf.getLegendLayerByName(self.iface, "Rotterdam_gridStatistics")
        summary = []
        self.scenarioAttributes["Rotterdam"] = summary
        # send this to the table
        self.clearTable()
        self.updateTable()

    def setSelectedLayer(self):
        layer_name = "BU_NAAM"
        layer = uf.getLegendLayerByName(self.iface, layer_name)
        self.updateAttributes(layer)

    def updateAttributes(self, layer):
        if layer:
            self.clearReport()
            self.clearChart()
            fields = uf.getFieldNames(layer)
            if fields:
                # send list to the report list window
                self.updateReport(fields)



