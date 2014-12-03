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



class PyMOL:
    """ Class doc """
    
    def __init__ (self, glaera):
        """ Class initialiser """
        #global slab
        #global clicado, ZeroX, ZeroY, Buffer, Zero_ViewBuffer, Menu
        self.slab            = 50
        self.zoom            = 1.0
        self.angle           = 0.0
        self.sprite          = None
        self.zfactor         = 0.005
        self.clicado         = False
        self.ZeroX           = 0
        self.ZeroY           = 0
        self.Buffer          = 0
        self.Zero_pointerx   = 0
        self.Zero_pointery   = 0
        self.Zero_ViewBuffer = None
        self.Menu            = True
        
        self.glaera = glaera
        #self.glarea.connect_after('realize'        , self.init)
        #self.glarea.connect      ('configure_event', self.reshape)
        #self.glarea.connect      ('expose_event'   , self.draw)
        #self.glarea.connect      ('map_event'      , map)
        #self.glarea.set_events(glarea.get_events() | gtk.gdk.BUTTON_PRESS_MASK | gtk.gdk.BUTTON_RELEASE_MASK |
        #               gtk.gdk.POINTER_MOTION_MASK | gtk.gdk.POINTER_MOTION_HINT_MASK | gtk.gdk.KEY_PRESS_MASK)                      
        #
        #self.glarea.connect("button_press_event", mousepress)      
        #self.glarea.connect("button_release_event", mouserelease)  
        #self.glarea.connect("motion_notify_event", mousemove)      
        #self.glarea.connect("scroll_event", slabchange)
        self.glarea.set_can_focus(True)
        
        import pymol2
        pymol   = pymol2.PyMOL(self.glarea)
        #glarea.connect_object("button_release_event", show_context_menu, context_menu())

    def draw(self, glarea, event):
        # Get surface and context
        glcontext  = self.glarea.get_gl_context()
        gldrawable = self.glarea.get_gl_drawable()

        # Start opengl context
        if not gldrawable.gl_begin(glcontext):
            return

        # Actual drawing

        if sprite is not None:
            self.sprite.rot = angle
            self.sprite.scale = zoom
            self.sprite.render()

        # Flush screen
        gldrawable.swap_buffers()
        pymol.draw()
        # End opengl context
        gldrawable.gl_end()

        return True
        # Resizing function
    
    
    
    def reshape(self, glarea, event):

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
    def init(self, glarea):
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
    def idle(self, glarea):
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
    def map(self, glarea, event):
        # print 'map'
        # Add idle event
        gobject.idle_add(idle, glarea)
        return True

    def slabchange(self, button, event):
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

    def show_context_menu(self, widget, event):
        x, y, state = event.window.get_pointer()
        if clicado:
            if event.button == 3:
                widget.popup(None, None, None, event.button, event.time)

    def mousepress(self, button, event):
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

    def mouserelease(self, button, event):
        x, y, width, height = glarea.get_allocation()
        mouserelease = event
        button = mouserelease.button - 1
        pointerx = int(mouserelease.x)
        pointery = int(mouserelease.y)
        calc_y = height - pointery
        pymol.button(button, 1, pointerx, calc_y, 0)
        
    def mousemove(self, button, event):
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

    def my_menu_func(self, menu):
        print "Menu clicado"

    def context_menu(self):
        builder = masters.builder
        menu = builder.get_object('GLArea_menu')
        return menu




        
class MCwindow:
    """ Class doc """
    
    def OpenWindow (self):
        """ Function doc """
        if self.Visible  ==  False:
            self.builder = gtk.Builder()
            self.builder.add_from_file('MastersMonteCarloSimulationWindow.glade')
            self.builder.connect_signals(self)
            self.window = self.builder.get_object('window1')
            
            
            
            container = self.builder.get_object("container")
            
            
            
            # Create opengl configuration
            try:
                # Try creating rgb, double buffering and depth test modes for opengl
                glconfig = gtk.gdkgl.Config(mode=(gtk.gdkgl.MODE_RGB |
                                                  gtk.gdkgl.MODE_DOUBLE |
                                                  gtk.gdkgl.MODE_DEPTH))
            except:
                # Failed, so quit
                sys.exit(0)
            
            self.glarea = gtk.gtkgl.DrawingArea(glconfig)
            self.glarea.set_size_request(600, 400)
            container.pack_start(self.glarea)
            self.glarea.show()
            #PyMOL   = PyMOL(self.glarea)
            import pymol 
            pymol.start()
            cmd = pymol.cmd
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





