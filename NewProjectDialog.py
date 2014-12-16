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




def from20letterToAB (sequence, AminoAcidDic ):
    """ Function doc """
    ABsequence = ''
    for i in sequence:
        AB =  AminoAcidDic[i][2]
        ABsequence = ABsequence + AB
    
    return ABsequence

    
def GenerateInitialPDBCoordinates(text, sequence):
    """ Function doc 
		
        
        
        text  = []					     		# variable where the PDB file will be rewritten	
												#
												#
												#                  HETATM 1884  O   HOH A 372      21.952   9.654  -3.812  1.00 50.58           O
		for line in arq:						#	exemplo, line: ATOM  85830  CLA CLA I 154    -106.883-110.916-110.774  1.00  0.00      ION CL
			line2 = line.split()				#   	                             		'    '									'          line[76:78]
			line1 = line[0:6]					#												  li[30:38]
			#if line2[0] == "CRYST1":			#														  li[38:46]									
			#	print line2[0:-1]				#																  li[46:54]
			#	print line
			if line1 == "ATOM  ":				# 	line1  is the variable that presents the string "ATOM  " or "HETATM"
				index   = line[6:11]			#	indice
				A_name  = line[11:16]			#	atom name     ex" CA "
				resn    = line[16:20] 			#	residue name   ex" LYS"
				chain   = line[20:22]			#   chain    ex " A"
				resi    = line[22:26]			#   residue number
				gap     = line[26:30]			#	gap between residue number and coordinates
				x       = line[30:38]			#	coordinate X
				y       = line[38:46]			#	coordinate Y
				z       = line[46:54]			#	coordinate Z
												#
				b       = line[54:60]			#	B-factor
				oc      = line[60:66]			#	Occupancy
				gap2    = line[66:76]			#	gap between Occupancy and atomic type'    '
				atom    = line[76:78] 			# 	atomic type    
   
    """
           
           
           
           
           #ATOM      0  CA  LEU     1     -12.955  -7.015  -10.861  1.00  1.00           B
    text = text + '\n'
    size = float(len(sequence))
    initial_X_coord = -1*(size/2)
    
    _ATOMLINEFORMAT1    = "%-6s%5i %-4s%1s%3s %1s%4s%1s   %8.3f%8.3f%8.3f%6.2f%6.2f      %-4s%2s%2s\n"
    

    n = 0
    recordname = 'ATOM'
    for i in sequence:
        #text = text + _ATOMLINEFORMAT1 % ( recordname, n, " CA", " ", AminoAcidDic[i][0].upper(), ' ', str(n), '',
        #                                                           initial_X_coord + n , 0, 0, 0.0, 0.0, '', 'C', " " )
        text = text + _ATOMLINEFORMAT1 % ( recordname, n, " CA", " ", AminoAcidDic[i][0].upper(), ' ', str(n + 1), '',
                                                               initial_X_coord + n , 0, 0, 0.0, 0.0, '', 'C', " " )
        n = n +1
    return text


def AddHeaderToText (text, project):
    """ Function doc """
    user           = project['User'       ]
    projectID      = project['ProjectName']
    add_info       = project['Info'       ]
    folder         = project['Folder'     ]
    sequence       = project['Sequence'   ]
    ABsequence     = project['ABsequence' ]  
    AminoAcidDic   = project['ABmodel'    ]
    start          = project['Generated'  ]

    text = text +   'REMARK      - - MASTERS PROJECT FILE - - '
    text = text + '\nREMARK'
    text = text + "\nREMARK  GENERATED:    " + start  
    text = text + '\nREMARK  PROJECT_NAME: ' + projectID
    text = text + '\nREMARK  USER:         ' + user
    text = text + '\nREMARK'
    return text

def AddABModelToText (text, ABModel):
    '''ABmodel to MASTERS PROJECT FILE'''
    #--------------------------------------------------------------------------#
    line = ''                                                                  #
    text = text + '\nREMARK'                                                   #
    text = text + '\nREMARK     - - AB model - - '                             #
    n = 1                                                                      #
                                                                               #
    for i in ABModel:                                                          #
        line =  line +  '\nREMARK  ABMODEL  ' + i + ':' + str(ABModel[i])      #
    text = text + line                                                         #
    return text
    #--------------------------------------------------------------------------#

def AddABSequenceToText(text, ABsequence):
    #--------------------------------------------------------------------------#
    text = text + '\nREMARK'                                                   #
    text = text + '\nREMARK     - - protein ABsequence - - '                   #
    line = '\nREMARK  ABSEQUEN:  '                                             #
    n = 1                                                                      #
    for i in ABsequence:                                                       #
        if n >= 56:                                                            #
            n = 1                                                              #
            line =  line +  '\nREMARK  ABSEQUEN:  ' + i                        #
        else:                                                                  #
            line =  line + i                                                   #
        n = n+1                                                                #
    text = text + line                                                         #
    text = text + '\nREMARK'                                                   #
    return text                                                                #
    #--------------------------------------------------------------------------# 

def AddSequenceToText(text, sequence):
    #--------------------------------------------------------------------------#
    n = 1                                                                      #
    text = text + '\nREMARK     - - protein sequence - one letter code - - '   #
    line = '\nREMARK  SEQUENCE:  '                                             #
    
    for i in sequence:                                                         #
        if n >= 56:                                                            #
            n = 1                                                              #
            line =  line +  '\nREMARK  SEQUENCE:  ' + i                        #
        else:                                                                  #
            line =  line + i                                                   #
        n = n+1                                                                #
    text = text + line                                                         #
    return text
    #--------------------------------------------------------------------------#    

def AddCELLParametersToText (text,cell):
    minX           = cell['minX']
    maxX           = cell['maxX']
    minY           = cell['minY']
    maxY           = cell['maxY']
    minZ           = cell['minZ']
    maxZ           = cell['maxZ']

    text = text + '\nREMARK          - -   - -   - - CELL MODEL - -   - -   - -'
    text = text + '\nREMARK           -X       +X       -Y       +Y       -Z       +Z'
    line = '\nREMARK  CELL %8.3f %8.3f %8.3f %8.3f %8.3f %8.3f'% (minX,
                                                                  maxX,
                                                                  minY,
                                                                  maxY,
                                                                  minZ,
                                                                  maxZ)

    text = text + line                                                 
    text = text + '\nREMARK'                                           
    return text


def GeneratePDBtoProject(project, parameters = None, filename = None):
    '''
    project{
                       'User'        : user     ,
                       'ProjectName' : projectID,
                       'Info'        : add_info ,
                       'Folder'      : folder   ,
                       'Sequence'    : sequence,
                       'ABsequence'  : ABsequence,                
                       'ABmodel'     : AminoAcidDic,        
                       'Generated'   : start,                
                       'Modified'    : start,                
                       'Jobs'        : {}
                      }
    '''
    user           = project['User'       ]
    projectID      = project['ProjectName']
    add_info       = project['Info'       ]
    folder         = project['Folder'     ]
    sequence       = project['Sequence'   ]
    ABsequence     = project['ABsequence' ]  
    AminoAcidDic   = project['ABmodel'    ]
    start          = project['Generated'  ]       
    cell           = project['Cell']

    print filename  
    
    if filename == None:
        filename  = os.path.join(folder, 'InitialCoords.masters')
    
    arq  =  open(filename, 'w')
    
    text = ''
    
    text = AddHeaderToText(text, project)                   # - Header

    text = AddABSequenceToText(text, sequence)              # - Sequence

    text = AddABModelToText(text,AminoAcidDic )             # - ABModel
    
    text = AddABSequenceToText(text, ABsequence)            # - ABSequence

    text = AddCELLParametersToText  (text, cell)            # - CELL

    text = GenerateInitialPDBCoordinates(text, sequence)    # - Coordinates

    text = str(text)
    arq.writelines(text)
    arq.close()
    
    return filename

          
def GenerateRandomJob   (projects,parameters, random = False):
    """ Function doc """
    Jobs ={
            1:{
            'Title'  : 'teste com monte carlo',
            'Folder' : 'None', #
            'Type'   : 'MonteCarlo', #
            'Energy' : '1233.554', # exemplo de como deve ser o dic jobs
            'Start'  : 'ontem', #
            'End'    : 'hoje' } #
            }

                  
def CreateNewProject (projects, parameters):

    """ Function doc """
    user          = parameters['User']
    projectID     = parameters['ProjectName']
    add_info      = parameters['Info']
    folder        = parameters['Folder']
    sequence      = parameters['Sequence']
    
    ABsequence    = parameters['ABsequence']
    AminoAcidDic  = parameters['ABmodel'] 
    
    
    ABsequence = from20letterToAB (sequence, AminoAcidDic)
    index      = str(len(projects) + 1)
    start      = time.asctime(time.localtime(time.time()))
    
    #----------------------------CELL PARAMETERS-------------------------------#
    size = float(len(sequence))                                                #
    size = size + 14                                                           #
    minX = -1*(size/2)                                                         #
    minY = -20.0                                                               #
    minZ = -20.0                                                               #
    maxX =  (size/2)                                                           #
    maxY =  20.0                                                               #
    maxZ =  20.0                                                               #
    #--------------------------------------------------------------------------#
    
    projects[index] = {
                       'User'        : user     ,
                       'ProjectName' : projectID,
                       'Info'        : add_info ,
                       'Folder'      : folder   ,
                       'Sequence'    : sequence,
                       'ABsequence'  : ABsequence,                
                       'ABmodel'     : AminoAcidDic,        
                       'Generated'   : start,                
                       'Modified'    : start,                
                       'Cell'        : {'minX' : minX,
                                        'minY' : minY,
                                        'minZ' : minZ,
                                        'maxX' : maxX,
                                        'maxY' : maxY,
                                        'maxZ' : maxZ},
                       'Jobs'        : {}
                        }
    
    HOME   = os.environ.get('HOME')
    FOLDER = HOME +'/.config/MASTERS/'
    Filename = GeneratePDBtoProject(projects[index], parameters = None, filename = None)
    
    projects[index]['Jobs']['0'] = {
                                'Title'  : 'Extended coordinates from AB sequence',
                                'Folder' : folder, #
                                #'File'   : os.path.join(Filename),
                                'Input'  : '-',
                                'Output' : os.path.join(Filename),
                                'LogFile': '',
                                'Type'   : 'Initial Coordinates', #
                                'Energy' : '-', # exemplo de como deve ser o dic jobs
                                'Start'  : start, #
                                'End'    : '  -  ' } #
    
    json.dump(projects, open(FOLDER + 'ProjectHistory.dat', 'w'), indent=2)


class NewProjectDialog():
    
    """ Class doc """
    def on_new_project_entry_changed (self, entry):
        """ Function doc """
        text      = self.builder.get_object("new_project_entry").get_text()
        WorkSpace = self.MASTERSSession.GUIConfig['WorkSpace']
        path      = os.path.join(WorkSpace, text)
        print  text
        self.builder.get_object("project_directory_entry").set_text(path)
    
    
    
    
    
    def CreateNewProject_button (self, button):
        """ Function doc """
        user          =  self.builder.get_object('user_entry').get_text()
        projectID     =  self.builder.get_object('new_project_entry').get_text()
        #folder        =  self.builder.get_object('filechooserbutton1').get_filename()
        folder        =  self.builder.get_object('project_directory_entry').get_text()
        _buffer       =  self.builder.get_object('textview1').get_buffer()
        _buffer_infor =  self.builder.get_object('textview2').get_buffer()



        folder2 = folder.split('/')
        path = '/'
        for i in folder2:
            path = os.path.join(path, i)
            if not os.path.exists (path): 
                os.mkdir (path)
        
        
        
        
        
        
        sequence  = _buffer.get_text(*_buffer.get_bounds(), include_hidden_chars=False)
        add_info  = _buffer_infor.get_text(*_buffer_infor.get_bounds(), include_hidden_chars=False)
        sequence = sequence.replace('\n', '')
        sequence = sequence.replace(' ', '')
        sequence = sequence.replace('-', '')
        sequence = sequence.replace('.', '')
        sequence = sequence.replace(',', '')
        sequence = sequence.upper()
    
        if folder == None:
            self.builder.get_object('dialog1').hide()
            self.builder.get_object('messagedialog1').format_secondary_text("A folder is required")
            
            MessageDialog = self.builder.get_object('messagedialog1')
            #dialog.dialog.run()
            #dialog.dialog.hide()
            a = MessageDialog.run()  # possible "a" valors                                                           
            # 4 step                 # -8  -  yes                                                                    
            MessageDialog.hide()     # -9  -  no                                                                     
                                     # -4  -  close                                                                  
                                     # -5  -  OK                                                                     
                                     # -6  -  Cancel   
            self.builder.get_object('dialog1').run()

        elif sequence == '':
            self.builder.get_object('dialog1').hide()
            self.builder.get_object('messagedialog1').format_secondary_text("A sequence is required")
            
            MessageDialog = self.builder.get_object('messagedialog1')
            #dialog.dialog.run()
            #dialog.dialog.hide()
            a = MessageDialog.run()  # possible "a" valors                                                           
            # 4 step                 # -8  -  yes                                                                    
            MessageDialog.hide()     # -9  -  no                                                                     
                                     # -4  -  close                                                                  
                                     # -5  -  OK                                                                     
                                     # -6  -  Cancel   
            self.builder.get_object('dialog1').run()
        
        else:
            parameters =   {'User'        : user     ,
                            'ProjectName' : projectID,
                            'Info'        : add_info ,
                            'Folder'      : folder   ,
                            'Sequence'    : sequence,
                            'ABsequence'  : None,                
                            'ABmodel'     : AminoAcidDic,        
                            'Generated'   : None,                
                            'Modified'    : None,                
                            'Jobs'        : {}
                            }
            
            """ Starting a new project 
                'Title'  : 'Testing MonteCarlos Sim',
                'Folder' : folder,                
                'Input'  : filename_in,
                'Output' : filename_out,
                'LogFile': ''          , 
                'Type'   : 'MonteCarlo', 
                'Energy' : str(rdm.random()*1.2345),                   
                'Start'  : '  -  ',                 
                'End'    : '  -  ' } 
            """


            
            CreateNewProject (self.projects, parameters)
            
            print self.projects
            self.WindowControl.AddProjectHistoryToTreeview(liststore = self.main_builder.get_object('liststore2'))

        
        
            
    def __init__(self,MASTERSSession): #main_builder=None, projects = None, WindowControl = None, GUIConfig = None):
        
        """ Class initialiser """
        
        self.MASTERSSession   =  MASTERSSession
        self.projects         =  MASTERSSession.projects
        login                 =  os.getlogin()
        if self.projects == None:
            self.projects = {}
        
        self.builder = gtk.Builder()
        
        self.main_builder = MASTERSSession.builder

        self.builder.add_from_file(
            os.path.join('MastersNewProject.glade'))
        self.builder.connect_signals(self)
        
        self.dialog    = self.builder.get_object('dialog1')
        self.GUIConfig = MASTERSSession.GUIConfig
        
        
        
        localtime = time.asctime(time.localtime(time.time()))
        print "Local current time :", localtime
        localtime = localtime.split()

        #  0     1    2       3         4
        #[Sun] [Sep] [28] [02:32:04] [2014]
        text = login + '_project_' + localtime[1] + \
            '_' + localtime[2] + '_' + localtime[4]
        self.builder.get_object("new_project_entry").set_text(text)
        self.builder.get_object("user_entry").set_text(login)
        
        
        
        if self.GUIConfig  != None:
            self.builder.get_object('project_directory_entry').set_text(self.GUIConfig['WorkSpace'])
        
        
        '''
		--------------------------------------------------
		-                                                -
		-	              WindowControl                  -
		-                                                -
		--------------------------------------------------
		'''
        
        self.WindowControl = MASTERSSession.WindowControl

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

