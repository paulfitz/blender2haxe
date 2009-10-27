package %PACKAGE_NAME%;

import sandy.primitive.Primitive3D;
import sandy.core.scenegraph.Geometry3D;
import sandy.core.scenegraph.Shape3D;

class %CLASS_NAME% extends Shape3D, implements Primitive3D {
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
			l.setFaceNormal(l.getNextFaceNormalID(), normX,normY,normZ);
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
			l.setVertex(l.getNextVertexID(),vx,vy,vz);
		}

		public function new( p_Name:String=null ) {
			super( p_Name );
			geometry = generate();
		}

		public function generate<T>(?arguments:Array<T>):Geometry3D {
			l = new Geometry3D();
			
%DATA_LOOP%			
%TRANSFORM_PROPS%
			
			return (l);
		}
}
