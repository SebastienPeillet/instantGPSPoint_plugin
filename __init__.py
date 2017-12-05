"""
Roam search plugin

Install into roam install\plugins\gpsPointDef

Add the following config to project.config

plugins:
 - catchGPSPoint_plugin
 
getgpspointlayer:
 - layer
 
where layer is the layer name found in the project.
"""
from PyQt4.QtGui import QWidget, QGridLayout, QLabel
from roam.api.plugins import Page
import instantGPSPoint

def toolbars():
    return [instantGPSPoint.instantGPSPointToolBar]
    
