#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  BoxSetupDialog.py
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

import os, sys
import gtk
import gtk.gtkgl

import gobject
from pymol import cmd
from WindowControl import *

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
    if glarea.window:
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

#def context_menu():
#    builder = masters.builder
#    menu = builder.get_object('GLArea_menu')
#    return menu

# Create opengl configuration

# Try creating rgb, double buffering and depth test modes for opengl
glconfig = gtk.gdkgl.Config(mode=(gtk.gdkgl.MODE_RGB |
                                  gtk.gdkgl.MODE_DOUBLE |
                                  gtk.gdkgl.MODE_DEPTH))







class BoxSetupDialog:
    """ Class doc """

    def on_spinbutton_change_value(self, widget, event):
        """ Function doc """
        print 'teste'
        self.DrawCell()
    
    def on_spinbutton_change_value2(self, widget, event= None):
        """ Function doc """
        print 'teste2'
        
        self.DrawCell()

    def DrawCell (self):
        #pass
        #""" Function doc """
        
        selection="(all)"
        padding=0.0
        linewidth=2.0
        r=1.0
        g=1.0
        b=1.0
        
        minX  = self.builder.get_object("spinbutton_minX").get_value_as_int()
        minY  = self.builder.get_object("spinbutton_minY").get_value_as_int()
        minZ  = self.builder.get_object("spinbutton_minZ").get_value_as_int()
        maxX  = self.builder.get_object("spinbutton_maxX").get_value_as_int()
        maxY  = self.builder.get_object("spinbutton_maxY").get_value_as_int()
        maxZ  = self.builder.get_object("spinbutton_maxZ").get_value_as_int()
        
        #minX = self.minX
        #minY = self.minY
        #minZ = self.minZ
        #maxX = self.maxX
        #maxY = self.maxY
        #maxZ = self.maxZ
        

        boundingBox = [
                LINEWIDTH, float(linewidth),

                BEGIN, LINES,
                COLOR, float(r), float(g), float(b),

                VERTEX, minX, minY, minZ,       #1
                VERTEX, minX, minY, maxZ,       #2

                VERTEX, minX, maxY, minZ,       #3
                VERTEX, minX, maxY, maxZ,       #4

                VERTEX, maxX, minY, minZ,       #5
                VERTEX, maxX, minY, maxZ,       #6

                VERTEX, maxX, maxY, minZ,       #7
                VERTEX, maxX, maxY, maxZ,       #8


                VERTEX, minX, minY, minZ,       #1
                VERTEX, maxX, minY, minZ,       #5

                VERTEX, minX, maxY, minZ,       #3
                VERTEX, maxX, maxY, minZ,       #7

                VERTEX, minX, maxY, maxZ,       #4
                VERTEX, maxX, maxY, maxZ,       #8

                VERTEX, minX, minY, maxZ,       #2
                VERTEX, maxX, minY, maxZ,       #6


                VERTEX, minX, minY, minZ,       #1
                VERTEX, minX, maxY, minZ,       #3

                VERTEX, maxX, minY, minZ,       #5
                VERTEX, maxX, maxY, minZ,       #7

                VERTEX, minX, minY, maxZ,       #2
                VERTEX, minX, maxY, maxZ,       #4

                VERTEX, maxX, minY, maxZ,       #6
                VERTEX, maxX, maxY, maxZ,       #8

                END
        ]
        
        try:
            cmd.delete("box_1")
        except:
            pass
        
        boxName = "box_1"
        cmd.set('auto_zoom', 0)
        cmd.load_cgo(boundingBox,boxName)
        #cmd.set_frame(-1)
    
    def on_TrajectoryTool_Entry_Push(self, entry, data=None):
		MAX  = int(self.builder.get_object('trajectory_max_entrey').get_text())
		MIN  = int(self.builder.get_object('trajectory_min_entrey').get_text())

		scale = self.builder.get_object("trajectory_hscale")
		scale.set_range(MIN, MAX)
		scale.set_increments(1, 10)
		scale.set_digits(0)	

    def on_TrajectoryTool_BarSetFrame(self, hscale, text= None,  data=None):            # SETUP  trajectory window
        valor = hscale.get_value()
        cmd.frame( int (valor) )
        #BondTable = self.project.BondTable

    
    
    
    def on_window1_delete_event (self,widget, data=None):
        """ Function doc """
        print 'on_window1_delete_event'
        print dir(gtk)#.quit()
    
    def on_window1_destroy_event(self,widget, data=None):
        """ Function doc """
        print 'on_window1_destroy_event'
        

    
    def __init__(self, project=None, window_control=None, main_builder=None, filein = None):
        """ Class initialiser """
        self.project = project
        self.window_control = window_control
        #self.builder = gtk.Builder()
        #self.main_builder = main_builder


        #---------------------------------- MasterGUI ------------------------------------#
        self.builder = gtk.Builder()                                                      #
        self.builder.add_from_file("MastersBOXSetup.glade")                               #
        self.win     = self.builder.get_object("window1")                                 #
        self.win.show()                                                                   #
        self.builder.connect_signals(self)                                                #
        #self.statusbar = builder.get_object("statusbar")
        #---------------------------------------------------------------------------------#


        #self.builder.add_from_file('MastersBOXSetup.glade')
        #self.dialog = self.builder.get_object('dialog1')
        #self.builder.connect_signals(self)

        '''
		--------------------------------------------------
		-                                                -
		-	              WindowControl                  -
		-                                                -
		--------------------------------------------------
		'''
        
        
        if project == None:
            project= {'Cell' : {'minX' : -10.0,
                                'minY' : -10.0,
                                'minZ' : -10.0,
                                'maxX' :  10.0,
                                'maxY' :  10.0,
                                'maxZ' :  10.0}
                                }
        
        self.minX = project['Cell']['minX']
        self.minY = project['Cell']['minY']
        self.minZ = project['Cell']['minZ']
        self.maxX = project['Cell']['maxX']
        self.maxY = project['Cell']['maxY']
        self.maxZ = project['Cell']['maxZ']
        
        print self.minX
        print self.minY
        print self.minZ
        print self.maxX
        print self.maxY
        print self.maxZ
        




        #-------------------- config PyMOL ---------------------#
                                                                #
        container = self.builder.get_object("container")        #
        pymol.start()                                           #
        cmd = pymol.cmd                                         #
        container.pack_start(glarea)                            #
        glarea.show()                                           #
                                                                #
        #-------------------------------------------------------#

        
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
        #cmd.bg_color("grey")            # background color     #
        cmd.do("set field_of_view, 70")                         #
        cmd.do("set ray_shadows,off")                           #
                                                                #
                                                                #
                                                                #
        
        cmd.set('ribbon_sampling', 3)                           #
        self.DrawCell()
        
        if filein == None:
            cmd.load('/home/labio/Documents/mastersGUI/MastersGUI/test/1AGT.pdb')
        else:
            cmd.load(filein)                            #
        
        cmd.show("spheres")                                     #
        cmd.hide('lines')
        cmd.show('ribbon')                                      #
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
        
        adjustment1 = gtk.Adjustment(0.0, -1000.0, 1000.0, 1.0, 0.0, 0.0)
        self.spinbutton_minX  = self.builder.get_object("spinbutton_minX")
        self.spinbutton_minX.set_adjustment(adjustment1)
        self.spinbutton_minX.update()
        self.spinbutton_minX.set_value(int(project['Cell']['minX']))

        adjustment2 = gtk.Adjustment(0.0, -1000.0, 1000.0, 1.0, 0.0, 0.0)
        self.spinbutton_minY  = self.builder.get_object("spinbutton_minY")
        self.spinbutton_minY.set_adjustment(adjustment2)
        self.spinbutton_minY.update()
        self.spinbutton_minY.set_value(int(project['Cell']['minY']))

        adjustment3 = gtk.Adjustment(0.0, -1000.0, 1000.0, 1.0, 0.0, 0.0)
        self.spinbutton_minZ  = self.builder.get_object("spinbutton_minZ")
        self.spinbutton_minZ.set_adjustment(adjustment3)
        self.spinbutton_minZ.update()
        self.spinbutton_minZ.set_value(int(project['Cell']['minZ']))
        
        adjustment4 = gtk.Adjustment(0.0, -1000.0, 1000.0, 1.0, 0.0, 0.0)
        self.spinbutton_maxX  = self.builder.get_object("spinbutton_maxX")
        self.spinbutton_maxX.set_adjustment(adjustment4)
        self.spinbutton_maxX.update()
        self.spinbutton_maxX.set_value(int(project['Cell']['maxX']))

        adjustment5 = gtk.Adjustment(0.0, -1000.0, 1000.0, 1.0, 0.0, 0.0)
        self.spinbutton_maxY  = self.builder.get_object("spinbutton_maxY")
        self.spinbutton_maxY.set_adjustment(adjustment5)
        self.spinbutton_maxY.update()
        self.spinbutton_maxY.set_value(int(project['Cell']['maxY']))

        adjustment6 = gtk.Adjustment(0.0, -1000.0, 1000.0, 1.0, 0.0, 0.0)
        self.spinbutton_maxZ  = self.builder.get_object("spinbutton_maxZ")
        self.spinbutton_maxZ.set_adjustment(adjustment6)
        self.spinbutton_maxZ.update()
        self.spinbutton_maxZ.set_value(int(project['Cell']['maxZ'])) 
        
        self.DrawCell()
        
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
#masters = MastersMain()
#glarea.connect_object("button_release_event", show_context_menu, context_menu())
#masters.run()








def main():
    dialog = BoxSetupDialog()
    dialog.run()

if __name__ == '__main__':
    main()



