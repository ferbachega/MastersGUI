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
import json
from  pprint import pprint
import pango
# Imports
#from OpenGL.GL import *
#from OpenGL.GLU import *

#GUI
from FileChooserWindow      import *
from NewProjectDialog       import NewProjectDialog
from WindowControl          import WindowControl
from MCwindow               import MonteCarloSimulationWindow
from MastersWorkSpaceDialog import WorkSpaceDialog
from BoxSetupDialog         import BoxSetupDialog
# Imports
from OpenGL.GL import *
from OpenGL.GLU import *
#GUI
#from MastersNewProjectDialog import *
from FileChooserWindow           import *
from pymol import cmd
from pymol.cgo import *


HOME = os.environ.get('HOME')

if not os.path.isdir(HOME +'/.config/MASTERS' ):
    os.mkdir(HOME +'/.config/MASTERS' )
    print "Temporary files directory:  %s" % HOME +'/.config/MASTERS' 



class MastersMain():
    def OpenMasterFile (self, filename):
        """ Function doc """
        arq = open(filename, "r")
        t = None
        s = None
        history = []
        
        for line in arq:
            line2 = line.split()
            
            try:
                if line2[0] == 'REMARK':
                    print line
                    if line2[1] == "t":
                        t = line2[3].split(',')
                    elif line2[1] == "s":
                        s = line2[3].split(',')
                    else:
                        history.append(str(line[6:].replace('\n', '')))
            except:
                pass
            
               
        #liststore = self.builder.get_object('liststore1')
        #self.TREEVIEW_ADD_DATA(liststore, history)
        #
        #print t
        #print s
        #print history
        #x = []
        #y = []
        #try:
        #    for i in t:
        #        x.append(float(i))
        #    for i in s:
        #        y.append(float(i))    
        #except:
        #    pass
        #self.PlotData(x,y)
        ##cmd.load(filename)
        cmd.delete('all')
        cmd.load(filename)                     
        cmd.hide('all')                        
        
        cmd.show("spheres")                    
        cmd.show('ribbon')                     
        
        
        
        '''
        'A':['Ala','HID','A']
        'R':['Arg','POL','B']
        'N':['Asn','POL','B'] 
        'D':['Asp','POL','B'] 
        'C':['Cys','HID','A'] 
        'E':['Glu','POL','B'] 
        'Q':['Gln','POL','B'] 
        'G':['Gly','HID','A'] 
        'H':['His','POL','B'] 
        'I':['Ile','HID','A'] 
        'L':['Leu','HID','A'] 
        'K':['Lys','POL','B'] 
        'M':['Met','HID','A'] 
        'F':['Phe','POL','B'] 
        'P':['Pro','HID','A'] 
        'S':['Ser','POL','B'] 
        'T':['Thr','POL','B'] 
        'W':['Trp','POL','B'] 
        'Y':['Tyr','POL','B'] 
        'V':['Val','HID','A'] 
        ''' 
        
        
        cmd.color('blue')
        cmd.do('select resn leu')
        cmd.do('color red, sele')
        
        cmd.do('select resn ala')
        cmd.do('color red, sele')
        
        cmd.do('select resn ile')
        cmd.do('color red, sele')
        
        cmd.do('select resn pro')
        cmd.do('color red, sele')
        
        cmd.do('select resn val')
        cmd.do('color red, sele')
        
        cmd.do('select resn met')
        cmd.do('color red, sele')
        
        cmd.do('select resn gly')
        cmd.do('color red, sele')
        
        cmd.do('select resn cys')
        cmd.do('color red, sele') 


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

    def on_toolbutton9_clicked (self, button):
        """ Function doc """
        print button 
    
    def on_toolbutton_MC_clicked(self, button):
        """ Function doc """
        #if self.MCwindow.Visible == False:
        #    self.MCwindow.OpenWindow(ActivedProject =self.ActivedProject)
        MonteCarloSimulationWindow (self)

    
    
    def on_treeview3_button_release_event(self, tree, event):
        """ Function doc """
        if event.button == 3:
            #print 'button3'
            #print "Mostrar menu de contexto botao3"
            selection     = tree.get_selection()
            model         = tree.get_model()
            (model, iter) = selection.get_selected()
            
            if iter != None:
                self.selectedID  = str(model.get_value(iter, 1))
                self.selectedObj = str(model.get_value(iter, 2))

                self.builder.get_object('TreeViewObjLabel').set_label('- ' +self.selectedID+' -' )
                widget = self.builder.get_object('treeview_menu')
                widget.popup(None, None, None, event.button, event.time)
            
        if event.button == 1:
            #print "Mostrar menu de contexto botao1"
            selection     = tree.get_selection()
            model         = tree.get_model()
            (model, iter) = selection.get_selected()
            
            if iter != None:
                #print model, iter
                JobID         = model.get_value(iter, 0)
                pymol_object  = model.get_value(iter, 2)  # @+
                #print _object
                #pprint (self.projects[self.ActivedProject]['Jobs'][JobID])
                filename = self.projects[self.ActivedProject]['Jobs'][JobID]['Output']
                #print filename
                self.load_file(filename)
                




    def on_treeview3_row_activated (self, tree, path, column):
        """ Function doc """
        model = tree.get_model()  # @+
        iter  = model.get_iter(path)  # @+
        JobID = model.get_value(iter, 0)  # @+
        
        
        #pprint (self.projects[self.ActivedProject]['Jobs'][JobID])
        
        #filename = self.projects[self.ActivedProject]['Jobs'][JobID]['Output']
        MCwindow (self, JobID)


    def load_file(self, filename):
    
        ## add Loading message to status bar and ensure GUI is current
        #self.statusbar.push(self.statusbar_cid, "Loading %s" % filename)
        #while gtk.events_pending(): gtk.main_iteration()
        #
        #try:
        # get the file contents
        fin = open(filename, "r")
        text = fin.read()
        fin.close()
        
        # disable the text view while loading the buffer with the text
        self.text_view.set_sensitive(False)
        buff = self.text_view.get_buffer()
        buff.set_text(text)
        buff.set_modified(False)
        self.text_view.set_sensitive(True)
        
        # now we can set the current filename since loading was a success
        #self.filename = filename

    
    def row_activated2(self, tree, path, column):

        model = tree.get_model()  # @+
        iter = model.get_iter(path)  # @+
        
        projectID           = model.get_value(iter, 0)  # @+
        self.ActivedProject = projectID
        
        Jobs   = self.projects[projectID]['Jobs']
        Folder = self.projects[projectID]['Folder']

        liststore = self.builder.get_object("liststore1")
        
        try:
            self.WindowControl.AddJobHistoryToTreeview(liststore, Jobs)
        except:
            pass
        
        text = 'Project: ' + self.projects[projectID]['ProjectName'] + '    Directory:' + Folder
        self.WindowControl.STATUSBAR_SET_TEXT(text)
        print self.ActivedProject
        
        buff = self.text_view.get_buffer()
        buff.set_text('')
        buff.set_modified(False)
    
    def Save_GUI_ConfigFile(self):
        """ Function doc """
        path = os.path.join(self.home,'.config')
        if not os.path.exists (path): 
            os.mkdir (path)

        path = os.path.join(path, 'MASTERS')
        if not os.path.exists (path): 
            os.mkdir (path)
        
        filename = os.path.join(path,'GUI.config')
        json.dump(self.GUIConfig, open(filename, 'w'), indent=2)

    def Load_GUI_ConfigFile (self, filename = None):
        """ Function doc """
        #.config
        path = os.path.join(self.home,'.config', 'MASTERS', 'GUI.config')
        
        try:
            self.GUIConfig = json.load(open(path)) 
        except:
            print 'error: GUIConfig file not found'
            print 'open WorkSpace Dialog'




    def on_menuitem_show_model_activate(self, menuitem):
        """ Function doc """
        #print "Mostrar menu de contexto botao1"
        selection     = self.builder.get_object('treeview3').get_selection()
        model         = self.builder.get_object('treeview3').get_model()
        (model, iter) = selection.get_selected()
        
        if iter != None:
            JobID         = model.get_value(iter, 0)
            pymol_object  = model.get_value(iter, 2)  # @+
            filename = self.projects[self.ActivedProject]['Jobs'][JobID]['Output']



        dialog = BoxSetupDialog(filein = filename)



    def __init__(self):
        print '           Intializing MasterGUI object          '
        self.home = os.environ.get('HOME')
        
        #---------------------------------- MasterGUI ------------------------------------#
        self.builder = gtk.Builder()                                                      #
        self.builder.add_from_file("MastersMainWindow2-projects.glade")                   #
        self.win     = self.builder.get_object("window1")                                 #
        self.win.show()                                                                   #
        self.builder.connect_signals(self)                                                #
        #self.statusbar = builder.get_object("statusbar")
        self.text_view = self.builder.get_object("textview1")
        self.text_view.modify_font(pango.FontDescription("monospace 10"))
        #---------------------------------------------------------------------------------#

        self.projects = {}
        
        self.selectedID  = None
        self.selectedObj = None    
        
        HOME   = os.environ.get('HOME')
        FOLDER = os.path.join(HOME, '.config/MASTERS/')
        try:
            self.projects       = json.load(open(FOLDER + 'ProjectHistory.dat'))
        except:
            self.projects       = {}
        
        self.ActivedProject = None    
        
        
        
        
        
        #---------------------------------------------------------#
        #                  MASTERS GUI CONFIG                     #
        #---------------------------------------------------------#
        self.GUIConfig = {                              
                       'HideWorkSpaceDialog': False,  
                       'WorkSpace'          : HOME,  
                       'History'            : {}   } 
        self.Load_GUI_ConfigFile()
        #---------------------------------------------------------#

        
        
        '''
        #-----------------------------------------------#
        #             MastersProjectControl             #
        #-----------------------------------------------#
        projects = ProjectsControl(self.builder, True)  #
        projects.AddHistoryToTreeview()                 #
        #-----------------------------------------------#
        '''
        
        
        #---------------------------------------Dialogs and Windows-----------------------------------------------------#
        self.WindowControl    = WindowControl   (self.builder, self.projects )                                          #
        self.NewProjectDialog = NewProjectDialog(self)#.builder, self.projects, self.WindowControl, self.GUIConfig )    #
        #self.MCwindow         = MCwindow        (self.builder, self.projects, self.ActivedProject, self.WindowControl)  #                                                   
        self.WorkSpaceDialog  = WorkSpaceDialog (self)                                                                  #
        #---------------------------------------------------------------------------------------------------------------#

     
        self.WindowControl.AddProjectHistoryToTreeview(liststore = self.builder.get_object('liststore2'))                
        
        if self.GUIConfig['HideWorkSpaceDialog'] == False:
            self.WorkSpaceDialog.dialog.run()
            self.WorkSpaceDialog.dialog.hide()
            
            
            
    def run(self):
        gtk.main()

def main():
    masters = MastersMain()
    masters.run()
    return 0

if __name__ == '__main__':
	main()

