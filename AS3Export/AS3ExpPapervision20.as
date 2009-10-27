package %PACKAGE_NAME% {
	import org.papervision3d.core.math.NumberUV;
	import org.papervision3d.core.math.Number3D;
	import org.papervision3d.core.geom.renderables.Triangle3D;
	import org.papervision3d.core.geom.renderables.Vertex3D;
	import org.papervision3d.core.geom.TriangleMesh3D;
	import org.papervision3d.core.proto.MaterialObject3D;

	public class %CLASS_NAME% extends TriangleMesh3D {
		private var ve:Array;
		private var fa:Array;

		public function %CLASS_NAME%(material : MaterialObject3D ) {
			super( material, new Array(), new Array() );
			ve = this.geometry.vertices;
			fa = this.geometry.faces;
			
%DATA_LOOP%
%TRANSFORM_PROPS%
		}
		public function v(x:Number, y:Number, z:Number):void {
			ve.push(new Vertex3D(x, y, z));
		}

		public function f(vertexIndex1:Number, vertexIndex2:Number, vertexIndex3:Number, uv00:Number, uv01:Number, uv10:Number, uv11:Number, uv20:Number, uv21:Number, normalx:Number, normaly:Number, normalz:Number):void {
			var face : Triangle3D = new Triangle3D(this, [ve[vertexIndex1], ve[vertexIndex2], ve[vertexIndex3]], null, [ new NumberUV(uv00, uv01), new NumberUV(uv10, uv11), new NumberUV(uv20, uv21) ] );
			face.faceNormal = new Number3D(normalx,normaly,normalz);
			fa.push(face);
		}

		public function f2(vertexIndex1:Number, vertexIndex2:Number, vertexIndex3:Number):void {
			var face:Triangle3D = new Triangle3D(this, [ve[vertexIndex1], ve[vertexIndex2], ve[vertexIndex3]], null, []);
			fa.push(face);
		}

	}
}