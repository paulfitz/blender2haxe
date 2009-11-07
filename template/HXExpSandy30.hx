// -*- mode:java; tab-width:4; c-basic-offset:4; indent-tabs-mode:nil -*-

package {{PACKAGE_NAME}};

import sandy.primitive.Primitive3D;
import sandy.core.scenegraph.Geometry3D;
import sandy.core.scenegraph.Shape3D;

class {{CLASS_NAME}} extends Shape3D, implements Primitive3D {
    private var l:Geometry3D;

    private function f(v1:Int,v2:Int,v3:Int,uv00:Float,uv01:Float,uv10:Float,uv11:Float,uv20:Float,uv21:Float,normX:Float,normY:Float,normZ:Float):Void {
	var uv1:Int = l.getNextUVCoordID();
	var uv2:Int = uv1 + 1;
	var uv3:Int = uv2 + 1;

	l.setUVCoords(uv1,uv00,1-uv01);
	l.setUVCoords(uv2,uv10,1-uv11);
	l.setUVCoords(uv3,uv20,1-uv21);

	l.setFaceVertexIds(l.getNextFaceID(), [v1,v2,v3]);
	l.setFaceUVCoordsIds(l.getNextFaceUVCoordID(), [uv1,uv2,uv3]);
	l.setFaceNormal(l.getNextFaceNormalID(), normX,normZ,normY);
    }

    private function f4(v1:Int,v2:Int,v3:Int,v4:Int,uv00:Float,uv01:Float,uv10:Float,uv11:Float,uv20:Float,uv21:Float,uv30:Float,uv31:Float,normX:Float,normY:Float,normZ:Float):Void {
	var uv1:Int = l.getNextUVCoordID();
	var uv2:Int = uv1 + 1;
	var uv3:Int = uv2 + 1;
	var uv4:Int = uv3 + 1;

	l.setUVCoords(uv1,uv00,1-uv01);
	l.setUVCoords(uv2,uv10,1-uv11);
	l.setUVCoords(uv3,uv20,1-uv21);
	l.setUVCoords(uv4,uv30,1-uv31);

	l.setFaceVertexIds(l.getNextFaceID(),[v1,v2,v3,v4]);
	l.setFaceUVCoordsIds(l.getNextFaceUVCoordID(),[uv1,uv2,uv3,uv4]);
	l.setFaceNormal(l.getNextFaceNormalID(),normX,normZ,normY);
    }

    private function f2(v1:Int,v2:Int,v3:Int):Void {
	l.setFaceVertexIds(l.getNextFaceID(), [v1,v2,v3]);
    }

    private function f24(v1:Int,v2:Int,v3:Int,v4:Int):Void {
	l.setFaceVertexIds(l.getNextFaceID(), [v1,v2,v3,v4]);
    }

    private function v(vx:Float,vy:Float,vz:Float):Void {
	l.setVertex(l.getNextVertexID(),vx,vz,vy);
    }

    public function new( p_Name:String=null ) {
	    super( p_Name );
	    geometry = generate();
	}

	public function generate<T>(?arguments:Array<T>):Geometry3D {
	    l = new Geometry3D();
		
	    {% for v in mesh.verts -%}
	    v({{v.co.x}},{{v.co.y}},{{v.co.z}});
	    {% endfor %}

	    {% for f in mesh.faces -%}
	    {% if mesh.faceUV -%}
	    {% if f.uv|length < 4 -%}
	    f({{f.verts[0].index}},{{f.verts[1].index}}, {{f.verts[2].index}}, {{f.uv[0][0]}}, {{f.uv[0][1]}},{{f.uv[1][0]}}, {{f.uv[1][1]}}, {{f.uv[2][0]}}, {{f.uv[2][1]}}, {{f.no.x}}, {{f.no.y}}, {{f.no.z}});
	    {%- else -%}
	    f4({{f.verts[0].index}}, {{f.verts[1].index}}, {{f.verts[2].index}}, {{f.verts[3].index}}, {{f.uv[0][0]}}, {{f.uv[0][1]}}, {{f.uv[1][0]}}, {{f.uv[1][1]}}, {{f.uv[2][0]}}, {{f.uv[2][1]}}, {{f.uv[3][0]}}, {{f.uv[3][1]}}, {{f.no.x}}, {{f.no.y}}, {{f.no.z}});
	    {% endif -%}
	    {%- else -%}
	    {% if f.verts|length < 4 -%}
	    f2({{f.verts[0].index}}, {{f.verts[1].index}}, {{f.verts[2].index}});
	    {% else -%}
	    f24({{f.verts[0].index}}, {{f.verts[1].index}}, {{f.verts[2].index}}, {{f.verts[3].index}});
	    {% endif -%}
	    {% endif -%}
	    {% endfor %}

        {% set rot = object.getEuler('worldspace') %}

	    rotateX = -({{rot[0] * (180/pi)}});
	    rotateZ = -({{rot[1] * (180/pi)}});
        rotateY = {{rot[2] * (180/pi)}};

        {% set sz = object.getSize('worldspace') %}

	    scaleX = {{sz[0]}};
	    scaleZ = {{sz[1]}};
	    scaleY = {{sz[2]}};

        {% set loc = object.getLocation('worldspace') %}

	    x = {{loc[0]}};
	    z = {{loc[1]}};
	    y = {{loc[2]}};

	    return (l);
	}
}

