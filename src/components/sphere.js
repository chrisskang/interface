import { Center } from "@react-three/drei"
import { useControls } from "leva"
import React from "react"

export function Sphere() {
    const { roughness } = useControls({ roughness: { value: 0.5, min: 30, max: 30} })
    return (
      <Center top>
        <mesh castShadow>
          <sphereGeometry args={[0.75, 64, 64]} />
          <meshStandardMaterial metalness={1} roughness={roughness} />
        </mesh>
      </Center>
    )
  }