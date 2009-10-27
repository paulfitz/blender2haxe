package %PACKAGE_NAME% {
	import alternativa.engine3d.core.Face;
	import alternativa.engine3d.core.Mesh;
	import alternativa.engine3d.core.Vertex;
	import alternativa.types.Point3D;
	import flash.geom.Point;

	public class %CLASS_NAME% extends Mesh {
		private function f(v1:Number,v2:Number,v3:Number,uv00:Number,uv01:Number,uv10:Number,uv11:Number,uv20:Number,uv21:Number,normX:Number,normY:Number,normZ:Number):void {
			var f:Face = createFace([v1, v2, v3]);
			setUVsToFace(new Point(uv00, 1-uv01), new Point(uv10, 1-uv11), new Point(uv20, 1-uv21), f.id);
			// NOTE: normal is calculated automatically, blender values are provided just in case you need them
		}

		private function f4(v1:Number,v2:Number,v3:Number,v4:Number,uv00:Number,uv01:Number,uv10:Number,uv11:Number,uv20:Number,uv21:Number,uv30:Number,uv31:Number,normX:Number,normY:Number,normZ:Number):void {
			var f:Face = createFace([v1, v2, v3, v4]);
			setUVsToFace(new Point(uv00, 1-uv01), new Point(uv10, 1-uv11), new Point(uv20, 1-uv21), f.id);
			// NOTE: 4th UV pair is not used (TODO use it to triangulate quad if necessary)
			// NOTE: normal is calculated automatically, blender values are provided just in case you need them
		}

		private function f2(v1:Number,v2:Number,v3:Number):void {
			createFace([v1, v2, v3]);
		}

		private function f24(v1:Number,v2:Number,v3:Number,v4:Number):void {
			createFace([v1, v2, v3, v4]);
		}

		private function v(vx:Number,vy:Number,vz:Number):void {
			createVertex(vx,vy,vz);
		}

		public function %CLASS_NAME%( p_Name:String=null ) {
			super( p_Name );

%DATA_LOOP%
			moveAllFacesToSurface ("mesh");
%TRANSFORM_PROPS%
		}
	}
}