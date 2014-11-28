#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  DialogNewProject.py
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
import os
import gtk
import time
from pprint import pprint
import json 


AminoAcidDic = {'A':['Ala','HID','A'],
                'R':['Arg','POL','B'],
                'N':['Asn','POL','B'],
                'D':['Asp','POL','B'],
                'C':['Cys','HID','A'],
                'E':['Glu','POL','B'],
                'Q':['Gln','POL','B'],
                'G':['Gly','HID','A'],
                'H':['His','POL','B'],
                'I':['Ile','HID','A'],
                'L':['Leu','HID','A'],
                'K':['Lys','POL','B'],
                'M':['Met','HID','A'],
                'F':['Phe','POL','B'],
                'P':['Pro','HID','A'],
                'S':['Ser','POL','B'],
                'T':['Thr','POL','B'],
                'W':['Trp','POL','B'],
                'Y':['Tyr','POL','B'],
                'V':['Val','HID','A']}


def NewProject (project):
    """ Function doc """
    LogWriter()
     
    
    pass


class NewProjectDialog():
    
    def CreateNewProject (self, button):
        """ Function doc """
        user          =  self.builder.get_object('user_entry').get_text()
        projectID     =  self.builder.get_object('new_project_entry').get_text()
        folder        =  self.builder.get_object('filechooserbutton1').get_filename()
        _buffer       =  self.builder.get_object('textview1').get_buffer()
        _buffer_infor =  self.builder.get_object('textview2').get_buffer()

        sequence  = _buffer.get_text(*_buffer.get_bounds(), include_hidden_chars=False)
        add_info  = _buffer_infor.get_text(*_buffer_infor.get_bounds(), include_hidden_chars=False)
        
        if folder == None:
            print 'please - select a folder' 
        
        sequence2 = sequence.replace('\n', '')
        sequence2 = sequence2.replace(' ', '')
        sequence2 = sequence2.upper()
        #print user, projectID, folder, sequence2
        
        
        ABsequence = ''
        for i in sequence2:
            AB =  AminoAcidDic[i][2]
            ABsequence = ABsequence + AB
        
        
        index = len(self.projects) + 1
        
        start      = time.asctime(time.localtime(time.time()))
        
        self.projects[index] = {
                            'User'        : user     ,
                            'ProjectName' : projectID,
                            'Info'        : add_info ,
                            'Folder'      : folder   ,
                            'Sequence'    : sequence2,
                            'ABsequence'  : ABsequence,                
                            'ABmodel'     : AminoAcidDic,        
                            'Generated'   : start,                
                            'Modified'    : start,                
                            'Jobs'        : {                  
                                             1:{
                                                 'Title' : 'teste com monte carlo',
                                                'Folder' : 'None',          #
                                                  'Type' : 'MonteCarlo',          #
                                                'Energy' : '1233.554',          #  exemplo de como deve ser o dic jobs
                                                 'Start' : 'ontem',          #
                                                   'End' : 'hoje' }         #
                                            }
                            }
        

        
        pprint (self.projects)
        self.WindowControl.AddProjectHistoryToTreeview(liststore = self.main_builder.get_object('liststore2'))
        
        
        HOME   = os.environ.get('HOME')
        FOLDER = HOME +'/.config/MASTERS/'
        json.dump(self.projects, open(FOLDER + 'ProjectHistory.dat', 'w'), indent=2)
        
        # agora tem que criar a pasta do projeto com as info relevantes
        
            
    def __init__(self, main_builder=None, projects = None, WindowControl = None):
        
        """ Class initialiser """
        
        
        self.projects = projects
        if self.projects == None:
            self.projects = {}
        self.builder = gtk.Builder()
        self.main_builder = main_builder

        self.builder.add_from_file(
            os.path.join('MastersNewProject.glade'))
        self.builder.connect_signals(self)
        self.dialog = self.builder.get_object('dialog1')
        

        '''
		--------------------------------------------------
		-                                                -
		-	              WindowControl                  -
		-                                                -
		--------------------------------------------------
		'''
        
        self.WindowControl = WindowControl

        #----------------- Setup ComboBoxes -------------------------#
        #combobox = '02_window_combobox_minimization_method'          #
        #combolist = ["Conjugate Gradient", "Steepest Descent", "LBFGS"]
        #self.window_control.SETUP_COMBOBOXES(combobox, combolist, 0)
        #------------------------------------------------------------#


def main():
    dialog = NewProjectDialog()
    dialog.dialog.run()
    dialog.dialog.hide()
if __name__ == '__main__':
    main()



def main():
	
	return 0

if __name__ == '__main__':
	main()

