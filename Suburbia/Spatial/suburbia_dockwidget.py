# -*- coding: utf-8 -*-
"""
/***************************************************************************
 SpatialDockWidget
                                 A QGIS plugin
 The green housing search
                             -------------------
        begin                : 2017-12-05
        git sha              : $Format:%H$
        copyright            : (C) 2017 by Elias Vetter/TU Delft
        email                : vetterelisa@gmail.com
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

from PyQt4 import QtGui, QtCore, uic
from qgis.core import *
from qgis.networkanalysis import *
from qgis.gui import *

#for visualisation
import numpy
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import math as m

# Initialize Qt resources from file resources.py
import resources

import processing
import os
import os.path
import random
import webbrowser
import csv

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'suburbia_dockwidget_base.ui'))


class SpatialDockWidget(QtGui.QDockWidget, FORM_CLASS):

    closingPlugin = pyqtSignal()

    def __init__(self, iface, parent=None):
        """Constructor."""
        super(SpatialDockWidget, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)

        # define globals
        self.iface = iface
        self.canvas = self.iface.mapCanvas()

        # data
        self.iface.connect(self.openDataRotterdam)

        # Bind mouse click to canvas for adding new events
        self.map_canvas.mouseDoubleClickEvent = self.place_new_event

        # Bind buttons to specific path finding methods

    def closeEvent(self, event):
        self.closingPlugin.emit()
        event.accept()

  ######
  #  Analysis functions
  #####

    def yayClicked(self, mapPoint, mouseButton):
        if mapPoint:
            self.x = mapPoint.x()
            self.y = mapPoint.y()
            self.defineName(self.x, self.y)

    ######
    #  Data Functions
    #####


    def loadDataRotterdam(self):
        try:
            data_path = os.path.join(os.path.dirname(__file__), 'sample_data','Rotterdam_Sample_Data.qgs')
        except:
            self.errorOccurs()
        self.iface.addProject(data_path)
        self.updateLayers()