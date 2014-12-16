#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  MCwindow.py
#  
#  Copyright 2014 Labio <labio@labio-XPS-8300>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

# System
import time
import pygtk
pygtk.require('2.0')
import gtk
import gtk.gtkgl
import gobject
import sys
import os
import json 


# Imports
from OpenGL.GL import *
from OpenGL.GLU import *
from pprint import pprint
import random as rdm 

#GUI
#from MastersNewProjectDialog import *
from FileChooserWindow           import *
from pymol import cmd
from pymol.cgo import *

'''
if not sys.platform.startswith('win'):
    HOME = os.environ.get('HOME')
else:
    HOME = os.environ.get('PYMOL_PATH')
'''





def RunMCSimulation( project, parameters):
    """ Function doc """
    Job    =  str(len(project['Jobs']))
    folder = project['Folder']
    
    '''                                    
    --- ---------------------------------- ---
    ---                                    ---
    ---            Input File              ---
    ---                                    ---
    --- ---------------------------------- ---
    '''
    filename_in = os.path.join(folder, Job+'_MonteCarlo.in')
    arq         = open(filename_in, 'w')
    text        = 'input File'
    text        = str(text)
    text =  text + '\n'
    for i in parameters:
        text =  text + i + ':' + parameters[i] + '\n'
    arq.writelines(text)
    arq.close()




    '''                                    
    --- ---------------------------------- ---
    ---                                    ---
    ---            Output File             ---
    ---                                    ---
    --- ---------------------------------- ---
    '''
    filename_out = os.path.join(folder, Job+'_MonteCarlo.out')
    arq          = open(filename_out, 'w')
    text         = 'Output File'
    text         = str(text)
    arq.writelines(text)
    arq.close()


 
    project['Jobs'][Job] = {
                'Title'     : 'Testing MonteCarlos Sim',
                'Folder'    : folder,                
                'Input'     : filename_in,
                'Output'    : filename_out,
                'LogFile'   : ''          , 
                'Type'      : 'MonteCarlo', 
                'Energy'    : str(rdm.random()*1.2345),                   
                'Start'     : '  -  ',                 
                'End'       : '  -  ' ,
                'parameters': parameters}              


class MCwindow:
    """ Class doc """
    
    def RunMCSimulationButton (self, button):
        """ Function doc """
        
        # Environment Variables
        InitialTemperature               = self.builder.get_object('Initial_Temperature_entry')             .get_text()
        Temperature_THR                  = self.builder.get_object('Temperature_THR_entry')                 .get_text()
        AttemptsThresholdWithDirector    = self.builder.get_object('AttemptsThresholdWithDirector_entry')   .get_text()
        AttemptsThresholdWithoutDirector = self.builder.get_object('AttemptsThresholdWithoutDirector_entry').get_text()
        MaxMumberOfNoImprovenment        = self.builder.get_object('MaxMumberOfNoImprovenment_entry')       .get_text()
        MinTemperatureAllowed            = self.builder.get_object('MinTemperatureAllowed_entry')           .get_text()
        TemperatureDecreaseRatio         = self.builder.get_object('TemperatureDecreaseRatio_entry')        .get_text()
        EnergyVariationThreshold         = self.builder.get_object('EnergyVariationThreshold_entry')        .get_text()
    
    
        # Directors
        TotalDirectorsMovies       = self.builder.get_object('TotalDirectorsMovies_entry')     .get_text()
        TemperatureFactorDirector  = self.builder.get_object('TemperatureFactorDirector_entry').get_text()
        MinCrank                   = self.builder.get_object('MinCrank_entry')                 .get_text()
        AddWeightPivotCrank        = self.builder.get_object('AddWeightPivotCrank_entry')      .get_text()
        MinPivotDistance           = self.builder.get_object('MinPivotDistance_entry')         .get_text()
        MaxAngle                   = self.builder.get_object('MaxAngle_entry')                 .get_text()

        #Searching Agents
        AddMovieType               = self.builder.get_object('AddMovieType_entry')           .get_text()
        TemperatureFactorSearch    = self.builder.get_object('TemperatureFactorSearch_entry').get_text()

        #print  'InitialTemperature               :',InitialTemperature               
        #print  'Temperature-THR                  :',Temperature_THR                  
        #print  'AttemptsThresholdWithDirector    :',AttemptsThresholdWithDirector    
        #print  'AttemptsThresholdWithoutDirector :',AttemptsThresholdWithoutDirector 
        #print  'MaxMumberOfNoImprovenment        :',MaxMumberOfNoImprovenment        
        #print  'MinTemperatureAllowed            :',MinTemperatureAllowed            
        #print  'TemperatureDecreaseRatio         :',TemperatureDecreaseRatio         
        #print  'EnergyVariationThreshold         :',EnergyVariationThreshold         
        #print  'TotalDirectorsMovies             :',TotalDirectorsMovies             
        #print  'TemperatureFactorDirector        :',TemperatureFactorDirector        
        #print  'MinCrank                         :',MinCrank                         
        #print  'AddWeightPivotCrank              :',AddWeightPivotCrank              
        #print  'MinPivotDistance                 :',MinPivotDistance                 
        #print  'AddMovieType                     :',AddMovieType                     
        #print  'TemperatureFactorSearch          :',TemperatureFactorSearch          
        
        parameters =   {
                        'InitialTemperature               ' : InitialTemperature              ,
                        'Temperature-THR                  ' : Temperature_THR                 ,
                        'AttemptsThresholdWithDirector    ' : AttemptsThresholdWithDirector   ,
                        'AttemptsThresholdWithoutDirector ' : AttemptsThresholdWithoutDirector,
                        'MaxMumberOfNoImprovenment        ' : MaxMumberOfNoImprovenment       ,
                        'MinTemperatureAllowed            ' : MinTemperatureAllowed           ,
                        'TemperatureDecreaseRatio         ' : TemperatureDecreaseRatio        ,
                        'EnergyVariationThreshold         ' : EnergyVariationThreshold        ,
                        'TotalDirectorsMovies             ' : TotalDirectorsMovies            ,
                        'TemperatureFactorDirector        ' : TemperatureFactorDirector       ,
                        'MinCrank                         ' : MinCrank                        ,
                        'AddWeightPivotCrank              ' : AddWeightPivotCrank             ,
                        'MinPivotDistance                 ' : MinPivotDistance                ,
                        'AddMovieType                     ' : AddMovieType                    ,
                        'TemperatureFactorSearch          ' : TemperatureFactorSearch         
                        }
        #print self.projects
        project = self.projects[self.ActivedProject]
        
        RunMCSimulation(project, parameters)
        
        Jobs      = project['Jobs']
        liststore = self.main_builder.get_object("liststore1")
        
        try:
            self.WindowControl.AddJobHistoryToTreeview(liststore, Jobs)
        except:
            pass
            
        HOME   = os.environ.get('HOME')
        FOLDER = HOME +'/.config/MASTERS/'
        json.dump(self.projects, open(FOLDER + 'ProjectHistory.dat', 'w'), indent=2)
            
    def __init__(self, Session =  None): #main_builder = None, projects = None, ActiveProject=None, WindowControl = None):
        
        self.builder = gtk.Builder()
        self.builder.add_from_file('MastersMonteCarloSimulationWindow.glade')
        self.builder.connect_signals(self)
        self.window = self.builder.get_object('window1')
        self.window.show()                                               
        self.builder.connect_signals(self)                                   
        
        self.inputfiles = {
                        'initialCoords': '/home/labio/Documents/MASTERS/test/MastersSaida.masters',
                        }
        
        if Session == None:
            pass
        else:
            self.ActivedProject = Session.ActivedProject
            self.projects       = Session.projects
            self.WindowControl  = Session.WindowControl
            self.main_builder   = Session.builder        
        gtk.main()
        

if __name__ == '__main__':
	MCwindow = MCwindow()







'''
class MCwindow:
    """ Class doc """
    
    def RunMCSimulationButton (self, button):
        """ Function doc """
        
        # Environment Variables
        InitialTemperature               = self.builder.get_object('Initial_Temperature_entry')             .get_text()
        Temperature_THR                  = self.builder.get_object('Temperature_THR_entry')                 .get_text()
        AttemptsThresholdWithDirector    = self.builder.get_object('AttemptsThresholdWithDirector_entry')   .get_text()
        AttemptsThresholdWithoutDirector = self.builder.get_object('AttemptsThresholdWithoutDirector_entry').get_text()
        MaxMumberOfNoImprovenment        = self.builder.get_object('MaxMumberOfNoImprovenment_entry')       .get_text()
        MinTemperatureAllowed            = self.builder.get_object('MinTemperatureAllowed_entry')           .get_text()
        TemperatureDecreaseRatio         = self.builder.get_object('TemperatureDecreaseRatio_entry')        .get_text()
        EnergyVariationThreshold         = self.builder.get_object('EnergyVariationThreshold_entry')        .get_text()
    
    
        # Directors
        TotalDirectorsMovies       = self.builder.get_object('TotalDirectorsMovies_entry')     .get_text()
        TemperatureFactorDirector  = self.builder.get_object('TemperatureFactorDirector_entry').get_text()
        MinCrank                   = self.builder.get_object('MinCrank_entry')                 .get_text()
        AddWeightPivotCrank        = self.builder.get_object('AddWeightPivotCrank_entry')      .get_text()
        MinPivotDistance           = self.builder.get_object('MinPivotDistance_entry')         .get_text()
        MaxAngle                   = self.builder.get_object('MaxAngle_entry')                 .get_text()

        #Searching Agents
        AddMovieType               = self.builder.get_object('AddMovieType_entry')           .get_text()
        TemperatureFactorSearch    = self.builder.get_object('TemperatureFactorSearch_entry').get_text()

        #print  'InitialTemperature               :',InitialTemperature               
        #print  'Temperature-THR                  :',Temperature_THR                  
        #print  'AttemptsThresholdWithDirector    :',AttemptsThresholdWithDirector    
        #print  'AttemptsThresholdWithoutDirector :',AttemptsThresholdWithoutDirector 
        #print  'MaxMumberOfNoImprovenment        :',MaxMumberOfNoImprovenment        
        #print  'MinTemperatureAllowed            :',MinTemperatureAllowed            
        #print  'TemperatureDecreaseRatio         :',TemperatureDecreaseRatio         
        #print  'EnergyVariationThreshold         :',EnergyVariationThreshold         
        #print  'TotalDirectorsMovies             :',TotalDirectorsMovies             
        #print  'TemperatureFactorDirector        :',TemperatureFactorDirector        
        #print  'MinCrank                         :',MinCrank                         
        #print  'AddWeightPivotCrank              :',AddWeightPivotCrank              
        #print  'MinPivotDistance                 :',MinPivotDistance                 
        #print  'AddMovieType                     :',AddMovieType                     
        #print  'TemperatureFactorSearch          :',TemperatureFactorSearch          
        
        parameters =   {
                        'InitialTemperature               ' : InitialTemperature              ,
                        'Temperature-THR                  ' : Temperature_THR                 ,
                        'AttemptsThresholdWithDirector    ' : AttemptsThresholdWithDirector   ,
                        'AttemptsThresholdWithoutDirector ' : AttemptsThresholdWithoutDirector,
                        'MaxMumberOfNoImprovenment        ' : MaxMumberOfNoImprovenment       ,
                        'MinTemperatureAllowed            ' : MinTemperatureAllowed           ,
                        'TemperatureDecreaseRatio         ' : TemperatureDecreaseRatio        ,
                        'EnergyVariationThreshold         ' : EnergyVariationThreshold        ,
                        'TotalDirectorsMovies             ' : TotalDirectorsMovies            ,
                        'TemperatureFactorDirector        ' : TemperatureFactorDirector       ,
                        'MinCrank                         ' : MinCrank                        ,
                        'AddWeightPivotCrank              ' : AddWeightPivotCrank             ,
                        'MinPivotDistance                 ' : MinPivotDistance                ,
                        'AddMovieType                     ' : AddMovieType                    ,
                        'TemperatureFactorSearch          ' : TemperatureFactorSearch         
                        }
        #print self.projects
        project = self.projects[self.ActivedProject]
        
        RunMCSimulation(project, parameters)
        
        Jobs = project['Jobs']
        
        liststore = self.main_builder.get_object("liststore1")
        
        try:
            self.WindowControl.AddJobHistoryToTreeview(liststore, Jobs)
        except:
            pass
        
        
        HOME   = os.environ.get('HOME')
        FOLDER = HOME +'/.config/MASTERS/'
        json.dump(self.projects, open(FOLDER + 'ProjectHistory.dat', 'w'), indent=2)
            
            
    def  OpenConfigFile(self, button):
        pass

    def OpenWindow (self, ConfigFile = None, ActivedProject = None):
        """ Function doc """
        if self.Visible  ==  False:
            self.builder = gtk.Builder()
            self.builder.add_from_file('MastersMonteCarloSimulationWindow.glade')
            self.builder.connect_signals(self)
            self.window = self.builder.get_object('window1')
      
            
            self.window.show()                                               
            self.builder.connect_signals(self)                                   
            self.Visible  =  True
            gtk.main()
            self.ActivedProject = ActivedProject
            #----------------------------------------------------------------
    def  on_MCwindow_destroy(self, widget):
        """ Function doc """
        self.Visible  =  False

    def __init__(self, main_builder = None, projects = None, ActiveProject=None, WindowControl = None):
        self.projects       =  projects
        self.Visible        =  False
        self.ActiveProject  =  None
        self.WindowControl  =  WindowControl
        self.main_builder   =  main_builder
        # - - - CELL - - - #
        self.minX = -10.0  #
        self.minY = -10.0  #
        self.minZ = -10.0  #
        self.maxX =  10.0  #
        self.maxY =  10.0  #
        self.maxZ =  10.0  #
        # - - - - - - - - -#
'''

