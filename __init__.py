# -*- coding: utf-8 -*-
"""
***************************************************************************
 __init__.py
                                An Intramaps plugin
 ToolBar with buttons on the fly to record instant GPS point with attribute
                            -------------------
        begin				 : 2017-12-04
        last				 : 2017-12-06
        copyright			 : (C) 2017 by Peillet Sebastien
        email				 : peillet.seb@gmail.com
 ***************************************************************************/

 /***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 3 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/

Install into roam install\plugins\gpsPointDef

Add the following config to project.config

plugins:
 - instantGPSPoint_plugin
 
gpspointlayer:
 - layer

gpspointattr:
 - attribute field name
 
gpspointtime: (optionnal field name for time)
 - time field name

gpspointoption:
 - option 1 (string)
 - option 2 (string)
 - etc
 
where layer is the layer name found in the project.
"""

from PyQt4.QtGui import QWidget, QGridLayout, QLabel
from roam.api.plugins import Page
import instantGPSPoint

def toolbars():
    return [instantGPSPoint.instantGPSPointToolBar]
    
