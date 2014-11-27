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


class NewProjectDialog():
    def __init__(self, project=None, window_control=None, main_builder=None):
        
        """ Class initialiser """
        self.project = project
        self.window_control = window_control
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
        
        #self.window_control = WindowControl(self.builder)

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

