import React from 'react'
import { useState, useTransition } from 'react'
import { useControls } from 'leva'
import { Canvas } from '@react-three/fiber'
import { AccumulativeShadows, RandomizedLight, Center, Environment, OrbitControls, Grid } from '@react-three/drei'
import { Sphere } from './components/sphere'
import { Env } from './components/env'
import { DoubleSide } from 'three'
import { Comp } from './components/mesh'

const positions = new Float32Array([
  -1.102044,6.25,0,-8.5635e-8,4.875,0,1.102044,6.25,0,1.667348,4.581002,0,3.173208,5.496158,0,3.13359,3.734467,0,4.861637,4.079398,0,4.221874,2.4375,0,5.963681,2.170602,0,4.800938,0.846535,0,6.346416,1.718e-7,0,4.800938,-0.846535,0,5.963681,-2.170602,0,4.221874,-2.4375,0,4.861637,-4.079398,0,3.13359,-3.734467,0,3.173208,-5.496158,0,1.667348,-4.581002,0,1.102044,-6.25,0,8.5635e-8,-4.875,0,-1.102044,-6.25,0,-1.667348,-4.581002,0,-3.173208,-5.496158,0,-3.13359,-3.734467,0,-4.861637,-4.079398,0,-4.221874,-2.4375,0,-5.963681,-2.170602,0,-4.800938,-0.846535,0,-6.346416,-1.718e-7,0,-4.800938,0.846535,0,-5.963681,2.170602,0,-4.221874,2.4375,0,-4.861637,4.079398,0,-3.13359,3.734467,0,-3.173208,5.496158,0,-1.667348,4.581002,0

])

const indices = new Uint16Array([
  0,1,2,1,3,2,2,3,4,3,5,4,4,5,6,5,7,6,6,7,8,7,9,8,8,9,10,9,11,10,10,11,12,11,13,12,12,13,14,13,15,14,14,15,16,15,17,16,16,17,18,17,19,18,18,19,20,19,21,20,20,21,22,21,23,22,22,23,24,23,25,24,24,25,26,25,27,26,26,27,28,27,29,28,28,29,30,29,31,30,30,31,32,31,33,32,32,33,34,33,35,34,34,35,0,35,1,0

])

export default function App() {
  return (
    <Canvas shadows camera={{ position: [0, 0, 10], fov: 50 }}>
      
      <group position={[0, 0, 0]}>
        {/* <Sphere /> */}
        <Comp vertices = {positions} indicesInput = {indices}/>
        
        <Grid
				position={[0, -10, 0]}
				infiniteGrid
				cellSize={10}
				cellThickness={2}
				sectionSize={1}
				sectionThickness={0.75}
				
        sectionColor={'#000000'}
        cellColor={'#000000'}
			/>

      </group>
      <Env />
      <OrbitControls enablePan={false} enableZoom={true} />
    </Canvas>
  )
}



