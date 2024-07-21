import React from 'react'
import { useState, useTransition } from 'react'
import { useControls } from 'leva'
import { Canvas, useFrame } from '@react-three/fiber'
import { AccumulativeShadows, RandomizedLight, Center, Environment, OrbitControls, Grid } from '@react-three/drei'
import { Sphere } from './components/sphere'
import { Env } from './components/env'
import { DoubleSide } from 'three'
import { Comp } from './components/mesh'
import { Pane } from 'tweakpane'
import {ui} from './components/ui'

const UI = ui
const ws = new WebSocket('ws://localhost:8001')


export default function App() {


  return (
    <Canvas shadows camera={{ position: [0, 1, 10], fov: 50 }}>
      
      <group position={[0, 0, 0]}>
        {/* <Sphere /> */}
        <Comp/>
        
        <Grid
				position={[0, -1.1, 0]}
				infiniteGrid
				cellSize={10}
				cellThickness={2}
				sectionSize={0.1}
				sectionThickness={0.75}

				
        sectionColor={'#ffffff'}
        cellColor={'#ffffff'}
			/>

      </group>
      <Env />
      <OrbitControls enablePan={false} enableZoom={true} />
    </Canvas>
  )
}



