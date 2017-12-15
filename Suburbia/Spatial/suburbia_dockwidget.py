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

from PyQt4 import QtGui, uic
from PyQt4.QtCore import pyqtSignal

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