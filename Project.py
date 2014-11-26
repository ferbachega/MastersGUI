#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Project.py
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
import random as rdm 
import time
import os
from pprint import pprint 

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


class MasterProject:
    """ Class doc """
    
    def __init__ (self):
        """ Class initialiser """
        
        self.settings = {
                        'title'     : 'My Project',                                 #just a name
                        'directory' : os.environ.get('HOME'),                       #path 
                        'sequence'  : None,                                         #sequence
                        'ABsequence': None,                                         #sequence converted to As and Bs
                        'AAmodel'   : AminoAcidDic,                                 #dictionary containg  de A and B residues
                        'generated' : None,                                         #
                        'modified'  : None,                                         #
                        'info'      : 'information like: SOD protein from T.cruzy', # 
                        'jobs'      : {                                             #
                                       1:{'path' : None,
                                          'type' : None, 
                                        'energy' : None, 
                                         'start' : None, 
                                           'end' : None } #
                                      }
                        }

    
    
    
    def ExportDataToFile (self, path, filename = "log.gui.txt"):
        """ The new  DualTextLog writes the log files right to the 
        diretory where the job is already running."""
        
        if not os.path.isdir(path):
            os.mkdir(path)
            print "Temporary files directory:  %s" % path
        
        header = '''
        #-----------------------------------------------------------------------------#
        #                                                                             #
        #                                MASTERS-GUI                                  #
        #                        - A MASTERS graphical tool -                         #
        #                                                                             #
        #-----------------------------------------------------------------------------#
        #                                                                             #
        #                              Developed by LABIO                             #
        #                               <labio@pucrs.br>                              #
        #                                                                             #
        #             visit: https://github.com/ferbachega/MastersGUI                 #
        #      Pontifical Catholic University of Rio Grande do Sul - RS, Brazil       #
        #                                                                             #
        #                                                                             #
        #                        - Thiago Lipinski-Paes                               #
        #                        - Michele Silva                                      #
        #                        - Jose Fernando R Bachega                            #
        #                        - Vanessa S. Machado                                 #
        #                        - Walter R. Paixao-Cortes                            #
        #                        - Osmar Norbeto de souza                             #
        #                                                                             #
        #   Cite this work as:                                                        #
        #                                                                             #
        #      Lipinski-Paes, T., & de Souza, O. N. (2014). MASTERS: A General        #
        #      Sequence-based MultiAgent System for Protein TERtiary Structure        #
        #      Prediction. Electronic Notes in Theoretical Computer Science,          #
        #      306, 45–59. doi:10.1016/j.entcs.2014.06.014                            #
        #                                                                             #
        #-----------------------------------------------------------------------------#


        '''
        
                    
        #Directory:      /home/labio/Documents/MasterProjectExanple/1_MonteCarlo
        #Version:        1.0
        #Parameter_file: /home/labio/Documents/MasterProjectExanple/1_MonteCarlo/1_MonteCarlo.config
    

    def IncrementStep (self, path=None, _type = 'testing', energy=None, start = None, end = None):
        
        """ Function doc """
        step   = len(self.settings['jobs'])+1
        self.settings['jobs'][step] = {'path' : path   ,
                                       'type' : _type  , 
                                     'energy' : energy , 
                                      'start' : start  , 
                                        'end' : end    }
    
    def RunMonteCarlo (self, test = False):
        """ Roda um job generico e incrementa informacoes ao settings """
        start      = time.asctime(time.localtime(time.time()))
        
        if test == True:
            _type  = 'MonteCarlo'
            self.settings['counter'] =+ 1
            step   = len(self.settings['jobs'])+1

            path   = self.settings['directory']
            path   = path + '/'+ str(step) + '_' + _type
            energy = rdm.random()
            end    = time.asctime(time.localtime(time.time()))
            self.settings['jobs'][step] = {'path' : path   ,
                                           'type' : _type  , 
                                         'energy' : energy , 
                                          'start' : start  , 
                                            'end' : end    }
            

        
    def RemoveJob (self):
        """ Function doc """
        pass




class LogFileWriter:
    """ Class doc """
    def __init__ (self):
        """ Class initialiser """
        pass

















def main():
    Project =  MasterProject()
    #pprint (Project.settings['jobs'])
    Project.RunMonteCarlo(test = True)
    #pprint (Project.settings['jobs'])
    Project.RunMonteCarlo(test = True)
    pprint (Project.settings['jobs'])

    return 0

if __name__ == '__main__':
	main()

