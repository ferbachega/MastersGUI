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

# Imports
from OpenGL.GL import *
from OpenGL.GLU import *

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





class MCwindow:
    """ Class doc """
    
    def OpenWindow (self):
        """ Function doc """
        if self.Visible  ==  False:
            self.builder = gtk.Builder()
            self.builder.add_from_file('MastersMonteCarloSimulationWindow.glade')
            self.builder.connect_signals(self)
            self.window = self.builder.get_object('window1')
            
            '''
            --------------------------------------------------
            -                                                -
            -	              WindowControl                  -
            -                                                -
            --------------------------------------------------
        
            self.window_control = WindowControl(self.builder)
           
            #--------------------- Setup ComboBoxes -------------------------
            combobox  = 'ScanDialog_combobox_SCAN_reaction_coordiante_type'                     
            combolist = ['simple-distance', 'multiple-distance']
            self.window_control.SETUP_COMBOBOXES(combobox, combolist, 0)     

            combobox  = 'ScanDialog_combobox_optimization_method'                     
            combolist = ['Conjugate Gradient', 'Steepest Descent','LBFGS']
            self.window_control.SETUP_COMBOBOXES(combobox, combolist, 0)     
            '''            
            
            self.window.show()                                               
            self.builder.connect_signals(self)                                   
            self.Visible  =  True
            gtk.main()
            #----------------------------------------------------------------
    def  on_MCwindow_destroy(self, widget):
        """ Function doc """
        self.Visible  =  False

    def __init__(self, main_builder = None, projects = None, WindowControl = None):
        self.projects   =  projects
        self.Visible    =  False
        
        
        #print '           Intializing MC MASTERS GUI object          '
        #self.home = os.environ.get('HOME')
        #
        ##------------------------------------------- MasterGUI ----------------------------------------------#
        ##                                                                                                    #
        #self.builder = gtk.Builder()                                                                         #
        #self.builder.add_from_file("/home/labio/Documents/MASTERS/MastersMonteCarloSimulationWindow.glade")  #
        ##                                                                                                    #
        #self.win = self.builder.get_object("window1")                                                        #
        ##                                                                                                    #
        #self.win.show()                                                                                      #
        ##                                                                                                    #
        #self.builder.connect_signals(self)                                                                   #
        ##                                                                                                    #
        ##----------------------------------------------------------------------------------------------------#  


def main():
	
	return 0

if __name__ == '__main__':
	main()

