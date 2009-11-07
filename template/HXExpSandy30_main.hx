// -*- mode:java; tab-width:4; c-basic-offset:4; indent-tabs-mode:nil -*-

package {{PACKAGE_NAME}};
{% for t in TESTED_CLASSES -%}
import {{t.name}};
{% endfor %}

import sandy.core.Scene3D;
import sandy.core.scenegraph.Camera3D;
import sandy.core.scenegraph.Group;
import sandy.core.scenegraph.Shape3D;
import sandy.core.scenegraph.TransformGroup;
import sandy.events.SandyEvent;
import sandy.parser.IParser;
import sandy.parser.Parser;
import sandy.parser.ColladaParser;
import sandy.parser.ParserEvent;
import flash.display.Sprite;
import sandy.view.ViewPort;
import flash.events.Event;
import flash.Lib;
import sandy.primitive.Box;
import sandy.primitive.Sphere;
import sandy.core.Scene3D;
import sandy.materials.Appearance;
import sandy.materials.BitmapMaterial;
import sandy.materials.Material;
import sandy.materials.ColorMaterial;
import sandy.materials.attributes.MaterialAttributes;
import sandy.materials.attributes.LineAttributes;
import flash.display.BitmapData;

{% for t in TESTED_CLASSES %}
{% if t.has_texture %}
class {{t.name}}Skin extends BitmapData { 
    public function new() { super(1,1); } 
} 
{% endif %}
{% endfor %}

class {{CLASS_NAME}} extends Sprite {
    private var scene: Scene3D;
    private var camera: Camera3D;
    private var shapes: TransformGroup;
    
    public function new () {
        super();
        loadShape();
    }
	
    public function loadShape() {
        camera = new Camera3D(0,0,45,0.1);
        camera.viewport = new ViewPort(400, 300);
        camera.x = 0;
        camera.y = 0;
        camera.z = 0;
        camera.rotateX = -{{camera_geom.RotX * (180/pi)}}+90;
        camera.rotateZ = -({{camera_geom.RotY * (180/pi)}});
        camera.rotateY = {{camera_geom.RotZ * (180/pi)}};
        camera.x = {{camera_geom.LocX}};
        camera.z = {{camera_geom.LocY}};
        camera.y = {{camera_geom.LocZ}};
        camera.scaleX = {{camera_geom.SizeX}};
        camera.scaleZ = {{camera_geom.SizeY}};
        camera.scaleY = {{camera_geom.SizeZ}};
        
        var root:Group = createScene();
        scene = new Scene3D("scene", this, camera, root);
        Lib.current.stage.addEventListener(Event.ENTER_FRAME, 
                                           enterFrameHandler);
        Lib.current.addChild(this);
    }
    
    
    public function createScene():Group {
        var g:Group = new Group();
        shapes = new TransformGroup();

        {% for t in TESTED_CLASSES %}
        var s:Shape3D = new {{t.name}}();

        // Turn off some optimizations.  These can often be turned
        // back on, but hard to know this automatically.
        s.enableBackFaceCulling = false;
        //s.useSingleContainer = false;

        {% if t.has_texture %}
        var bmp{{loop.index}} = new BitmapMaterial(new {{t.name}}Skin());
        s.appearance = new Appearance(bmp{{loop.index}});
        {% else %}
        var materialAttr{{loop.index}}:MaterialAttributes = new MaterialAttributes( 
				[new LineAttributes( 0.5, 0x2111BB, 0.4 )]
				);
	     var material{{loop.index}}:Material = new ColorMaterial( 0xFFCC33, 1, materialAttr{{loop.index}} );
        s.appearance = new Appearance(material{{loop.index}});

        {% endif %}

        shapes.addChild(s);
        {% endfor %}

        g.addChild(shapes);

        return g;
    }

    public function enterFrameHandler( ?event : Event ) : Void {
        scene.render();
        shapes.rotateY += 1;
    }
    
    
    static function main() {
        //haxe.Firebug.redirectTraces();
        new {{CLASS_NAME}}();
    }    
}
