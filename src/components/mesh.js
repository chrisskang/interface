import React, { useMemo } from "react"
import { DoubleSide } from "three"



export function Comp({vertices, indicesInput}) {
  
  const positions = useMemo(() =>
    
    Float32Array.from(
      new Array(vertices.length).fill().flatMap(
        (item, index) => vertices[index]
    )),[vertices]);
  
    const indicess = useMemo(() =>
    
      Uint16Array.from(
        new Array(indicesInput.length).fill().flatMap(
          (item, index) => indicesInput[index]
      )),[indicesInput]);
    
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
          /> */}
          <bufferAttribute
              attach="index"
              array={indicess}
              count={indicess.length}
              itemSize={1}
          />
      </bufferGeometry>
      <meshStandardMaterial
          vertexColors
          side={DoubleSide}
      />
  </mesh>
  )
}