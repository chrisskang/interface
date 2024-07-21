import { useFrame } from "@react-three/fiber";
import React, { useRef } from "react";
import { DoubleSide } from "three";


const indices = new Uint16Array([
  0, 1, 2, 1, 3, 2, 2, 3, 4, 3, 5, 4, 4, 5, 6, 5, 7, 6, 6, 7, 8, 7, 9, 8, 8, 9, 10, 9, 11, 10, 10, 11, 12, 11, 13, 12, 12, 13, 14, 13, 15, 14, 14, 15, 16, 15, 17, 16, 16, 17, 18, 17, 19, 18, 18, 19, 20, 19, 21, 20, 20, 21, 22, 21, 23, 22, 22, 23, 24, 23, 25, 24, 24, 25, 26, 25, 27, 26, 26, 27, 28, 27, 29, 28, 28, 29, 30, 29, 31, 30, 30, 31, 32, 31, 33, 32, 32, 33, 34, 33, 35, 34, 34, 35, 0, 35, 1, 0
])
const colors = new Float32Array([
  0.771094, 0.404163, 0.165999, 0.985047, 0.109005, 0.30668, 0.80214, 0.445547, 0.224983, 0.011207, 0.765367, 0.028744, 0.007561, 0.510022, 0.382095, 0.279409, 0.703088, 0.235346, 0.731322, 0.089002, 0.082649, 0.338725, 0.329912, 0.731317, 0.895953, 0.81265, 0.653549, 0.926836, 0.099241, 0.691829, 0.92548, 0.980141, 0.10142, 0.038685, 0.341055, 0.84964, 0.687093, 0.744002, 0.685646, 0.093061, 0.040521, 0.27162, 0.263251, 0.499779, 0.96157, 0.556045, 0.017603, 0.488541, 0.342212, 0.485653, 0.642432, 0.620128, 0.073345, 0.895422, 0.595373, 0.432369, 0.07425, 0.434682, 0.089094, 0.296354, 0.653132, 0.875304, 0.346305, 0.533154, 0.085727, 0.785227, 0.927324, 0.968876, 0.168968, 0.532455, 0.592316, 0.959086, 0.5497, 0.638261, 0.04848, 0.811029, 0.075474, 0.830133, 0.769747, 0.339908, 0.795047, 0.165008, 0.584624, 0.613588, 0.049397, 0.305352, 0.906795, 0.205998, 0.443312, 0.908686, 0.775389, 0.252411, 0.654909, 0.389291, 0.43993, 0.165217, 0.925315, 0.730097, 0.414053, 0.176343, 0.628722, 0.048727, 0.319573, 0.809757, 0.893338, 0.683346, 0.070428, 0.435085, 0.846941, 0.784344, 0.356895, 0.244118, 0.664935, 0.749186, 0.501307, 0.488124, 0.290681, 0.732717, 0.483757, 0.780374, 0.878431, 0.721326, 0.525564, 0.260282, 0.757066, 0.339905, 0.304178, 0.160409, 0.198331, 0.883264, 0.885714, 0.345377, 0.41608, 0.593404, 0.711186, 0.74632, 0.845435, 0.774867, 0.72025, 0.366051, 0.234925, 0.471711, 0.359056, 0.658968
])
const normals = new Float32Array([
  0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1
])

export function Comp({ positions }) {
  const positionBuffer = useRef(null)

  useFrame(() => {
    if (positionBuffer.current && positions.current) {
      positionBuffer.current.array = new Float32Array(positions.current)
    }
  })

  return (
    <mesh>
      <bufferGeometry>
        <bufferAttribute
          ref={positionBuffer}
          attach='attributes-position'
          count={36}
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
  )
}