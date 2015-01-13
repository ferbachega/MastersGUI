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
    #path   =  project['Folder']
    path   = os.path.join(project['Folder'],Job +'_MonteCarlo')
    if not os.path.exists (path): 
        os.mkdir (path)
    
    
    '''                                    
    --- ---------------------------------- ---
    ---                                    ---
    ---            Input File              ---
    ---                                    ---
    --- ---------------------------------- ---
    '''
    filename_in = os.path.join(path, Job+'_MonteCarlo.in')
    arq         = open(filename_in, 'w')
    
    #----------------title-----------------#
    text        = '#  - - MASTERS input file simulation - - \n'
    text        = str(text)
    text =  text + '\n'
    
    text =  text + '#ProjectName = ' + project['ProjectName'] + '\n'
    text =  text + '#User        = ' + project['User'] + '\n'
    text =  text + '#Generated   = ' + time.asctime(time.localtime(time.time())) + '\n'
    text =  text + '\n\n'

    text =  text + '# - - JOB-PATH - - \n'
    text =  text + 'job_path     = ' + '"' + path + '/"' + '\n'
    text =  text + '\n\n'
    
    #--------------------------------------#
    
    
    #-------------------CELL-PARAMETERS------------------#
    text =  text + '# - - CELL-PARAMETERS - - \n'
    text =  text + 'max-pxcor = ' + str(project['Cell']["maxX"]) + '\n'
    text =  text + 'max-pycor = ' + str(project['Cell']["maxY"]) + '\n'
    text =  text + 'max-pzcor = ' + str(project['Cell']["maxZ"]) + '\n'
    text =  text + 'min-pxcor = ' + str(project['Cell']["minX"]) + '\n'
    text =  text + 'min-pycor = ' + str(project['Cell']["minY"]) + '\n'
    text =  text + 'min-pzcor = ' + str(project['Cell']["minZ"]) + '\n'
    text =  text + '\n\n'

    #----------------------------------------------------#
    
    
    #-------------------PARAMETERS-------------------#
    text =  text + '# - - PARAMETERS - - \n'
    for i in parameters:
        text =  text + i + ' = ' + parameters[i] + '\n'
    #------------------------------------------------#
    
    
    
        
    arq.writelines(text)
    arq.close()



    
    '''                                    
    --- ---------------------------------- ---
    ---                                    ---
    ---            Output File             ---
    ---                                    ---
    --- ---------------------------------- ---
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
    '''


class MCwindow:
    """ Class doc """

    def AddFileToTreeview (self, Filein, Format,  DataType):
        model = self.builder.get_object('liststore1')
        data  = [Filein, Format, DataType] #string string string
        model.append(data)

    def on_treeview_button_release_event(self, tree, event):
        if event.button == 3:
            selection     = tree.get_selection()
            model         = tree.get_model()
            (model, iter) = selection.get_selected()
            if iter != None:
                #self.selectedID  = str(model.get_value(iter, 1))  # @+
                self.selectedObj    = str(model.get_value(iter, 1))
                self.selectedFormat = str(model.get_value(iter, 2))
                
                self.builder.get_object('TreeViewObjLabel').set_label('- ' +self.selectedObj+' -' )
                
                widget = self.builder.get_object('treeview_menu')
                widget.popup(None, None, None, event.button, event.time)
            
        if event.button == 1:
            print "Mostrar menu de contexto botao1"


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
        #AddMovieType               = self.builder.get_object('AddMovieType_entry')           .get_text()
        TemperatureFactorSearch    = self.builder.get_object('TemperatureFactorSearch_entry').get_text()

        #print  'InitialTemperature               :',InitialTemperature                 #time 
        #print  'Temperature-THR                  :',Temperature_THR                    #user
        #print  'AttemptsThresholdWithDirector    :',AttemptsThresholdWithDirector      
        #print  'AttemptsThresholdWithoutDirector :',AttemptsThresholdWithoutDirector   #title = 'jobname'
        #print  'MaxMumberOfNoImprovenment        :',MaxMumberOfNoImprovenment          #cell -25 25 -20 20 -20 20
        #print  'MinTemperatureAllowed            :',MinTemperatureAllowed              #min-pxcor = -25.00
        #print  'TemperatureDecreaseRatio         :',TemperatureDecreaseRatio           #max-pxcor =  25.00
        #print  'EnergyVariationThreshold         :',EnergyVariationThreshold           #min-pycor = -20.00
        #print  'TotalDirectorsMovies             :',TotalDirectorsMovies               #max-pycor =  20.00
        #print  'TemperatureFactorDirector        :',TemperatureFactorDirector          #min-pxcor = -20.00
        #print  'MinCrank                         :',MinCrank                           #max-pxcor =  20.00
        #print  'AddWeightPivotCrank              :',AddWeightPivotCrank                
        #print  'MinPivotDistance                 :',MinPivotDistance                   director-sleep-time = 5
        #print  'AddMovieType                     :',AddMovieType                       temp_factor_dir = 0.5
        #print  'TemperatureFactorSearch          :',TemperatureFactorSearch            temp_factor_search = 0.5
        #                                                                               nr-of-directors = 1
        #                                                                               limit_prob_dir = 1
        #                                                                               limit_prob_search = 1
        #                                                                               attempted_threshold_with_dir = 500
        #                                                                               job_path="/tmp/"
        '''
        ENVIR-----
        temperature 10
        temp_thr 0.03
        attempted_threshold_with_dir 500
        attempted_threshold_without_dir 40
        max_number_of_no_improvement_in_energy 20
        min_temperature_allowed 0.0099
        temp_decrease_ratio 0.98
        energy_variation_threshold 1.0E-4

        ----
        DIRECTORS-----  ESSE ADD WEIGHT SAI, ENTRA MAX CRANK
        total_dir_moves 20
        temp_factor_dir 0.5
        min_crank 2 AA
        max_crank 3 AA
        min_pivot_dist 4 AA
        max_angle 180 degrees
        ---
        SEARCHING ----
        temp_factor_search 0.5
        TIRAR add move type
        '''  
        
        
        
        
        
        
        parameters =   {
                        'temperature'                            : InitialTemperature               ,
                        'temp_thr'                               : Temperature_THR                  ,
                        'attempted_threshold_with_dir'           : AttemptsThresholdWithDirector    ,
                        'attempted_threshold_without_dir'        : AttemptsThresholdWithoutDirector ,
                        'max_number_of_no_improvement_in_energy' : MaxMumberOfNoImprovenment        ,
                        'min_temperature_allowed'                : MinTemperatureAllowed            ,
                        'temp_decrease_ratio'                    : TemperatureDecreaseRatio         ,
                        'energy_variation_threshold'             : EnergyVariationThreshold         ,
                        'total_dir_moves'                        : TotalDirectorsMovies             ,
                        'temp_factor_dir'                        : TemperatureFactorDirector        ,
                        'min_crank'                              : MinCrank                         ,
                        'max_crank'                              : AddWeightPivotCrank              ,
                        'min_pivot_dist'                         : MinPivotDistance                 ,
                        'max_angle'                              : MaxAngle                         ,
                        'temp_factor_search'                     : TemperatureFactorSearch         
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
        
        project = self.projects[self.ActivedProject]
        Filein  = project['Jobs']['0']['Output']
        Filein2 = os.path.split(Filein) 
        Filein2 = Filein2[-1]
        Format  = 'pdb'
        DataType= 'inital coordinates'
        
        self.AddFileToTreeview(Filein2, Format,  DataType)
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

