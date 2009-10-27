package %PACKAGE_NAME% {
	import org.papervision3d.core.*;
	import org.papervision3d.materials.*;
	import org.papervision3d.core.proto.*;
	import org.papervision3d.core.geom.*;

	public class %CLASS_NAME% extends Mesh3D {
		private var ve:Array;
		private var fa:Array;

		public function %CLASS_NAME%(material : MaterialObject3D, initObject:Object=null ) {
			super( material, new Array(), new Array(), null, initObject );
			ve = this.geometry.vertices;
			fa = this.geometry.faces;
			
%DATA_LOOP%
%TRANSFORM_PROPS%
			
			this.geometry.ready = true;
		}
		public function v(x:Number, y:Number, z:Number):void {
			ve.push(new Vertex3D(x, y, z));
		}

		public function f(vertexIndex1:Number, vertexIndex2:Number, vertexIndex3:Number, imageName:String, uv00:Number, uv01:Number, uv10:Number, uv11:Number, uv20:Number, uv21:Number, normalx:Number, normaly:Number, normalz:Number):void {
			var face:Face3D = new Face3D( [ve[vertexIndex1], ve[vertexIndex2], ve[vertexIndex3]], imageName, [ {u: uv00, v: uv01}, {u: uv10, v: uv11}, {u: uv20, v: uv21} ] );
			face.faceNormal = new Number3D(normalx,normaly,normalz);
			fa.push(face);
		}

		public function f2(vertexIndex1:Number, vertexIndex2:Number, vertexIndex3:Number):void {
			var face:Face3D = new Face3D([ve[vertexIndex1], ve[vertexIndex2], ve[vertexIndex3]]);
			fa.push(face);
		}
	}
}