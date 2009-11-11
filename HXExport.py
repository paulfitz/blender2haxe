#!BPY 
""" 
Name: 'Haxe Class (.hx) ...'
Blender: 244
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
__url__ = ("http://github.com/paulfitz/blender2haxe")
__version__ = "0.1"

__bpydoc__ = """

Based on AS3Export by Dennis Ippel.
"""


# --------------------------------------------------------------------------
# Imports.
#
# Import jinja2 for templates.
# Finding the current path was a little dicey, __file__ is not available
# when used within the GUI.
import os
import sys
def get_path():
    import inspect
    f = inspect.currentframe().f_code.co_filename
    p = os.path.abspath(os.path.dirname(f))
    f = os.path.join(p,f)
    if not(os.path.isfile(f)):
        import blender2haxe
        f = inspect.getfile(blender2haxe)
        p = os.path.abspath(os.path.dirname(f))
    return p
sys.path.append(get_path())
from jinja2 import Environment, FileSystemLoader, TemplateNotFound
template_dirs = []
template_dirs.append(get_path()+"/"+ "template")
env = Environment(loader = FileSystemLoader(template_dirs))

from Blender import Scene, Mesh, Window, Get, sys, Image, Draw
from Blender import Registry, Camera, Object
import Blender
import math
import copy
import re
from math import *
from Blender.BGL import *

# --------------------------------------------------------------------------
# Store defaults in Blender

reg_key = "HXExport5"

def update_registry():
    global hx_package_name
    global fileButton
    global export_all_button
    global export_test_button
    d = {}
    d['package_name'] = hx_package_name.val
    d['file_location'] = fileButton.val
    d['export_all'] = export_all_button.val
    d['export_test'] = export_test_button.val
    d['auto_skin'] = auto_skin_button.val
    Blender.Registry.SetKey(reg_key, d, True)

rdict = Registry.GetKey(reg_key, True)
got = False
if rdict:
    try:
        package_name = rdict['package_name']
	file_location = rdict['file_location']
	export_all = rdict['export_all']
	export_test = rdict['export_test']
	auto_skin = rdict['auto_skin']
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
    auto_skin = 0

hx_package_name = Draw.Create(package_name)
fileButton = Draw.Create(file_location)
export_all_button = Draw.Create(export_all)
export_test_button = Draw.Create(export_test)
auto_skin_button = Draw.Create(auto_skin)
update_registry()


# --------------------------------------------------------------------------
# Generate HX files.

class HxOptions:
	def __init__(self, output_dir, base_dir, include_tests, auto_skin,
		     package_name):
		self.output_dir = output_dir
                self.base_dir = base_dir
                self.include_tests = include_tests
		self.auto_skin = auto_skin
		self.package_name = package_name

def render(template_name, variables):
    try:
	template = env.get_template(template_name)
    except TemplateNotFound:
	raise TemplateNotFound(template_name)
    content = template.render(variables)
    return content


def generate_files(class_name,has_texture,tvars,options):
	file_name = "HXExpSandy30.hx"
	test_file_name = "HXExpSandy30_main.hx"
	build_file_name = "HXExpSandy30_main.hxml"
	make_file_name = "HXExpSandy30_Makefile"
	res_file_name = "HXExpSandy30.xml"

	tvars['pi'] = pi
        tvars['TARGET_NAME'] = class_name
        tvars['HAS_TEXTURE'] = has_texture

        # make basic model .hx file
        if 'mesh' in tvars:
            save_file(file_name, class_name, None, tvars, options,True)
            full = False
        else:
            full = True

	if options.include_tests:
                # make test .hx file
		save_file(test_file_name,
			  class_name + "Main",
			  None,
			  tvars,
			  options,
			  False)

                # make haxe project file for compiling test
		save_file(build_file_name,
			  class_name + "Main",
			  class_name + ".hxml",
			  tvars,
			  options,
			  False)

                # make swfmill project file for generating texture
                if has_texture:
                    save_file(res_file_name,
                              class_name + "Main",
                              class_name + "Skin.xml",
                              tvars,
                              options,
			      False)

                # make Makefile for running haxe and swfmill if needed
                mname = "Makefile"
                if not(full):
                        mname = class_name + "_" + mname
 		save_file(make_file_name,
			  class_name + "Main",
                          mname,
			  tvars,
			  options,
			  False)


def export_sandy(tested_classes, tvars, options):
        tvars['TESTED_CLASSES'] = tested_classes
        if len(tested_classes)==1:
            c = tested_classes[0]
            generate_files(c['name'],c['has_texture'],tvars,options)
            return
        any_texture = False
        for c in tested_classes:
            if c['has_texture']:
                any_texture = True
        fname = "All"
        if 'hint' in tvars:
            fname = tvars['hint']
        generate_files(fname,any_texture,tvars,options)

def save_file(file_name,class_name,output_file_name,tvars,options,packaged):
	success = False
	pname = options.package_name
	if pname != "":
		tvars['PACKAGE_NAME'] = pname
		tvars['PACKAGE_NAME_DOT'] = pname + "."
		tvars['PACKAGE_NAME_SLASH'] = pname + "/"
	else:
		tvars['PACKAGE_NAME'] = ""
		tvars['PACKAGE_NAME_DOT'] = ""
		tvars['PACKAGE_NAME_SLASH'] = ""
		
	tvars['CLASS_NAME'] = class_name
	template_name = get_path()+sys.sep+ "template" +sys.sep+ file_name
	inf = open(template_name, "r")
	
	ext = ".hx"
	if not(output_file_name):
		output_file_name = class_name+ext
	reported_name = output_file_name

	out_dir = options.output_dir
	if packaged and pname!="":
		out_dir = os.path.join(out_dir,pname)
                reported_name = os.path.join(pname,reported_name)
			
	if not(os.path.exists(out_dir)):
            os.makedirs(out_dir)

	output_file_name = os.path.join(out_dir,output_file_name)
	out = open(output_file_name, 'w')
	x = render(file_name,tvars)
	out.write(x)
	out.close()
	inf.close()
	print "+ "+output_file_name

def convert_image(src,dest):
        try:
            import ImageFile
            fp = open(img.filename, "rb")
            p = ImageFile.Parser()
            while True:
                s = fp.read(1024)
                if not s:
                    break
                p.feed(s)
            im = p.close()
            im.save(file_base + ".png")
        except:
            import subprocess
            subprocess.call(['convert', '-quiet', "tga:" + src, dest],
			    stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            if not(os.path.exists(dest)):
                subprocess.call(['convert', '-quiet', src, dest],
				stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            if not(os.path.exists(dest)):
		    print "= FAILED to create: "+dest

def haxeClassNamify(fname):
        fname = re.sub(r"[^a-zA-Z0-9]",r"",fname)
        fname = fname.capitalize()
        return fname

def hintName():
	fname = os.path.split(Blender.Get('filename'))[1]
        fname = fname.replace(".blend","")
        return haxeClassNamify(fname)


def export_to_hx(ob,options,cam,cam_geom):
        has_texture = False
	me = Mesh.New()
	me.getFromObject(ob,0)

        if not(me.faceUV) and auto_skin:
            # try auto unwrapping
            print("Trying unwrapping and baking to produce skin image")
            try:
                sce = Blender.Scene.GetCurrent()
                for o in sce.objects:
                    ob.select(0)
                import unwrap.uvcalc_smart_project
                me = ob.getData(mesh=1)
                img = Blender.Image.New("bake.tga",512,512,24)
                img.filename = "bake.tga"
                for f in me.faces:
                    f.image = img
                me.update()
                unwrap.uvcalc_smart_project.uvcalc_main([ob])
                me.update()
                context = sce.getRenderingContext()
                context.bakeMode = Blender.Scene.Render.BakeModes['TEXTURE']
		context.enableOversampling(0)
		context.enableMotionBlur(0)
		context.enableShadow(0)
		context.enableEnvironmentMap(0)
		context.enableRayTracing(0)
		context.enableRadiosityRender(0)
		context.enablePanorama(0)
		context.enableFieldRendering(0)
		context.gaussFilterSize(0.5)
		context.setRenderWinSize(25)
                ob.select(1)
                context.bake()
                ob.select(0)
            except e:
                print "Unwrapping and baking didn't work out, skipping"
		print "Problem:", e

        me = Mesh.New()
	me.getFromObject(ob,0)
	
	class_name = haxeClassNamify(ob.name)

        if not(os.path.exists(options.output_dir)):
            os.makedirs(options.output_dir)

	tvars = { 'mesh': me,
		  'object': ob,
		  'camera': cam,
		  'camera_geom': cam_geom }
	
        images = dict()
            
        if me.faceUV:
            for f in me.faces:
                if f.image!=None:
                    images[f.image.getName()] = 1
        images = images.keys()
        if len(images)==0:
            print("= No UV image found")
        else:
            if len(images)>1:
                print("= Too many images on object")
            else:
                # perfect, one image, we can deal with that
                img = Blender.Image.Get(images[0])
                print("= Processing UV image "+img.filename)

                original_name = img.filename
                file_base = os.path.join(options.output_dir,class_name)
                img.filename = file_base + ".unknown.format"
                new_name = img.filename
                    
                try:
                    try:
                        img.save()
                    except:
                        # give Blender a chance to scan for image
                        img.filename = os.path.join(options.base_dir,os.path.split(original_name)[1])
                        print("= Attempting to load image from " +
                              str(img.filename))
                        img.reload()
                        print("= Got image of dimensions " + str(img.size))
                        img.filename = new_name
                        img.save()
                    convert_image(img.filename,file_base+".png")
                    print("= Saved converted image to " + file_base + ".png")
                    os.remove(img.filename)
                    has_texture = True
                except:
                    print "No image available - perhaps it was not packed?"
                    print "Omitting texture."
                img.filename = original_name

        rec = {'name':class_name, 'has_texture':has_texture}
        print("= Generating files")
	export_sandy([rec],tvars,options)
        return rec
                

def export_list(obs,options):
        print("================================================")
	cam = None
	cam_geom = None
	cam_loc = [0,0,0]
	if options.include_tests == 1:
		cams = Camera.Get()
		if len(cams)>0:
			cam = cams[0]
			cam_geom = Object.Get(cam.name)
			print("= Using camera: " + cam.name)

        recs = []
	for ob in obs:
		me = Mesh.New()
		me.getFromObject(ob,0)
		print("================================================")
		print("= Working on object " + ob.name)
		sce = Blender.Scene.GetCurrent()
                vis = list(set(sce.getLayers())&set(ob.layers))
                if len(vis)>0:
                    print("= Visible on layers: " + str(vis))
                    rec = export_to_hx(ob,options,cam,cam_geom)
                    recs.append(rec)
                else:
                    print("= Ignoring object, it is not visible")
        if len(recs)>=1:
            hint = "All" + hintName()
            need_check = True
            while need_check:
                need_check = False
                for r in recs:
                    if hint == r['name']:
                        hint = "All" + hint
                        need_check = True
                        break
            
            # make test code for all objects together
            print("= Generating group file")
            export_sandy(recs,{'camera':cam,'camera_geom':cam_geom,
                               'hint': hint},options)

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
		sce = Blender.Scene.GetCurrent()
		
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
			
		# export all object 
		try:
			options = HxOptions(fileButton.val,
                                            fileButton.val,
					    export_test_button.val,
					    auto_skin_button.val,
					    hx_package_name.val)
			export_list(obs,options)
			Draw.PupMenu("Export Successful")
		except:
			Draw.PupMenu("Export failed | Check the console for more info")
		Draw.Exit()

	elif (evt== EVENT_BROWSEFILE):
		Window.FileSelector(FileSelected,"Export .hx", expFileName)
		Draw.Redraw(1)

		
def FileSelected(fileName):
	global fileButton
	
	if fileName != '':
		fileButton.val = fileName
	else:
		cutils.Debug.Debug('ERROR: filename is empty','ERROR')

def draw():
	global hx_package_name
	global fileButton, expFileName
	global engine_menu, engine_name
	global EVENT_NOEVENT,EVENT_DRAW,EVENT_EXIT,EVENT_EXPORT
	global export_all_button
	global export_test_button
	global auto_skin_button
	global export_all
	global export_test
	global auto_skin
	expFileName = ""
	########## Titles
	glClear(GL_COLOR_BUFFER_BIT)
	glRasterPos2i(40, 240)

	hx_package_name = Draw.String("Package name: ", EVENT_NOEVENT, 40, 130, 250, 20, hx_package_name.val, 300)

	fileButton = Draw.String('File location: ', EVENT_NOEVENT, 40, 100, 250, 20, fileButton.val, 255) 
	Draw.PushButton('...', EVENT_BROWSEFILE, 300, 100, 30, 20, 'browse file')
	export_all_button = Draw.Toggle('Export ALL objects', EVENT_NOEVENT, 40, 70, 200, 20, export_all_button.val)
	export_test_button = Draw.Toggle('Export example project', EVENT_NOEVENT, 250, 70, 200, 20, export_test_button.val)
	auto_skin_button = Draw.Toggle('Generate UV map if needed', EVENT_NOEVENT, 40, 45, 200, 20, auto_skin_button.val)
	######### Draw and Exit Buttons
	Draw.Button("Export",EVENT_EXPORT , 40, 20, 80, 18)
	Draw.Button("Exit",EVENT_EXIT , 140, 20, 80, 18)

if Blender.mode == 'interactive':
	Draw.Register(draw, event, bevent)
else:
	print("Command-line mode operation, exporting all mesh objects")

	sce = Blender.Scene.GetCurrent()
	obs = [ob for ob in sce.objects if (ob.type in 'Mesh')]
	#obs = [ob for ob in sce.objects if (ob.type in ['Mesh','Curve','Surf','MBall','Font'])]

        try:
            out_dir = os.environ['BLENDER2HAXE_DIR']
        except:
            out_dir = "Haxe"
        
        options = HxOptions(out_dir,"",True,False,"")
        
	export_list(obs,options)
