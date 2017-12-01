# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Spatial
                                 A QGIS plugin
 The green housing search
                             -------------------
        begin                : 2017-12-01
        copyright            : (C) 2017 by Elias Vetter
        email                : vetterelias@gmail.com
        git sha              : $Format:%H$
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


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load Spatial class from file Spatial.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .suburbia import Spatial
    return Spatial(iface)
