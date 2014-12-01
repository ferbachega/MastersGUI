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
# Imports
#from OpenGL.GL import *
#from OpenGL.GLU import *

#GUI
from FileChooserWindow    import *
from NewProjectDialog     import NewProjectDialog
from WindowControl        import WindowControl








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





global slab
global clicado, ZeroX, ZeroY, Buffer, Zero_ViewBuffer, Menu
slab            = 50
zoom            = 1.0
angle           = 0.0
sprite          = None
zfactor         = 0.005
clicado         = False
ZeroX           = 0
ZeroY           = 0
Buffer          = 0
Zero_pointerx   = 0
Zero_pointery   = 0
Zero_ViewBuffer = None
Menu            = True


def draw(glarea, event):
    # Get surface and context
    glcontext = glarea.get_gl_context()
    gldrawable = glarea.get_gl_drawable()

    # Start opengl context
    if not gldrawable.gl_begin(glcontext):
        return

    # Actual drawing
    global sprite, angle, zoom

    # Clear screen
    #rabbyt.clear((0.0, 0.0, 0.0))

    # Render sprite
    if sprite is not None:
        sprite.rot = angle
        sprite.scale = zoom
        sprite.render()

    # Flush screen
    gldrawable.swap_buffers()
    pymol.draw()
    # End opengl context
    gldrawable.gl_end()

    return True
# Resizing function


def reshape(glarea, event):

    reshape = event
    reshape_x = reshape.width
    reshape_y = reshape.height
    pymol.reshape(reshape_x, reshape_y, 0)
    pymol.idle()
    # pymol.draw()

    # Get surface and context
    glcontext = glarea.get_gl_context()
    gldrawable = glarea.get_gl_drawable()

    # Start opengl context
    if not gldrawable.gl_begin(glcontext):
        return

    # Get widget dimensions
    x, y, width, height = glarea.get_allocation()

    pymol.reshape(width, height, True)

    # Reset rabbyt viewport
    #rabbyt.set_viewport((width, height))
    # rabbyt.set_default_attribs()

    # End opengl context
    pymol.draw()
    gldrawable.swap_buffers()
    gldrawable.gl_end()
    #

    return True

# Initialization function
def init(glarea):
    print 'init'
    # Get surface and context
    glcontext = glarea.get_gl_context()
    gldrawable = glarea.get_gl_drawable()

    # Start opengl context
    if not gldrawable.gl_begin(glcontext):
        return

    # Get widget dimensions
    x, y, width, height = glarea.get_allocation()

    # Reset rabbyt viewport
    #rabbyt.set_viewport((width, height))
    # rabbyt.set_default_attribs()

    # Get sprite variable
    global sprite

    # Load sprite
    #sprite = rabbyt.Sprite('sprite.png')

    # End opengl context
    gldrawable.gl_end()

    return True

# Idle function
def idle(glarea):
    # Get vars
    global angle, zoom, zfactor

    # Update angle
    angle += 1.0
    if angle > 359:
        angle = 0.0

    # Update zoom
    if zoom > 10 or zoom < 1:
        zfactor = -zfactor
        zoom += zfactor

    # Needed for synchronous updates
    glarea.window.invalidate_rect(glarea.allocation, False)
    glarea.window.process_updates(False)

    return True

# Map events function
def map(glarea, event):
    # print 'map'
    # Add idle event
    gobject.idle_add(idle, glarea)
    return True

def slabchange(button, event):
    global slab
    x, y, width, height = glarea.get_allocation()
    if event.direction == gtk.gdk.SCROLL_UP:
        step = 1.5
        slab = slab + step
        slab = slab + step
        # if  slab >=100:
        #   slab = 100
    else:
        step = -1.5

        slab = slab + step
        if slab <= -5:
            slab = -5
    pymol.cmd.clip('slab', slab)
    #cmd.zoom(buffer = Buffer)
    return step
    pymol.button(button, 0, x, y, 0)
    pymol.idle()

def show_context_menu(widget, event):
    x, y, state = event.window.get_pointer()
    if clicado:
        if event.button == 3:
            widget.popup(None, None, None, event.button, event.time)

def mousepress(button, event):
    global ZeroX, ZeroY
    
    ZeroX, ZeroY, state = event.window.get_pointer()
    
    #print ZeroX, ZeroY
    
    x, y, width, height = glarea.get_allocation()

        
    if event.button == 3:
        global clicado
        clicado = True
        #print 'gordao'
        x, y, width, height = glarea.get_allocation()
        #print x, y, width, height
        mousepress = event
        button = mousepress.button - 1
        pointerx = int(mousepress.x)
        pointery = int(mousepress.y)
        calc_y = height - pointery
        #print pointerx,pointery,calc_y
        #cmd.zoom(buffer=calc_y)
        pymol.button(button, 0, pointerx , calc_y, 0)

        
    if event.button != 3:
        x, y, width, height = glarea.get_allocation()
        mousepress = event
        button = mousepress.button - 1
        pointerx = int(mousepress.x)
        pointery = int(mousepress.y)
        calc_y = height - pointery
        pymol.button(button, 0, pointerx, calc_y, 0)

def mouserelease(button, event):
    x, y, width, height = glarea.get_allocation()
    mouserelease = event
    button = mouserelease.button - 1
    pointerx = int(mouserelease.x)
    pointery = int(mouserelease.y)
    calc_y = height - pointery
    pymol.button(button, 1, pointerx, calc_y, 0)
    
def mousemove(button, event):
    global clicado, Buffer,Zero_pointerx, Zero_pointery, Zero_ViewBuffer, Menu
    x, y, width, height = glarea.get_allocation()
    clicado = False
    mousemove = event
    pointerx = int(mousemove.x)
    pointery = int(mousemove.y)

    calc_y2  = (float(Zero_pointery - pointery))/10.0
    calc_y   = height - pointery
    
    if clicado:
        global ZeroY
        #print 'a'
        #print clicado
        #print Menu
        #Buffer = (calc_y2)
        #_view   = cmd.get_view()
        #
        #print _view
        #if Zero_ViewBuffer == None:
        #   Zero_ViewBuffer = _view[11]
        #
        #_view11 = Zero_ViewBuffer - Buffer
        #_view15 = _view[15]       - Buffer
        #_view16 = _view[16]       + Buffer
        #
        #_view2 = (_view[0], _view[1], _view[2],
        #         _view[3], _view[4], _view[5],
        #         _view[6], _view[7], _view[8],
        #         _view[9], _view[10],_view11,
        #         _view[12],_view[13],_view[14],
        #         _view15,  _view16,  _view[17])
        #
        #print Buffer, _view11, _view15,_view16
        #cmd.set_view(_view2)
        #Zero_pointerx   = pointerx
        #Zero_pointery   = pointery
        #Zero_ViewBuffer = _view11
    #else:
    pymol.drag(pointerx, calc_y, 0)
    pymol.idle()

def my_menu_func(menu):
    print "Menu clicado"

def context_menu():
    builder = masters.builder
    menu = builder.get_object('GLArea_menu')
    return menu


# Create opengl configuration
try:
    # Try creating rgb, double buffering and depth test modes for opengl
    glconfig = gtk.gdkgl.Config(mode=(gtk.gdkgl.MODE_RGB |
                                      gtk.gdkgl.MODE_DOUBLE |
                                      gtk.gdkgl.MODE_DEPTH))
except:
    # Failed, so quit
    sys.exit(0)








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
    
    
    def on_treeview3_row_activated (self, tree, path, column):
        """ Function doc """
        model = tree.get_model()  # @+
        iter  = model.get_iter(path)  # @+
        JobID = model.get_value(iter, 0)  # @+
        
        
        #print _object
        print self.projects[self.active_project]['Jobs'][JobID]
        filename = self.projects[self.active_project]['Jobs'][JobID]['File']
        print filename
        self.OpenMasterFile(filename)
        
        
    def row_activated2(self, tree, path, column):

        model = tree.get_model()  # @+
        iter = model.get_iter(path)  # @+
        
        projectID           = model.get_value(iter, 0)  # @+
        self.active_project = projectID
        
        Jobs   = self.projects[projectID]['Jobs']
        Folder = self.projects[projectID]['Folder']
        
        print Jobs
        liststore = self.builder.get_object("liststore1")
        
        try:
            self.WindowControl.AddJobHistoryToTreeview(liststore, Jobs)
        except:
            pass
        
        text = 'Project: ' + self.projects[projectID]['ProjectName'] + '    Folder:' + Folder
        self.WindowControl.STATUSBAR_SET_TEXT(text)
        print self.active_project


    def __init__(self):
        print '           Intializing MasterGUI object          '
        self.home = os.environ.get('HOME')
        #---------------------------------- MasterGUI ------------------------------------#
        self.builder = gtk.Builder()                                                      #
        self.builder.add_from_file("MastersMainWindow2-projects.glade")                   #
        self.win     = self.builder.get_object("window1")                                 #
        self.win.show()                                                                   #
        self.builder.connect_signals(self)                                                #
        #---------------------------------------------------------------------------------#

        self.projects = {}
        
        HOME   = os.environ.get('HOME')
        FOLDER = HOME +'/.config/MASTERS/'
        
        self.projects       = json.load(open(FOLDER + 'ProjectHistory.dat'))
        self.active_project = None    
        
        '''
        'title' : {'path' : None,
                   'type' : None, 
              'generated' : None, 
               'modified' : None } 
        '''                


        
        '''
        #-----------------------------------------------#
        #             MastersProjectControl             #
        #-----------------------------------------------#
        projects = ProjectsControl(self.builder, True)  #
        projects.AddHistoryToTreeview()                 #
        #-----------------------------------------------#
        '''
        
        
        # Dialogs
        self.WindowControl    = WindowControl(self.builder, self.projects )
        self.NewProjectDialog = NewProjectDialog(self.builder, self.projects,  self.WindowControl )
        #pprint(self.projects)
        #
        #for i in self.projects:
        #    i = int(i)
        #    #data = [self.projects[i]['ProjectName'], self.projects[i]['Modified'], str(len(self.projects[1]['Jobs'])), self.projects[i]['User'] ]
        #    #print data
        #    ##model.append(data)        
        #
        #pprint(self.projects)

        
        self.WindowControl.AddProjectHistoryToTreeview(liststore = self.builder.get_object('liststore2'))


        
        
        
        
        
        
        
        
        container = self.builder.get_object("container")
        pymol.start()
        cmd = pymol.cmd
        container.pack_start(glarea)
        glarea.show()

        #-------------------- config PyMOL ---------------------#
        #                                                       #
        pymol.cmd.set("internal_gui", 0)                        #
        pymol.cmd.set("internal_gui_mode", 0)                   #
        pymol.cmd.set("internal_feedback", 0)                   #
        pymol.cmd.set("internal_gui_width", 220)                #
        sphere_scale = 0.1                                      #
        stick_radius = 0.15                                     #
        label_distance_digits = 4                               #
        mesh_width = 0.3                                        #
        cmd.set('sphere_scale', sphere_scale)                   #
        cmd.set('stick_radius', stick_radius)                   #
        cmd.set('label_distance_digits', label_distance_digits) #
        cmd.set('mesh_width', mesh_width)                       #
        cmd.set("retain_order")         # keep atom ordering    #
        cmd.bg_color("grey")            # background color      #
        cmd.do("set field_of_view, 70")                         #
        cmd.do("set ray_shadows,off")                           #
                                                                #
                                                                #

        cmd.set('ribbon_sampling', 3)                           #
        #-------------------------------------------------------#

                                      

    def run(self):
        gtk.main()


print "Creating object"
glarea = gtk.gtkgl.DrawingArea(glconfig)
glarea.set_size_request(600, 400)
glarea.connect_after('realize', init)
glarea.connect('configure_event', reshape)
glarea.connect('expose_event', draw)
glarea.connect('map_event', map)
glarea.set_events(glarea.get_events() | gtk.gdk.BUTTON_PRESS_MASK | gtk.gdk.BUTTON_RELEASE_MASK |
                  gtk.gdk.POINTER_MOTION_MASK | gtk.gdk.POINTER_MOTION_HINT_MASK | gtk.gdk.KEY_PRESS_MASK)                      

glarea.connect("button_press_event", mousepress)      
glarea.connect("button_release_event", mouserelease)  
glarea.connect("motion_notify_event", mousemove)      
glarea.connect("scroll_event", slabchange)
glarea.set_can_focus(True)
import pymol2
pymol   = pymol2.PyMOL(glarea)
masters = MastersMain()
glarea.connect_object("button_release_event", show_context_menu, context_menu())



def main():
    #masters = MastersMain()
    masters.run()
    return 0

if __name__ == '__main__':
	main()
