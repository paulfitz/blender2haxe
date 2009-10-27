#!BPY 
""" 
Name: 'ActionScript 3.0 Class (.as) ...'
Blender: 240
Group: 'Export'
Tooltip: 'Export geometry to ActionScript 3.0 Class (.as)'
""" 

# --------------------------------------------------------------------------
# ***** BEGIN GPL LICENSE BLOCK *****
#
# Copyright (C) 2007-2008 Dennis Ippel
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
# ***** END GPL LICENCE BLOCK *****
# --------------------------------------------------------------------------

__author__ = "Dennis Ippel"
__url__ = ("http://www.rozengain.com")
__version__ = "0.7"

__bpydoc__ = """

For more information please go to:
http://www.rozengain.com
"""

#triangulate: go into edit mode, select all faces and press ctrl+t
 
from Blender import Scene, Mesh, Window, Get, sys, Image, Draw
import Blender
import BPyMessages 
import bpy 
import math
import os
import inspect
from math import *
from Blender.BGL import *

EVENT_NOEVENT = 1
EVENT_DRAW = 2
EVENT_EXIT = 3
EVENT_EXPORT = 4
EVENT_BROWSEFILE = 5

as_package_name = Draw.Create("")
fileButton = Draw.Create("")
engine_menu = Draw.Create(1)
export_all = None

def get_path():
	return os.path.dirname(inspect.currentframe().f_code.co_filename)

def export_papervision(me, class_name): 
	file_name = "AS3ExpPapervision17.as"
	data_loop = ""
	transform_props = ""
	 
	for v in me.verts: 
		data_loop += "\t\t\tv(%f,%f,%f);\n" % (v.co.x, v.co.y, v.co.z)
	
	data_loop += "\n"
	
	for f in me.faces:
		if me.faceUV:
			data_loop += "\t\t\tf(%i,%i,%i,null,%f,%f,%f,%f,%f,%f,%f,%f,%f);\n" % (f.verts[0].index, f.verts[1].index, f.verts[2].index, f.uv[0][0], f.uv[0][1], f.uv[1][0], f.uv[1][1], f.uv[2][0], f.uv[2][1], f.no.x, f.no.y, f.no.z )
		if not me.faceUV:
			data_loop += "\t\t\tf2(%i,%i,%i);\n" % (f.verts[0].index, f.verts[1].index, f.verts[2].index)
	
	transform_props += "\n\t\t\tx = %f; y = %f; z = %f;\n" % (ob_locX, ob_locY, ob_locZ)
	transform_props += "\n\t\t\trotationX = %f; rotationY = %f; rotationZ = %f;\n" % (ob_rotX, ob_rotY, ob_rotZ)
	transform_props += "\n\t\t\tscaleX = %f; scaleY = %f; scaleZ = %f;\n" % (ob_scaleX, ob_scaleY, ob_scaleZ)

	save_file(file_name, class_name, data_loop, transform_props)

def export_papervision2(me, class_name): 
	file_name = "AS3ExpPapervision20.as"
	data_loop = ""
	transform_props = ""
	
	for v in me.verts: 
		data_loop += "\t\t\tv(%f,%f,%f);\n" % (v.co.x, v.co.y, v.co.z)
	
	data_loop += "\n"
	
	for f in me.faces:
		if me.faceUV:
			data_loop += "\t\t\tf(%i,%i,%i,%f,%f,%f,%f,%f,%f,%f,%f,%f);\n" % (f.verts[0].index, f.verts[1].index, f.verts[2].index, f.uv[0][0], f.uv[0][1], f.uv[1][0], f.uv[1][1], f.uv[2][0], f.uv[2][1], f.no.x, f.no.y, f.no.z )
		if not me.faceUV:
			data_loop += "\t\t\tf2(%i,%i,%i);\n" % (f.verts[0].index, f.verts[1].index, f.verts[2].index)
	
	transform_props += "\n\t\t\tx = %f; y = %f; z = %f;\n" % (ob_locX, ob_locY, ob_locZ)
	transform_props += "\n\t\t\trotationX = %f; rotationY = %f; rotationZ = %f;\n" % (ob_rotX, ob_rotY, ob_rotZ)
	transform_props += "\n\t\t\tscaleX = %f; scaleY = %f; scaleZ = %f;\n" % (ob_scaleX, ob_scaleY, ob_scaleZ)

	save_file(file_name, class_name, data_loop, transform_props)
	
def export_away3d(me, class_name): 
	file_name = "AS3ExpAway3D.as"
	data_loop = ""
	transform_props = ""
	 
	for v in me.verts: 
		data_loop += "\t\t\tv(%f,%f,%f);\n" % (v.co.x, v.co.y, v.co.z)
	
	data_loop += "\n"
	
	for f in me.faces:
		if me.faceUV:
			data_loop += "\t\t\tf(%i,%i,%i,%f,%f,%f,%f,%f,%f,%f,%f,%f);\n" % (f.verts[0].index, f.verts[1].index, f.verts[2].index, f.uv[0][0], f.uv[0][1], f.uv[1][0], f.uv[1][1], f.uv[2][0], f.uv[2][1], f.no.x, f.no.y, f.no.z )
		if not me.faceUV:
			data_loop += "\t\t\tf2(%i,%i,%i);\n" % (f.verts[0].index, f.verts[1].index, f.verts[2].index)
	
	transform_props += "\n\t\t\tx = %f; y = %f; z = %f;\n" % (ob_locX, ob_locY, ob_locZ)
	transform_props += "\n\t\t\trotationX = %f; rotationY = %f; rotationZ = %f;\n" % (ob_rotX, ob_rotY, ob_rotZ)
	transform_props += "\n\t\t\tthis.scaleXYZ(%f, %f, %f);\n" % (ob_scaleX, ob_scaleY, ob_scaleZ)
	
	save_file(file_name, class_name, data_loop, transform_props)

def export_away3d_210(me, class_name): 
	file_name = "AS3ExpAway3D210.as"
	data_loop = ""
	transform_props = ""
	 
	for v in me.verts: 
		data_loop += "\t\t\tv(%f,%f,%f);\n" % (v.co.x, v.co.y, v.co.z)
	
	data_loop += "\n"
	
	for f in me.faces:
		if me.faceUV:
			data_loop += "\t\t\tf(%i,%i,%i,%f,%f,%f,%f,%f,%f,%f,%f,%f);\n" % (f.verts[0].index, f.verts[1].index, f.verts[2].index, f.uv[0][0], f.uv[0][1], f.uv[1][0], f.uv[1][1], f.uv[2][0], f.uv[2][1], f.no.x, f.no.y, f.no.z )
		if not me.faceUV:
			data_loop += "\t\t\tf2(%i,%i,%i);\n" % (f.verts[0].index, f.verts[1].index, f.verts[2].index)
	
	transform_props += "\n\t\t\tx = %f; y = %f; z = %f;\n" % (ob_locX, ob_locY, ob_locZ)
	transform_props += "\n\t\t\trotationX = %f; rotationY = %f; rotationZ = %f;\n" % (ob_rotX, ob_rotY, ob_rotZ)
	transform_props += "\n\t\t\tthis.scaleXYZ(%f, %f, %f);\n" % (ob_scaleX, ob_scaleY, ob_scaleZ)
	
	save_file(file_name, class_name, data_loop, transform_props)

##########################################################################################
# Thanks to Andrea Boschini (Panurge Web Design, http://www.panurge.it)
# for this addition
##########################################################################################
 	
def export_away3d_220(me, class_name): 
	file_name = "AS3ExpAway3D220.as"
	data_loop = ""
	transform_props = ""
	
	for v in me.verts: 
		data_loop += "\t\t\tv(%f,%f,%f);\n" % (v.co.x, v.co.y, v.co.z)
	
	data_loop += "\n"
	
	for f in me.faces:
		if me.faceUV:
			data_loop += "\t\t\tf(%i,%i,%i,%f,%f,%f,%f,%f,%f,%f,%f,%f);\n" % (f.verts[0].index, f.verts[1].index, f.verts[2].index, f.uv[0][0], f.uv[0][1], f.uv[1][0], f.uv[1][1], f.uv[2][0], f.uv[2][1], f.no.x, f.no.y, f.no.z )
		if not me.faceUV:
			data_loop += "\t\t\tf2(%i,%i,%i);\n" % (f.verts[0].index, f.verts[1].index, f.verts[2].index)
	
	transform_props += "\n\t\t\tx = %f; y = %f; z = %f;\n" % (ob_locX, ob_locY, ob_locZ)
	transform_props += "\n\t\t\trotationX = %f; rotationY = %f; rotationZ = %f;\n" % (ob_rotX, ob_rotY, ob_rotZ)
	transform_props += "\n\t\t\tscaleX = %f; scaleY = %f; scaleZ = %f;\n" % (ob_scaleX, ob_scaleY, ob_scaleZ)
	
	save_file(file_name, class_name, data_loop, transform_props)
	
def export_away3d_lite_10(me, class_name): 
	file_name = "AS3ExpAway3DLite.as"
	data_loop = ""
	transform_props = ""

	if me.faceUV:
		for v in me.verts:
			data_loop += "\t\t\tv(%f,%f,%f);\n" % (v.co.x, v.co.y, v.co.z)
	else:
		for v in me.verts:
			data_loop += "\t\t\tv2(%f,%f,%f);\n" % (v.co.x, v.co.y, v.co.z)
			
	for f in me.faces:
		if me.faceUV:
			data_loop += "\t\t\tf(%i,%i,%i,%f,%f,%f,%f,%f,%f);\n" % (f.verts[0].index, f.verts[1].index, f.verts[2].index, f.uv[0][0], f.uv[0][1], f.uv[1][0], f.uv[1][1], f.uv[2][0], f.uv[2][1])
			
		if not me.faceUV:
			data_loop += "\t\t\tf2(%i,%i,%i);\n" % (f.verts[0].index, f.verts[1].index, f.verts[2].index)
		
	transform_props += "\n\t\t\tx = %f; y = %f; z = %f;\n" % (ob_locX, ob_locY, ob_locZ)
	transform_props += "\n\t\t\trotationX = %f; rotationY = %f; rotationZ = %f;\n" % (ob_rotX, ob_rotY, ob_rotZ)
	transform_props += "\n\t\t\tscaleX = %f; scaleY = %f; scaleZ = %f;\n" % (ob_scaleX, ob_scaleY, ob_scaleZ)

	save_file(file_name, class_name, data_loop, transform_props)
	
##########################################################################################
# Thanks to Makc (http://makc3d.wordpress.com/)
# for the quads addition
##########################################################################################

def export_sandy(me, class_name, is_haxe):
	if is_haxe:
		file_name = "HXExpSandy30.hx"
	else:
		file_name = "AS3ExpSandy30.as"
	data_loop = ""
	transform_props = ""
	
	for v in me.verts: 
		data_loop += "\t\t\tv(%f,%f,%f);\n" % (v.co.x, v.co.y, v.co.z)
	data_loop += "\n"
	
	for f in me.faces:
		if me.faceUV:
			if len(f.uv) < 4:
				data_loop += "\t\t\tf(%i,%i,%i,%f,%f,%f,%f,%f,%f,%f,%f,%f);\n" % (f.verts[0].index,f.verts[1].index, f.verts[2].index, f.uv[0][0], f.uv[0][1],f.uv[1][0], f.uv[1][1], f.uv[2][0], f.uv[2][1], f.no.x, f.no.y, f.no.z)
			else:
				data_loop += "\t\t\tf4(%i,%i,%i,%i,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f);\n" % (f.verts[0].index, f.verts[1].index, f.verts[2].index, f.verts[3].index, f.uv[0][0], f.uv[0][1], f.uv[1][0], f.uv[1][1], f.uv[2][0], f.uv[2][1], f.uv[3][0], f.uv[3][1], f.no.x, f.no.y, f.no.z)
		if not me.faceUV:
			if len(f.verts) < 4:
				data_loop += "\t\t\tf2(%i,%i,%i);\n" % (f.verts[0].index, f.verts[1].index, f.verts[2].index)
			else:
				data_loop += "\t\t\tf24(%i,%i,%i,%i);\n" % (f.verts[0].index, f.verts[1].index, f.verts[2].index, f.verts[3].index)	
	
	transform_props += "\n\t\t\tx = %f; y = %f; z = %f;\n" % (ob_locX, ob_locY, ob_locZ)
	transform_props += "\n\t\t\trotateX = %f; rotateY = %f; rotateZ = %f;\n" % (ob_rotX, ob_rotY, ob_rotZ)
	transform_props += "\n\t\t\tscaleX = %f; scaleY = %f; scaleZ = %f;\n" % (ob_scaleX, ob_scaleY, ob_scaleZ)

	save_file(file_name, class_name, data_loop, transform_props, is_haxe)

##########################################################################################
# Alternativa 5.x export (based on Sandy code)
##########################################################################################

def export_alternativa3d(me, class_name):
	file_name = "AS3ExpAlternativa5x.as"
	data_loop = ""
	transform_props = ""

	#generate geometry
	for v in me.verts: 
		data_loop += "\t\t\tv(%f,%f,%f);\n" % (v.co.x, v.co.y, v.co.z)
	
	data_loop += "\n"
	
	for f in me.faces:
		if me.faceUV:
			if len(f.uv) < 4:
				data_loop += "\t\t\tf(%i,%i,%i,%f,%f,%f,%f,%f,%f,%f,%f,%f);\n" % (f.verts[0].index,f.verts[1].index, f.verts[2].index, f.uv[0][0], f.uv[0][1],f.uv[1][0], f.uv[1][1], f.uv[2][0], f.uv[2][1], f.no.x, f.no.y, f.no.z)
			else:
				data_loop += "\t\t\tf4(%i,%i,%i,%i,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f);\n" % (f.verts[0].index, f.verts[1].index, f.verts[2].index, f.verts[3].index, f.uv[0][0], f.uv[0][1], f.uv[1][0], f.uv[1][1], f.uv[2][0], f.uv[2][1], f.uv[3][0], f.uv[3][1], f.no.x, f.no.y, f.no.z)
		if not me.faceUV:
			if len(f.verts) < 4:
				data_loop += "\t\t\tf2(%i,%i,%i);\n" % (f.verts[0].index, f.verts[1].index, f.verts[2].index)
			else:
				data_loop += "\t\t\tf24(%i,%i,%i,%i);\n" % (f.verts[0].index, f.verts[1].index, f.verts[2].index, f.verts[3].index)

	transform_props += "\n\t\t\tx = %f; y = %f; z = %f;\n" % (ob_locX, ob_locY, ob_locZ)
	transform_props += "\n\t\t\trotationX = 0.01745329252 * %f; rotationY = 0.01745329252 * %f; rotationZ = 0.01745329252 * %f;\n" % (ob_rotX, ob_rotY, ob_rotZ)
	transform_props += "\n\t\t\tscaleX = %f; scaleY = %f; scaleZ = %f;\n" % (ob_scaleX, ob_scaleY, ob_scaleZ)
	
	save_file(file_name, class_name, data_loop, transform_props)

def save_file(file_name, class_name, data_loop, transform_props,
	      is_haxe=False):
	try:
		inf = open(get_path()+sys.sep+ "AS3Export" +sys.sep+ file_name, "r")
		ext = ".as"
		if is_haxe:
			ext = ".hx"
		out = open(fileButton.val+""+class_name+ext, 'w')
		try:
			lines = inf.readlines()
			for line in lines:
				line = line.replace("%PACKAGE_NAME%", as_package_name.val)
				line = line.replace("%CLASS_NAME%", class_name)
				line = line.replace("%DATA_LOOP%", data_loop)
				line = line.replace("%TRANSFORM_PROPS%", transform_props)
				out.write(line)
		finally:
			out.close()
			inf.close()
			print "Export Successful: "+class_name+ext
	except:
		Draw.PupMenu("Export failed | Check the console for more info")
		raise # throw the exception

	Draw.Exit()
	
def main(): 
	# Saves the editmode state and go's out of  
	# editmode if its enabled, we cant make 
	# changes to the mesh data while in editmode. 
	is_editmode = Window.EditMode() 
	if is_editmode: Window.EditMode(0) 
	 
	Window.WaitCursor(1) 
	t = sys.time() 
	
	# Restore editmode if it was enabled 
	if is_editmode: Window.EditMode(1) 
	 
	print 'ActionScript 3.0 Exporter Script finished in %.2f seconds' % (sys.time()-t) 
	Window.WaitCursor(0) 

# This lets you can import the script without running it 
if __name__ == '__main__': 
	main() 

def event(evt, val):
	if (evt == Draw.QKEY and not val):
		Draw.Exit()

def bevent(evt):
	global EVENT_NOEVENT,EVENT_DRAW,EVENT_EXIT
	
	if (evt == EVENT_EXIT):
		Draw.Exit()
	elif (evt== EVENT_DRAW):
		Draw.Redraw()
	elif (evt== EVENT_EXPORT):
		sce = bpy.data.scenes.active 
		
		obs = None
		
		if(export_all == 1):
			# export all scene objects
			obs = [ob for ob in sce.objects if ob.type == 'Mesh']
		else:
			# export the selected objects
			obs = [ob for ob in sce.objects.selected if ob.type == 'Mesh']
		
		if (len(obs) == 0):
			Draw.PupMenu("Nothing to export. Please select a Mesh.")
			Draw.Exit()
			return
			
		# export all object names
		for ob in obs:
			me = Mesh.New()
			me.getFromObject(ob,0)
			print(me.name)
			export_to_as(ob)
		
		Draw.PupMenu("Export Successful")

	elif (evt== EVENT_BROWSEFILE):
		Window.FileSelector(FileSelected,"Export .as", expFileName)
		Draw.Redraw(1)

def export_to_as(ob):
	me = Mesh.New()
	me.getFromObject(ob,0)
	
	class_name = ob.name.replace(".", "")
	
	#get transformations
	global ob_locX, ob_locY, ob_locZ, ob_mtrx, ob_rotX, ob_rotY, ob_rotZ, ob_scaleX, ob_scaleY, ob_scaleZ
	ob_locX = ob.LocX
	ob_locY = ob.LocY
	ob_locZ = ob.LocZ
	ob_mtrx = ob.matrix.rotationPart()
	ob_rotX = ob.RotX * (180 / pi)
	ob_rotY = ob.RotY * (180 / pi)
	ob_rotZ = ob.RotZ * (180 / pi)
	ob_scaleX = ob.SizeX
	ob_scaleY = ob.SizeY
	ob_scaleZ = ob.SizeZ	
	
	if (engine_menu.val == 2):
		export_papervision(me, class_name) 
	elif (engine_menu.val == 3 ):
		export_papervision2(me, class_name)
	elif (engine_menu.val == 4 ):
		export_sandy(me, class_name, False)
	elif (engine_menu.val == 41 ):
		export_sandy(me, class_name, True)
	elif (engine_menu.val == 7 ):
		export_alternativa3d(me, class_name)
	elif (engine_menu.val == 1 ):
		export_away3d(me, class_name)
	elif (engine_menu.val == 5 ):
		export_away3d_210(me, class_name)	
	elif (engine_menu.val == 6 ):
		export_away3d_220(me, class_name)		
	elif (engine_menu.val == 8 ):
		export_away3d_lite_10(me, class_name)		
		
def FileSelected(fileName):
	global fileButton
	
	if fileName != '':
		# check if file exists
		#if sys.exists(fileName) != 1:
		#	cutils.Debug.Debug('File(%s) does not exist' % (fileName),'ERROR')
		#	return False
		
		fileButton.val = fileName
	else:
		cutils.Debug.Debug('ERROR: filename is empty','ERROR')

######################################################
# GUI drawing
######################################################
def draw():
	global as_package_name
	global fileButton, expFileName
	global engine_menu, engine_name
	global EVENT_NOEVENT,EVENT_DRAW,EVENT_EXIT,EVENT_EXPORT
	global export_all
	expFileName = ""
	########## Titles
	glClear(GL_COLOR_BUFFER_BIT)
	glRasterPos2i(40, 240)

	logoImage = Image.Load(get_path()+sys.sep+'AS3Export'+sys.sep+'AS3Export.png')
	Draw.Image(logoImage, 40, 155)
	
	as_package_name = Draw.String("Package name: ", EVENT_NOEVENT, 40, 130, 250, 20, as_package_name.val, 300)
	engine_name = "Alternativa3D 5.x%x7|Away3D%x1|Away3D 2.1.0%x5|Away3D 2.2, 2.3, 2.4, 3.4%x6|Away3D Lite Version 1.0%x8|Papervision3D%x2|Papervision3D 2.0%x3|Sandy 3.0%x4|Sandy Haxe 3.0%x41"
	engine_menu = Draw.Menu(engine_name, EVENT_NOEVENT, 40, 100, 200, 20, engine_menu.val, "Choose your engine")

	fileButton = Draw.String('File location: ', EVENT_NOEVENT, 40, 70, 250, 20, fileButton.val, 255) 
	Draw.PushButton('...', EVENT_BROWSEFILE, 300, 70, 30, 20, 'browse file')
	export_all = Draw.Toggle('Export ALL scene objects', EVENT_NOEVENT, 40, 45, 200, 20, 0)
	######### Draw and Exit Buttons
	Draw.Button("Export",EVENT_EXPORT , 40, 20, 80, 18)
	Draw.Button("Exit",EVENT_EXIT , 140, 20, 80, 18)

Draw.Register(draw, event, bevent)
