import { Center } from "@react-three/drei"
import { useControls } from "leva"
import React from "react"

export function Sphere() {
    const { roughness } = useControls({ roughness: { value: 1, min: 0, max: 1 } })
    return (
      <Center top>
        <mesh castShadow>
          <sphereGeometry args={[0.75, 64, 64]} />
          <meshStandardMaterial metalness={1} roughness={roughness} />
        </mesh>
      </Center>
    )
  }