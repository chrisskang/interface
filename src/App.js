import React from 'react'
import { useState, useTransition } from 'react'
import { useControls } from 'leva'
import { Canvas } from '@react-three/fiber'
import { AccumulativeShadows, RandomizedLight, Center, Environment, OrbitControls, Grid } from '@react-three/drei'
import { Sphere } from './components/sphere'
import { Env } from './components/env'
import { DoubleSide } from 'three'

const positions = new Float32Array([
  1, 0, 0,
  0, 1, 0,
  -1, 0, 0,
  0, -1, 0
])

const normals = new Float32Array([
  0, 0, 1,
  0, 0, 1,
  0, 0, 1,
  0, 0, 1,
])

const colors = new Float32Array([
  0, 1, 1, 1,
  1, 0, 1, 1,
  1, 1, 0, 1,
  1, 1, 1, 1,
])

const indices = new Uint16Array([
  0, 1, 3,
  2, 3, 1,
])

const Comp = () =>
  <mesh>
      <bufferGeometry>
          <bufferAttribute
              attach='attributes-position'
              array={positions}
              count={positions.length / 3}
              itemSize={3}
          />
          <bufferAttribute
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
          />
      </bufferGeometry>
      <meshStandardMaterial
          vertexColors
          side={DoubleSide}
      />
  </mesh>

export default function App() {
  return (
    <Canvas shadows camera={{ position: [0, 0, 10], fov: 50 }}>
      
      <group position={[0, -0.65, 0]}>
        {/* <Sphere /> */}
        <Comp />
        
        <Grid
				position={[0, 0, 0]}
				infiniteGrid
				cellSize={10}
				cellThickness={2}
				sectionSize={1}
				sectionThickness={0.75}
				fadeDistance={50}
        sectionColor={'#000000'}
        cellColor={'#000000'}
			/>

      </group>
      <Env />
      <OrbitControls enablePan={false} enableZoom={true} />
    </Canvas>
  )
}



