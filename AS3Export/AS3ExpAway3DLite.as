package %PACKAGE_NAME% {
	import away3dlite.arcane;
	import away3dlite.core.base.*;
	import away3dlite.materials.*;
	import away3dlite.primitives.*;
	use namespace arcane;

	public class %CLASS_NAME% extends AbstractPrimitive {
		protected var vtmp:Vector.<Number> = new Vector.<Number>();
		protected var indicesCounter:int=0;

		public function %CLASS_NAME%(mat:Material= null) {
			super( mat );
		}
		protected override function buildPrimitive():void {
			super.buildPrimitive();

%DATA_LOOP%
%TRANSFORM_PROPS%
		}
		public function v(x:Number, y:Number, z:Number):void {
			vtmp.push(x, y, z);
		}

		public function v2(x:Number, y:Number, z:Number):void {
			_vertices.push(x, y, z);
		}

		public function uv(u:Number, v:Number):void {
			_uvtData.push(u,v,1);
		}

		public function f(vertexIndex1:int, vertexIndex2:int, vertexIndex3:int, uv00:Number, uv01:Number, uv10:Number, uv11:Number, uv20:Number, uv21:Number ):void {
			var vi1:int=vertexIndex1*3;
			var vi2:int=vertexIndex2*3;
			var vi3:int=vertexIndex3*3;
			_vertices.push(vtmp[vi1],vtmp[vi1+1],vtmp[vi1+2]);
			_vertices.push(vtmp[vi2],vtmp[vi2+1],vtmp[vi2+2]);
			_vertices.push(vtmp[vi3],vtmp[vi3+1],vtmp[vi3+2]);
			_uvtData.push(uv00,uv01,1,uv10,uv11,1,uv20,uv21,1);
			_indices.push(indicesCounter++,indicesCounter++,indicesCounter++);
		}

		public function f2(vertexIndex1:int, vertexIndex2:int, vertexIndex3:int):void {
			_indices.push(vertexIndex1,vertexIndex2,vertexIndex3);
		}

	}
}