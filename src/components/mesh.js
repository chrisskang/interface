import React, { useMemo } from "react"
import { DoubleSide } from "three"



export function Comp({vertices}) {

  const positions = useMemo(() => Float32Array.from(new Array(vertices.length).fill().flatMap((item, index) => vertices[index].toArray())),[vertices]);

  return (
  <mesh>
      <bufferGeometry>
          <bufferAttribute
              attach='attributes-position'
              array={positions}
              count={positions.length / 3}
              itemSize={3}
          />
          {/* <bufferAttribute
              attach='attributes-color'
              array={colors}
              count={colors.length / 3}
              itemSize={3}
          />
          <bufferAttribute
              attach='attributes-normal'
              array={normals}
              count={normals.length / 3}
              itemSize={3}
          />
          <bufferAttribute
              attach="index"
              array={indices}
              count={indices.length}
              itemSize={1}
          /> */}
      </bufferGeometry>
      <meshStandardMaterial
          vertexColors
          side={DoubleSide}
      />
  </mesh>
  )
}