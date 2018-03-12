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

from qgis.core import QgsMapLayer, QgsMapLayerRegistry, QgsFeature, QgsFeatureRequest, QgsRectangle, QgsCoordinateReferenceSystem, QgsGeometry

from roam.api import utils
import logging
from roam.flickwidget import FlickCharm
from roam.api.events import RoamEvents
from roam.api.plugins import Page, ToolBar
from roam.api import GPS

logger = logging.getLogger("roam")
# widget, base = loadUiType(resolve("gpsPointDef.ui"))

class instantGPSPointToolBar(ToolBar):
    title = "instantGPSPointToolBar"
    def __init__(self, api, parent=None):
        super(instantGPSPointToolBar, self).__init__(parent)
        self.mapwindow = api.mapwindow
        self.gpsService = GPS
        # logger.info(str(self.gpsService))
        self.gpsService.connectGPS('')
        self.gpsService.crs = QgsCoordinateReferenceSystem(2972)
        self.cland_list = [
            'Chantier CLAND','Carbet CLAND','Village','1 Carbet',
            '2 Carbets','3 Carbets','4 Carbets','5 Carbets',
            '6 Carbets','7 Carbets','8 Carbets','9 Carbets'
        ]
        self.legal_list = [
            'Chantier LEGAL','Carbet LEGAL'
        ]

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
        field_type = settings['gpspointtype']
        self.w_layer_type_field = field_type[0]
        field_obs = settings['gpspointobs']
        self.w_layer_obs_field = field_obs[0]
        try :
            field_time = settings['gpspointtime']
            self.w_layer_time_field = field_time[0]
        except (KeyError) :
            logger.info('No time field in project.config')
            self.w_layer_time_field = None
        try :
            field_date = settings['gpspointdate']
            self.w_layer_date_field = field_date[0]
        except (KeyError) :
            logger.info('No date field in project.config')
            self.w_layer_date_field = None
        try :
            field_nom = settings['gpspointnom']
            self.w_layer_nom_field = field_nom[0]
        except (KeyError) :
            logger.info('No nom field in project.config')
            self.w_layer_nom_field = None
        try :
            field_titre = settings['gpspointtitre']
            self.w_layer_titre_field = field_titre[0]
        except (KeyError) :
            logger.info('No titre field in project.config')
            self.w_layer_titre_field = None
        try :
            field_pollution = settings['gpspointpollution']
            self.w_layer_pollution_field = field_pollution[0]
        except (KeyError) :
            logger.info('No pollution field in project.config')
            self.w_layer_pollution_field = None
        try :
            field_rehab = settings['gpspointrehab']
            self.w_layer_rehab_field = field_rehab[0]
        except (KeyError) :
            logger.info('No rehab field in project.config')
            self.w_layer_rehab_field = None
        try :
            intersect_layer = settings['gpsintersectlayer']
            self.intersect_layer = field_rehab[0]
        except (KeyError) :
            logger.info('No intersect layer in project.config')
            self.intersect_layer = None
        try :
            intersect_titre = settings['gpsintersecttitre']
            self.intersect_titre = field_rehab[0]
        except (KeyError) :
            logger.info('No intersect_titre field in project.config')
            self.intersect_layer = None
        try :
            intersect_nom = settings['gpsintersectnom']
            self.intersect_nom = field_rehab[0]
        except (KeyError) :
            logger.info('No intersect_nom field in project.config')
            self.intersect_layer = None
    
    def get_natures_def(self) :
        settings = self.project.settings
        self.natures_def = settings['gpspointoption']
    
    def add_buttons(self) :
        self.buttons= []
        for nat in self.natures_def :
            self.buttons.append(QAction(nat[0],self))
        for i in range(0,len(self.buttons)) :
            self.buttons[i].list_info = self.natures_def[i]
            self.addAction(self.buttons[i])
            self.buttons[i].triggered[()].connect(lambda i=i: self.add_record(self.buttons[i].list_info))
        
    def add_record(self, list_info):
        f_type = list_info[1]
        if len(list_info)>2 :
            f_obs = list_info[2]
        else : 
            f_obs = None
        logger.info(str(self.gpsService.postion.x())+"x"+str(self.gpsService.postion.y())+"y")
        if self.gpsService.isConnected == True :
            ft = QgsFeature(self.w_layer.pendingFields())
            point = self.gpsService.postion
            ft.setGeometry(QgsGeometry.fromPoint(point))
            
            index = self.w_layer.fieldNameIndex('Waypointid')
            id_max = 0
            for feat in self.w_layer.getFeatures():
                id = feat.attribute('Waypointid')
                id_max = max(id_max, int(id))

            new_id = int(id_max) + 1
            ft.setAttribute(index, new_id)       
            
            index = self.w_layer.fieldNameIndex(self.w_layer_type_field)
            ft.setAttribute(index, f_type)

            if self.intersect_layer != None and list_info[0] in self.legal_list :
                geom_rect = ft.geometry().boundingBox()
                intersect_feat_it = self.intersect_layer.getFeatures(QgsFeatureRequest().setFilterRect(geom_rect))
                try :
                    intersect_feat = next(intersect_feat_it)
                    if self.w_layer_nom_field != None :
                        nom_attr = intersect_feat.attribute(self.intersect_nom)
                        index = self.w_layer.fieldNameIndex(self.w_layer_nom_field)
                        ft.setAttribute(index, nom_attr)
                    if self.w_layer_titre_field != None :
                        titre_attr = intersect_feat.attribute(self.intersect_titre)
                        index = self.w_layer.fieldNameIndex(self.w_layer_titre_field)
                        ft.setAttribute(index, titre_attr)
                except StopIteration :
                    pass

            elif list_info[0] in self.cland_list :
                if self.w_layer_nom_field != None :
                    index = self.w_layer.fieldNameIndex(self.w_layer_nom_field)
                    ft.setAttribute(index, 'clandestin')
                if self.w_layer_titre_field != None :
                    index = self.w_layer.fieldNameIndex(self.w_layer_titre_field)
                    ft.setAttribute(index, 'sans titre')
                if self.w_layer_pollution_field != None :
                    index = self.w_layer.fieldNameIndex(self.w_layer_pollution_field)
                    ft.setAttribute(index, 'o')
                if self.w_layer_rehab_field != None :
                    index = self.w_layer.fieldNameIndex(self.w_layer_rehab_field)
                    ft.setAttribute(index, 'O')

            index = self.w_layer.fieldNameIndex(self.w_layer_obs_field)
            ft.setAttribute(index, f_obs)
            
            if self.w_layer_time_field != None :
                index = self.w_layer.fieldNameIndex(self.w_layer_time_field)
                ft.setAttribute(index, time.strftime("%H:%M:%S",time.localtime()))
            if self.w_layer_date_field != None :
                index = self.w_layer.fieldNameIndex(self.w_layer_date_field)
                ft.setAttribute(index, time.strftime("%Y%m%d",time.localtime()))
            
            self.w_layer.startEditing()
            pr = self.w_layer.dataProvider()
            pr.addFeatures([ft])
            
            self.w_layer.commitChanges()
            ft = None
            
        else :
            logger.info("No GPS connected, no coordinates for {} record".format(nature))

        

        
