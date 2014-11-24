#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  MainWindow2-project.py
#  
#  Copyright 2014 Fernando Bachega <fernando@bachega>
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
import datetime
import time
import pygtk
pygtk.require('2.0')
import gtk
import gtk.gtkgl

#import thread
import threading
import gobject
import sys
import glob
import math
import os

# Imports
from OpenGL.GL import *
from OpenGL.GLU import *

#GUI
from FileChooserWindow           import *
from MastersProject              import *

class MastersMain():
    
    def on_toolbutton_NewProject_clicked(self, button):
        """ Function doc """
        self.NewProjectDialog.dialog.run()
        self.NewProjectDialog.dialog.hide()

    def on_toolbutton_LoadMasterProject_clicked(self, button):
        """ Function doc """
        FileChooser = FileChooserWindow()
        FileName = FileChooser.GetFileName(self.builder)
        print FileName
        #self.OpenMasterFile (FileName)

    def on_toolbutton_SaveProject_clicked (self, button):
        """ Function doc """
        print "Save project"

    def on_toolbutton_SaveAsProject_clicked (self, button):
        """ Function doc """
        print "Save As project"        
        
    def on_toolbutton_SetupBoxSize_clicked (self, button):    
        print "Setup Box Size"        

    
    def row_activated2(self, tree, path, column):

        model = tree.get_model()  # @+
        iter = model.get_iter(path)  # @+
        pymol_object = model.get_value(iter, 1)  # @+
        true_or_false = model.get_value(iter, 0)
        # atomtype = model.get_value( iter, 2) #@+
        # print true_or_false

        if true_or_false == False:
            true_or_false = True
            model.set(iter, 0, true_or_false)
            # print true_or_false

        else:
            true_or_false = False
            model.set(iter, 0, true_or_false)
            # print true_or_false


    def __init__(self):
        print '           Intializing MasterGUI object          '
        self.home = os.environ.get('HOME')
        #---------------------------------- MasterGUI ------------------------------------#
        self.builder = gtk.Builder()                                                      #
        self.builder.add_from_file("MastersMainWindow2-projects.glade")                   #
        self.win     = self.builder.get_object("window1")                                     #
        self.win.show()                                                                   #
        self.builder.connect_signals(self)                                                #
        #---------------------------------------------------------------------------------#
        
        
        #-----------------------------------------------#
        #             MastersProjectControl             #
        #-----------------------------------------------#
        projects = ProjectsControl(self.builder, True)  #
        projects.AddHistoryToTreeview()                 #
        #-----------------------------------------------#
        
        
        #-----------------------------------------------#
        #            MastersProjectTextView             #
        #-----------------------------------------------#
        textview   = self.builder.get_object("textview1")
        textbuffer = textview.get_buffer()
        infile = open("./test/NoName.out", "r")

        if infile:
            string = infile.read()
            infile.close()
            textbuffer.set_text(string)
        #self.NewProjectDialog = NewProjectDialog()                                            

    def run(self):
        gtk.main()


def main():
    masters = MastersMain()
    masters.run()
    return 0

if __name__ == '__main__':
	main()

