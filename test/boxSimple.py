#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  boxSimple.py
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



#print "Box dimensions (%.2f, %.2f, %.2f)" % (maxX-minX, maxY-minY, maxZ-minZ)
#
#minX = minX - float(padding)
#minY = minY - float(padding)
#minZ = minZ - float(padding)
#maxX = maxX + float(padding)
#maxY = maxY + float(padding)
#maxZ = maxZ + float(padding)

selection="(all)"
padding=0.0
linewidth=2.0
r=1.0
g=1.0
b=1.0

minX = -10.0
minY = -10.0
minZ = -10.0
maxX =  10.0
maxY =  10.0
maxZ =  10.0


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

boxName = "box_1"
cmd.load_cgo(boundingBox,boxName)
