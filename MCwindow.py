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

from py4j.java_gateway import JavaGateway


'''
if not sys.platform.startswith('win'):
    HOME = os.environ.get('HOME')
else:
    HOME = os.environ.get('PYMOL_PATH')
'''


class MonteCarloSimulation:
    """ Class doc """
    
    def __init__ (self, project, main_builder):
        """ Class initialiser """
        self.project      = project
        self.folder       = None
        self.Job          = None # index
         
        self.main_builder = main_builder
    
    def AddNewFolder (self, Job):
        """ Function doc """
        # - - - Ceating a new folder - - - #
        newfolder = os.path.join(self.project['Folder'],Job +'_MonteCarlo')  # eg. /home/LABIO/Workspace/myself.project/1_MonteCarlo
        if not os.path.exists (newfolder): 
            os.mkdir (newfolder) 
        return newfolder
           
    def GenerateMastersMCInputFiles (self             , 
                                     InputParamaters  , 
                                     folder           , 
                                     inputfile = None ,
                                     title = 'test2'):
        """ Function doc """
        

        parameters = InputParamaters['MCparameters']
        
        
        '''                                    
        --- ---------------------------------- ---
        ---                                    ---
        ---            Input File              ---
        ---                                    ---
        --- ---------------------------------- ---
        '''
         
        arq          = open(inputfile, 'w')
        
        #input_coords = self.project['Jobs']['0']['Output']   - Michele's version
            
            

        #----------------------------------INPUT-PARAMETERS-------------------------------------#
        text        = '#  - - MASTERS input file simulation - - \n'                             #
        text        = str(text)                                                                 #
        text =  text + '\n'                                                                     #
        text =  text + '#JobTitle    = ' + InputParamaters['title'] + '\n'                      #
        text =  text + '#ProjectName = ' + self.project['ProjectName'] + '\n'                   #
        text =  text + '#User        = ' + self.project['User'] + '\n'                          #
        text =  text + '#Generated   = ' + time.asctime(time.localtime(time.time())) + '\n'     #
        text =  text + '\n\n'                                                                   #
        text =  text + '# - - JOB-PATH - - \n'                                                  #
        text =  text + 'job_path     = ' + '"' + folder + '/"' + '\n'                           #
        text =  text + 'input_coords = ' + '"' + InputParamaters['input_coords'] + '/"\n'         #
        text =  text + 'title        = ' + '"' + title + '"' + '\n'                             #
        #text =  text + 'input_coords = ' + '"' + input_coords + '/"' + '\n'- Michele's version #
        text =  text + '\n\n'                                                                   #
        #---------------------------------------------------------------------------------------#

        
        #-----------------------------CELL-PARAMETERS-------------------------------#
        text =  text + '# - - CELL-PARAMETERS - - \n'                               #
        text =  text + 'max_pxcor = ' + str(InputParamaters['Cell']["maxX"]) + '\n' #
        text =  text + 'max_pycor = ' + str(InputParamaters['Cell']["maxY"]) + '\n' #
        text =  text + 'max_pzcor = ' + str(InputParamaters['Cell']["maxZ"]) + '\n' #
        text =  text + 'min_pxcor = ' + str(InputParamaters['Cell']["minX"]) + '\n' #
        text =  text + 'min_pycor = ' + str(InputParamaters['Cell']["minY"]) + '\n' #
        text =  text + 'min_pzcor = ' + str(InputParamaters['Cell']["minZ"]) + '\n' #
        text =  text + '\n\n'                                                       #
        #---------------------------------------------------------------------------#
        
        
        #-------------------------------MCPARAMETERS------------------------------#
        text =  text + '# - - PARAMETERS - - \n'                                  #
        for i in parameters:                                                      #
            if i == 'Title':                                                      #
                pass                                                              #
            else:                                                                 #
                text =  text + i + ' = ' + parameters[i] + '\n'                   #
        #-------------------------------------------------------------------------#
        arq.writelines(text)
        arq.close()
        
        return inputfile

    
    def RunMastersMCSimulation (self, InputParamaters):
        """ Function doc """
        # - - - - INPUT FILE - - - - # 
        Job       = str(len(self.project['Jobs']))
        title     = Job +'_MonteCarlo'
        newfolder = self.AddNewFolder(Job)
        inputfile = os.path.join(newfolder , Job +'_MonteCarlo.in')
        self.GenerateMastersMCInputFiles(InputParamaters, newfolder , inputfile, title)
        
        
        # - - - - - RUN MC SIMULATION - - - - -#
        gateway = JavaGateway()
        masters = gateway.entry_point.getMasters()
        masters.loadParameters(inputfile)
        
        print 'Starting simulation'
        step = 0
        while masters.is_running():
            masters.step()
            try:
               os.rename( os.path.join(newfolder,title+'-current.pdb'), os.path.join(newfolder,title+'_step_'+str(step)))
                
            except:
                pass
            step += 1
            

  
        
        filename_out = Job+'_MonteCarlo.pdb'
        project['Jobs'][Job] = {
                    'Title'      : InputParamaters['title'],
                    'Folder'     : newfolder               ,                
                    'Input'      : inputfile               ,
                    'InputCoord' : None                    ,
                    'Output'     : filename_out            ,
                    'OutputCoord': None                    ,
                    'LogFile'    : ''                      , 
                    'Type'       : 'MonteCarlo'            , 
                    'Energy'     : str(rdm.random()*1.2345),                   
                    'Start'      : '  -  '                 ,                 
                    'End'        : '  -  '                 ,
                    'parameters' : parameters}              
        Jobs      = self.project['Jobs']
        liststore = self.main_builder.get_object("liststore1")
        try:
            self.WindowControl.AddJobHistoryToTreeview(liststore, Jobs)
        except:
            pass
            
        HOME   = os.environ.get('HOME')
        FOLDER = HOME +'/.config/MASTERS/'
        json.dump(self.projects, open(FOLDER + 'ProjectHistory.dat', 'w'), indent=2)
        
        
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


    def ImportParametersFromPDB (self):
        """ Function doc """
        pass
    

    def RunMCSimulationButton (self, button):
        """ Function doc """
        
        # Environment Variables
        title                            = self.builder.get_object('job_title_entry')                       .get_text()
        InitialTemperature               = self.builder.get_object('Initial_Temperature_entry')             .get_text()
        Temperature_THR                  = self.builder.get_object('Temperature_THR_entry')                 .get_text()
        AttemptsThresholdWithDirector    = self.builder.get_object('AttemptsThresholdWithDirector_entry')   .get_text()
        AttemptsThresholdWithoutDirector = self.builder.get_object('AttemptsThresholdWithoutDirector_entry').get_text()
        MaxMumberOfNoImprovenment        = self.builder.get_object('MaxMumberOfNoImprovenment_entry')       .get_text()
        MinTemperatureAllowed            = self.builder.get_object('MinTemperatureAllowed_entry')           .get_text()
        TemperatureDecreaseRatio         = self.builder.get_object('TemperatureDecreaseRatio_entry')        .get_text()
        EnergyVariationThreshold         = self.builder.get_object('EnergyVariationThreshold_entry')        .get_text()
    
        # Directors
        TotalDirectorsMovies             = self.builder.get_object('TotalDirectorsMovies_entry')     .get_text()
        TemperatureFactorDirector        = self.builder.get_object('TemperatureFactorDirector_entry').get_text()
        MinCrank                         = self.builder.get_object('MinCrank_entry')                 .get_text()
        AddWeightPivotCrank              = self.builder.get_object('AddWeightPivotCrank_entry')      .get_text()
        MinPivotDistance                 = self.builder.get_object('MinPivotDistance_entry')         .get_text()
        MaxAngle                         = self.builder.get_object('MaxAngle_entry')                 .get_text()

        #Searching Agents
        TemperatureFactorSearch          = self.builder.get_object('TemperatureFactorSearch_entry').get_text()
        
        
        
        InputParamaters =  {
                            'title'        : title,
                            'input_coords' : self.inputfiles['input_coords'],
                            'Cell'         : {
                                              "maxX": self.builder.get_object('cell_maxX_entry').get_text(),
                                              "maxY": self.builder.get_object('cell_maxY_entry').get_text(),
                                              "maxZ": self.builder.get_object('cell_maxZ_entry').get_text(),
                                              "minX": self.builder.get_object('cell_minX_entry').get_text(),
                                              "minY": self.builder.get_object('cell_minY_entry').get_text(),
                                              "minZ": self.builder.get_object('cell_minZ_entry').get_text()
                                              },
                                       
                            'MCparameters' :{
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
                                              },
                            'OutputParamaters': {}
                            }
                            


        
        
        
        MCsim = MonteCarloSimulation(self.project, self.main_builder)
        MCsim.RunMastersMCSimulation(InputParamaters)
        

        




    def PutCellValors (self):
        """ Function doc """
        project = self.projects[self.ActivedProject]
        self.builder.get_object('cell_maxX_entry').set_text(str(project['Cell']["maxX"]))
        self.builder.get_object('cell_maxY_entry').set_text(str(project['Cell']["maxY"]))
        self.builder.get_object('cell_maxZ_entry').set_text(str(project['Cell']["maxZ"]))
        self.builder.get_object('cell_minX_entry').set_text(str(project['Cell']["minX"]))
        self.builder.get_object('cell_minY_entry').set_text(str(project['Cell']["minY"]))
        self.builder.get_object('cell_minZ_entry').set_text(str(project['Cell']["minZ"]))
    
    def __init__(self, Session =  None, JobID = None):
        self.builder = gtk.Builder()
        self.builder.add_from_file('MastersMonteCarloSimulationWindow.glade')
        self.builder.connect_signals(self)
        self.window = self.builder.get_object('window1')
        self.window.show()                                               
        self.builder.connect_signals(self)                                   
        
        self.JobID = JobID
        
        self.inputfiles = {
                          'input_coords': '/home/labio/Documents/MASTERS/test/MastersSaida.masters',
                          }
        
        if Session == None:
            pass
        else:
            self.ActivedProject = Session.ActivedProject
            self.projects       = Session.projects
            self.WindowControl  = Session.WindowControl
            self.main_builder   = Session.builder        


        self.project = self.projects[self.ActivedProject]
        
        if self.JobID != None:
            pprint(self.project)
        
        
        
        
        
        Filein  = self.project['Jobs']['0']['Output']
        
        print Filein
        Filein2 = os.path.split(Filein) 
        Filein2 = Filein2[-1]
        
        Format  = 'pdb'
        DataType= 'inital coordinates'
        
        self.AddFileToTreeview(Filein2, Format,  DataType)
        
        self.PutCellValors()
        gtk.main()
        

if __name__ == '__main__':
	MCwindow = MCwindow()





