# -*- coding: utf-8 -*-
"""
***************************************************************************
 instantGPSPoint.py
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
"""

import sqlite3
import time
import os
import struct
from PyQt4.QtCore import Qt, QObject, pyqtSignal, QThread, QEvent
from PyQt4.QtGui import QWidget, QGridLayout, QLabel, QListWidgetItem, QStyledItemDelegate, QFontMetricsF, QTextOption, QAction, QPushButton
from PyQt4.uic import loadUiType

from qgis.core import QgsMapLayer, QgsMapLayerRegistry, QgsFeatureRequest, QgsRectangle

from roam.api import utils, gps
import logging
from roam.flickwidget import FlickCharm
from roam.api.events import RoamEvents
from roam.api.plugins import Page, ToolBar

logger = logging.getLogger("roam")
# widget, base = loadUiType(resolve("gpsPointDef.ui"))

class instantGPSPointToolBar(ToolBar):
    title = "instantGPSPointToolBar"
    def __init__(self, api, parent=None):
        super(instantGPSPointToolBar, self).__init__(parent)
        self.mapwindow = api.mapwindow
        self.gpsService = gps.GPSService()
        self.gpsService.crs = 2972

    def unload(self):
        pass

    def project_loaded(self, project):
        self.project = project
        self.get_work_layer()
        self.get_natures_def()
        self.add_buttons()
    
    def get_work_layer(self) :
        settings = self.project.settings
        layername = settings['gpspointlayer']
        self.w_layer = utils.layer_by_name(layername[0])
        field_nat = settings['gpspointattr']
        self.w_layer_nat_field = field_nat[0]
        try :
            field_time = settings['gpspointtime']
            self.w_layer_time_field = field_time[0]
        except (KeyError) :
            logger.info('No time field in project.config')
            self.w_layer_time_field = None
            
    
    def get_natures_def(self) :
        settings = self.project.settings
        self.natures_def = settings['gpspointnature']
    
    def add_buttons(self) :
        self.buttons= []
        for nat in self.natures_def :
            self.buttons.append(QAction(nat,self))
        for i in range(0,len(self.buttons)) :
            self.addAction(self.buttons[i])
            self.buttons[i].triggered[()].connect(lambda i=i: self.add_record(self.buttons[i].text()))
        
    def add_record(self, nature):
        if self.gpsService.isConnected == True :
            ft = QgsFeature()
            point = self.gpsService.postion
            ft.setGeometry(point)
            
            self.w_layer.startEditing()
            pr = self.w_layer.dataProvider()
            pr.addFeatures([ft])
            
            index = self.w_layer.fieldNameIndex('id')
            self.w_layer.changeAttributeValue(ft.id(), index, ft.id())           
            
            index = self.w_layer.fieldNameIndex(self.w_layer_nat_field)
            self.w_layer.changeAttributeValue(ft.id(), index, nature)
            
            if self.w_layer_time_field != None :
                index = self.w_layer.fieldNameIndex(self.w_layer_time_field)
                self.w_layer.changeAttributeValue(ft.id(), index, time.strftime("%d-%m-%Y-%H:%M:%S",time.localtime()))
            self.w_layer.commitChanges()
            ft = None
            
        else :
            logger.info("No GPS connected, no coordinates for {} record".format(nature))

        

        
