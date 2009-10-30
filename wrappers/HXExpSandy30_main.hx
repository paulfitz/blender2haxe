package %PACKAGE_NAME%;
import %TESTED_CLASS_NAME%;

import sandy.core.Scene3D;
import sandy.core.scenegraph.Camera3D;
import sandy.core.scenegraph.Group;
import sandy.core.scenegraph.Shape3D;
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
import flash.display.BitmapData;

//class Texture extends BitmapData { public function new() { super(1,1); } } 

class %CLASS_NAME% extends Sprite {
    private var scene: Scene3D;
    private var camera: Camera3D;
    private var shape: Shape3D;
    
    public function new () {
	    super();
	    loadShape();
	}

    public function loadShape() {
        camera = new Camera3D( 0, 0, -8);
        camera.viewport = new ViewPort(400, 300);
	camera.lookAt(0,160,0);
	camera.y = -160;

	var root:Group = createScene();
        scene = new Scene3D("scene", this, camera, root);
	Lib.current.stage.addEventListener(Event.ENTER_FRAME, 
					   enterFrameHandler);
        Lib.current.addChild(this);
    }
    
    
    public function createScene():Group {
	var g:Group = new Group();
	shape = new %TESTED_CLASS_NAME%();
        shape.enableBackFaceCulling = true;

	/*
	  var bmp = new BitmapMaterial(new Texture());
	  shape.appearance = new Appearance(bmp);
	}
	*/
	
	g.addChild(shape);
	return g;
    }

    public function enterFrameHandler( ?event : Event ) : Void {
        scene.render();
	shape.rotateX += 1;
    }
    
    
    static function main() {
	//haxe.Firebug.redirectTraces();
        new %CLASS_NAME%();
    }
    
}
