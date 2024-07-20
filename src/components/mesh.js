import React from 'react';

export default function Mesh() {
    const vertices = new Float32Array([
      0.0, 0.0,  0.0,
      100.0, 0.0,  0.0,
      0.0, 100.0,  0.0,
        
      100.0, 0.0,  0.0,
      100.0, 100.0,  0.0,
      0.0, 100.0,  0.0
    ]);

    const colors = new Float32Array([
      100.0, 0.0, 0.0,
      0.0, 100.0, 0.0,
      0.0, 0.0, 100.0,

      100.0, 0.0, 0.0,
      0.0, 100.0, 0.0,
      0.0, 0.0, 100.0,
    ]);

    
    return (
      <mesh>
        <bufferGeometry>
          <bufferAttribute
            attachObject={["attributes", "position"]}
            array={vertices}
            itemSize={3}
            count={6}
          />
          <bufferAttribute
            attachObject={["attributes", "color"]}
            array={colors}
            itemSize={3}
            count={6}
          />
        </bufferGeometry>
        <meshStandardMaterial attach="material" color="hotpink" flatShading={true} />
        
      </mesh>
    );
}