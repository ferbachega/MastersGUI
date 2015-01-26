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
import os
import json


# Imports
from OpenGL.GL import *
from OpenGL.GLU import *
from pprint import pprint

#GUI
#from MastersNewProjectDialog import *
from FileChooserWindow import *
from pymol.cgo import *

from py4j.java_gateway import JavaGateway

def GetFileType(filename):
    file_type = filename.split('.')
    return file_type[-1]



class MonteCarloSimulationWindow:
    """ Class doc """
    
    def __init__ (self,  Session = None, ClickedJobID = None, ReRunJOB = None ):
        """ Class initialiser """
        self.builder = gtk.Builder()
        self.builder.add_from_file('MastersMonteCarloSimulationWindow.glade')
        self.builder.connect_signals(self)
        self.window = self.builder.get_object('window1')
        self.window.show()                                               
        self.builder.connect_signals(self)
        
        self.ClickedJobID = ClickedJobID
        
        
        
        #---------------------------------------------#
        #              INPUT  PARAMETERS              #
        #---------------------------------------------#
        self.InputFiles       = None               
        self.InputParamaters  = None
        self.OutputParameters = None
        self.folder           = ''
        
        #---------------------------------------------#
        #                 INPUT FILES                 #
        #---------------------------------------------#

        if ReRunJOB == None:
            self.InputFiles = {
                              'input_coords': '/home/labio/MastersWorkSpace/labio_project_Jan_20_2015/12_initialCoordinates.pdb',
                              }
        else:
            self.InputFiles = {
                              'input_coords': '/home/labio/MastersWorkSpace/labio_project_Jan_20_2015/12_initialCoordinates.pdb',
                              }

        
        self.Session  = Session  # importing Master session
        
        try:
            self.project  = Session.projects[Session.ActivedProject]

            #pprint(self.Session.projects[self.ActivedProject])
            
            
            self.AddFilesToTreeview()
            self.ImportCellValorsFromProject()
        except:
            pass


        gtk.main()

    def ImportCellValorsFromProject (self):
        """ Function doc """
        try:
            self.builder.get_object('cell_maxX_entry').set_text(str(self.project['Cell']["maxX"]))
            self.builder.get_object('cell_maxY_entry').set_text(str(self.project['Cell']["maxY"]))
            self.builder.get_object('cell_maxZ_entry').set_text(str(self.project['Cell']["maxZ"]))
            self.builder.get_object('cell_minX_entry').set_text(str(self.project['Cell']["minX"]))
            self.builder.get_object('cell_minY_entry').set_text(str(self.project['Cell']["minY"]))
            self.builder.get_object('cell_minZ_entry').set_text(str(self.project['Cell']["minZ"]))
        except:
            print 'Cell parameters not available'

    def AddFilesToTreeview (self):
        model = self.builder.get_object('liststore1')

        for i  in self.InputFiles:
            print i, self.InputFiles[i]
            data   = [i, " - ", self.InputFiles[i]] #string string string
            model.append(data)

    def STATUSBAR_SET_TEXT(self, text):
        """ Function doc """
        self.builder.get_object('statusbar1').push(0, text)
        #--------------------------------------------#
        #               MCWINDOW METHODS             #
        #--------------------------------------------#
    ''' Only buttons and widgets - glade widgets signals'''

    def on_treeview_button_release_event  (self, tree, event):
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

    def on_button_RunMCSimulation_clicked (self, button):
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



        InputFiles       =  {
                             'input_coords'      : self.InputFiles['input_coords'],
                             'spatial_restraints': None,
                             'SS_restraints'     : None
                            }

        self.InputParamaters = {
                                 'title'        : title,
                                 'outputname'   : None ,

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
                                 }

        self.OutputParameters = {
                                'PyMOL_update'       : None,
                                'PDB_real'           : None,
                                'Graph_log'          : True,
                                'Splitted_PDB_files' : False
                                }

        pprint(self.InputFiles)
        pprint(self.InputParamaters)
        pprint(self.OutputParameters)


        self.RunMastersMCSimulation()



        #--------------------------------------------#
        #             MONTECARLO METHODS             #
        #--------------------------------------------#

    def CreateNewFolder (self):
        """ Function doc """
        # - - - Ceating a new folder - - - #
        Job       = str(len(self.project['Jobs'])) # the new job ID
        newfolder = os.path.join(self.project['Folder'],Job +'_MonteCarlo')  # eg. /home/LABIO/Workspace/myself.project/1_MonteCarlo
        if not os.path.exists (newfolder):
            os.mkdir (newfolder)
        self.folder = newfolder

    def GenerateMastersMCInputFiles (self, InputFileName = None, OutputFileName = None):
        """ Function doc """
        parameters   = self.InputParamaters['MCparameters']
        input_coords = self.InputFiles['input_coords']


        Job          = str(len(self.project['Jobs'])) # the new job ID

        if OutputFileName == None:
            self.InputParamaters['outputname'] = Job +'_MonteCarlo'
        else:
            self.InputParamaters['outputname'] = OutputFileName


        #project   = self.Session.projects[self.Session.ActivedProject]

        '''
        --- ---------------------------------- ---
        ---            Input File              ---
        --- ---------------------------------- ---
        '''

        arq          = open(InputFileName, 'w')

        #input_coords = self.project['Jobs']['0']['Output']   - Michele's version

        #----------------------------------INPUT-PARAMETERS---------------------------------------#
        text = '#  - - MASTERS input file simulation - - \n'                                      #
        text = str(text)                                                                          #
        text =  text + '\n'                                                                       #
        text =  text + '#JobTitle    = ' + self.InputParamaters['title']             + '\n'       #
        text =  text + '#ProjectName = ' + self.project['ProjectName']               + '\n'       #
        text =  text + '#User        = ' + self.project['User']                      + '\n'       #
        text =  text + '#Generated   = ' + time.asctime(time.localtime(time.time())) + '\n'       #
                                                                                                  #
        text =  text + '\n\n'                                                                     #
                                                                                                  #
        text =  text + '# - - JOB-PATH - - \n'                                                    #
        text =  text + 'job_path     = ' + '"' + self.folder                        + '/"' + '\n' #
        text =  text + 'input_coords = ' + '"' + input_coords                       + '/"\n'      #
        text =  text + 'title        = ' + '"' + self.InputParamaters['outputname'] + '"'  + '\n' #
        text =  text + '\n\n'                                                                     #
        #-----------------------------------------------------------------------------------------#



        #-----------------------------CELL-PARAMETERS------------------------------------#
        text =  text + '# - - CELL-PARAMETERS - - \n'                                    #
        text =  text + 'max_pxcor = ' + str(self.InputParamaters['Cell']["maxX"]) + '\n' #
        text =  text + 'max_pycor = ' + str(self.InputParamaters['Cell']["maxY"]) + '\n' #
        text =  text + 'max_pzcor = ' + str(self.InputParamaters['Cell']["maxZ"]) + '\n' #
        text =  text + 'min_pxcor = ' + str(self.InputParamaters['Cell']["minX"]) + '\n' #
        text =  text + 'min_pycor = ' + str(self.InputParamaters['Cell']["minY"]) + '\n' #
        text =  text + 'min_pzcor = ' + str(self.InputParamaters['Cell']["minZ"]) + '\n' #
        text =  text + '\n\n'                                                            #
        #--------------------------------------------------------------------------------#



        #-------------------------------MCPARAMETERS------------------------------#
        text =  text + '# - - PARAMETERS - - \n'                                  #
        for i in parameters:                                                      #
            text =  text + i + ' = ' + parameters[i] + '\n'                       #
        #-------------------------------------------------------------------------#

        arq.writelines(text)
        arq.close()
        return InputFileName

    def RunMastersMCSimulation (self):
        """ Function doc """
        self.STATUSBAR_SET_TEXT('running' )
        #-------------------------INPUT FILE-------------------------------#
        Job     = str(len(self.project['Jobs']))                           #
        title   = Job +'_MonteCarlo'                                       #
                                                                           #
                                                                           #
        self.CreateNewFolder()                                             #
        InputFileName = os.path.join(self.folder, Job +'_MonteCarlo.in')   #
        self.GenerateMastersMCInputFiles(InputFileName)                    #
        #------------------------------------------------------------------#


        # - - - - - RUN MC SIMULATION - - - - -#
        gateway = JavaGateway()
        masters = gateway.entry_point.getMasters()
        masters.loadParameters(InputFileName)



        print 'Starting simulation'
        step = 1

        self.Session.projects[self.Session.ActivedProject]['Jobs'][Job] = {
                                     'Title'      : self.InputParamaters['title'],
                                     'Folder'     : self.folder                  ,
                                     'Input'      : InputFileName                ,
                                     'Type'       : 'MonteCarlo'                 ,
                                     'Status'     : 'running'                    ,
                                     'Energy'     : '  -  '                      ,
                                     'Start'      : '  -  '                      ,
                                     'End'        : 'running'                    ,
                                     'Energy'     : '  -  '                      ,
                                     'parameters' : self.InputParamaters['MCparameters']
                                     }


        projectID  = self.Session.ActivedProject
        Jobs       = self.Session.projects[projectID]['Jobs']
        liststore  = self.Session.builder.get_object("liststore1")
        pprint(self.Session.projects[self.Session.ActivedProject]['Jobs'][Job])



        self.Session.WindowControl.AddJobHistoryToTreeview(liststore, Jobs)


        while masters.is_running():
            masters.step()


            # Update UI
            while gtk.events_pending():
                gtk.main_iteration(False)

            # ---------- adicionar aqui  tudo que  sera gerado de arquivos --------- #
            try:
                os.rename(
                    os.path.join(self.folder,title+'-current.pdb'),
                    os.path.join(self.folder,title+'_step_' + step)
                )
            except:
                pass
            # ---------------------------------------------------------------------- #

            step += 1
        self.Session.projects[self.Session.ActivedProject]['Jobs'][Job]['End'] = 'finished'
        self.STATUSBAR_SET_TEXT('finished' )
        #project['Jobs'][Job] = {
        #            'Title'      : InputParamaters['title'],
        #            'Folder'     : newfolder               ,
        #            'Input'      : inputfile               ,
        #            'InputCoord' : None                    ,
        #            'Output'     : filename_out            ,
        #            'OutputCoord': None                    ,
        #            'LogFile'    : ''                      ,
        #            'Type'       : 'MonteCarlo'            ,
        #            'Energy'     : str(rdm.random()*1.2345),
        #            'Start'      : '  -  '                 ,
        #            'End'        : '  -  '                 ,
        #            'parameters' : parameters}
        #Jobs      = self.project['Jobs']
        #liststore = self.main_builder.get_object("liststore1")
        #try:
        #    self.WindowControl.AddJobHistoryToTreeview(liststore, Jobs)
        #except:
        #    pass
        #
        HOME   = os.environ.get('HOME')
        FOLDER = HOME +'/.config/MASTERS/'
        json.dump(self.Session.projects, open(FOLDER + 'ProjectHistory.dat', 'w'), indent=2)






def main():
	window = MonteCarloSimulationWindow()

	return 0

if __name__ == '__main__':
	main()












