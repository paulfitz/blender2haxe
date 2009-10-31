#!BPY 
""" 
Name: 'Haxe Class (.hx) ...'
Blender: 240
Group: 'Export'
Tooltip: 'Export geometry to Haxe Class (.hx)'
""" 

# --------------------------------------------------------------------------
# ***** BEGIN GPL LICENSE BLOCK *****
#
# Copyright (C) 2009 Paul Fitzpatrick
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


# --------------------------------------------------------------------------
# Information about this script for Blender

__author__ = "Paul Fitzpatrick"
__url__ = ("http://live.makesweet.com")
__version__ = "0.1"

__bpydoc__ = """

Based on AS3Export by Dennis Ippel.
"""


# --------------------------------------------------------------------------
# Imports.
#
# Import jinja2 for templates.
# Not sure exactly how best to do this in a Blender python script.
# Even just finding the current path was a little dicey, __file__ is
# not available.
import os
import sys
def get_path():
    try:
        p = os.path.dirname(__file__)
    except:
        import inspect
        p = os.path.dirname(inspect.currentframe().f_code.co_filename)
    p = os.path.abspath(p)
    return p
sys.path.append(get_path())
from jinja2 import Environment, FileSystemLoader, TemplateNotFound
template_dirs = []
template_dirs.append(get_path()+"/"+ "template")
env = Environment(loader = FileSystemLoader(template_dirs))

from Blender import Scene, Mesh, Window, Get, sys, Image, Draw
from Blender import Registry, Camera, Object
import Blender
import BPyMessages 
import bpy 
import math
from math import *
from Blender.BGL import *


# --------------------------------------------------------------------------
# Store defaults in Blender

reg_key = "HXExport"

def update_registry():
    global as_package_name
    global fileButton
    global export_all_button
    global export_test_button
    d = {}
    d['package_name'] = as_package_name.val
    d['file_location'] = fileButton.val
    d['export_all'] = export_all_button.val
    d['export_test'] = export_test_button.val
    Blender.Registry.SetKey(reg_key, d, True)

rdict = Registry.GetKey(reg_key, True)
got = False
if rdict:
    try:
        package_name = rdict['package_name']
	file_location = rdict['file_location']
	export_all = rdict['export_all']
	export_test = rdict['export_test']
	got = True
    except:
        got = False
	pass
if not(got):
    package_name = ""
    menu_selection = 1
    file_location = ""
    export_all = 0
    export_test = 0

as_package_name = Draw.Create(package_name)
fileButton = Draw.Create(file_location)
export_all_button = Draw.Create(export_all)
export_test_button = Draw.Create(export_test)
update_registry()


# --------------------------------------------------------------------------
# Generate HX files.

def render(template_name, variables):
    try:
	template = env.get_template(template_name)
    except TemplateNotFound:
	raise TemplateNotFound(template_name)
    content = template.render(variables)
    return content


def export_sandy(class_name, tvars):
	file_name = "HXExpSandy30.hx"
	test_file_name = "HXExpSandy30_main.hx"
	build_file_name = "HXExpSandy30_main.hxml"

	tvars['pi'] = pi
	tvars['TESTED_CLASS_NAME'] = class_name

	save_file(file_name, class_name, None, tvars)

	if test_file_name and build_file_name and export_test_button.val:
		save_file(test_file_name,
			  class_name + "Main",
			  None,
			  tvars)
		save_file(build_file_name,
			  class_name + "Main",
			  class_name + ".hxml",
			  tvars)


def save_file(file_name,class_name,output_file_name,tvars):
	success = False
	tvars['PACKAGE_NAME'] = as_package_name.val
	tvars['CLASS_NAME'] = class_name
	template_name = get_path()+sys.sep+ "template" +sys.sep+ file_name
	inf = open(template_name, "r")
	
	ext = ".hx"
	if not(output_file_name):
		output_file_name = class_name+ext
	reported_name = output_file_name
	output_file_name = fileButton.val+""+output_file_name
	out = open(output_file_name, 'w')
	x = render(file_name,tvars)
	out.write(x)
	out.close()
	inf.close()
	print "Export Successful: "+reported_name


def export_to_hx(ob):
	me = Mesh.New()
	me.getFromObject(ob,0)
	
	class_name = ob.name.replace(".","").replace("-","")

	cam = None
	cam_geom = None
	cam_loc = [0,0,0]
	if export_test_button.val == 1:
		cams = Camera.Get()
		if len(cams)>0:
			cam = cams[0]
			cam_geom = Object.Get(cam.name)
			print("Using camera: " + cam.name)

	tvars = { 'mesh': me,
		  'object': ob,
		  'camera': cam,
		  'camera_geom': cam_geom }
	
	export_sandy(class_name,tvars)


def export_list(obs):
	for ob in obs:
		me = Mesh.New()
		me.getFromObject(ob,0)
		print(me.name)
		export_to_hx(ob)	

# --------------------------------------------------------------------------
# Generate HX files.

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



# --------------------------------------------------------------------------
# GUI stuff.

EVENT_NOEVENT = 1
EVENT_DRAW = 2
EVENT_EXIT = 3
EVENT_EXPORT = 4
EVENT_BROWSEFILE = 5

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
		update_registry()
		sce = bpy.data.scenes.active 
		
		obs = None
		
		if(export_all_button.val == 1):
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
		try:
			export_list(obs)
			Draw.PupMenu("Export Successful")
		except:
			Draw.PupMenu("Export failed | Check the console for more info")
		Draw.Exit()

	elif (evt== EVENT_BROWSEFILE):
		Window.FileSelector(FileSelected,"Export .as", expFileName)
		Draw.Redraw(1)

		
def FileSelected(fileName):
	global fileButton
	
	if fileName != '':
		fileButton.val = fileName
	else:
		cutils.Debug.Debug('ERROR: filename is empty','ERROR')

def draw():
	global as_package_name
	global fileButton, expFileName
	global engine_menu, engine_name
	global EVENT_NOEVENT,EVENT_DRAW,EVENT_EXIT,EVENT_EXPORT
	global export_all_button
	global export_test_button
	global export_all
	global export_test
	expFileName = ""
	########## Titles
	glClear(GL_COLOR_BUFFER_BIT)
	glRasterPos2i(40, 240)

	as_package_name = Draw.String("Package name: ", EVENT_NOEVENT, 40, 130, 250, 20, as_package_name.val, 300)

	fileButton = Draw.String('File location: ', EVENT_NOEVENT, 40, 70, 250, 20, fileButton.val, 255) 
	Draw.PushButton('...', EVENT_BROWSEFILE, 300, 70, 30, 20, 'browse file')
	export_all_button = Draw.Toggle('Export ALL scene objects', EVENT_NOEVENT, 40, 45, 200, 20, export_all_button.val)
	export_test_button = Draw.Toggle('Export test code for object(s)', EVENT_NOEVENT, 250, 45, 200, 20, export_test_button.val)
	######### Draw and Exit Buttons
	Draw.Button("Export",EVENT_EXPORT , 40, 20, 80, 18)
	Draw.Button("Exit",EVENT_EXIT , 140, 20, 80, 18)

if Blender.mode == 'interactive':
	Draw.Register(draw, event, bevent)
else:
	print("Command-line mode operation, exporting all objects")
	sce = bpy.data.scenes.active 
	obs = [ob for ob in sce.objects if ob.type == 'Mesh']
	export_list(obs)
