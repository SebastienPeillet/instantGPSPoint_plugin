import sqlite3
import time
import os
import struct
from PyQt4.QtCore import Qt, QObject, pyqtSignal, QThread, QEvent
from PyQt4.QtGui import QWidget, QGridLayout, QLabel, QListWidgetItem, QStyledItemDelegate, QFontMetricsF, QTextOption, QAction, QPushButton
from PyQt4.uic import loadUiType

from qgis.core import QgsMapLayer, QgsMapLayerRegistry, QgsFeatureRequest, QgsRectangle

import roam.api.utils
import logging
from roam.flickwidget import FlickCharm
from roam.api.events import RoamEvents
from roam.api.plugins import Page, ToolBar

logger = logging.getLogger("roam")
info = logger.info
# widget, base = loadUiType(resolve("gpsPointDef.ui"))

class instantGPSPointToolBar(ToolBar):
    title = "instantGPSPointToolBar"
    def __init__(self, api, parent=None):
        super(instantGPSPointToolBar, self).__init__(parent)
        self.mapwindow = api.mapwindow
        # self.button = QAction("Orpaillage", self)
        # self.addAction(self.button)
        # self.button2 = QAction("Chablis", self)
        # self.addAction(self.button2)
        # self.button.triggered.connect(lambda: self.add_record("Orpaillage"))
        # self.button2.triggered.connect(lambda: self.add_record("Chablis"))

    def unload(self):
        pass

    def project_loaded(self, project):
        self.project = project
        self.work_layer()
        self.natures_def()
        self.add_buttons()
    
    def work_layer(self) :
        settings = self.project.settings
        layername = settings['gpspointlayer']
        self.w_layer = roam.api.utils.layer_by_name(layername[0])
    
    def natures_def(self) :
        settings = self.project.settings
        self.natures_def = settings['gpspointnature']
    
    def add_buttons(self) :
        self.buttons= []
        for nat in self.natures_def :
            self.buttons.append(QAction(nat,self))
        for button in self.buttons :
            self.addAction(button)
            button.triggered.connect(lambda: self.add_record(button.text))
        
    def add_record(self, nature):
        for nat in self.natures_def :
            info("{}".format(nat))
        

        
