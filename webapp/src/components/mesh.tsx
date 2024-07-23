import { Edges, Outlines } from "@react-three/drei"
import { useFrame } from "@react-three/fiber"
import React from "react"
import { type RefObject, useRef } from "react"
import { type BufferAttribute, DoubleSide, MathUtils } from "three"

const positions = new Float32Array([
	0,975,0,220.408726,1250,0,333.469624,916.200311,0,634.641613,1099.231563,0,626.717875,746.893369,0,972.327343,815.879614,0,844.374771,487.499996,0,1192.73612,434.120438,0,960.187565,169.306942,0,1269.283265,-0.000041,0,960.187564,-169.306947,0,1192.736129,-434.120412,0,844.374771,-487.499995,0,972.327396,-815.87955,0,626.717917,-746.893334,0,634.641629,-1099.231554,0,333.469627,-916.20031,0,220.408709,-1250.000003,0,0,-975,0,-220.408726,-1250,0,-333.469624,-916.200311,0,-634.641613,-1099.231563,0,-626.717875,-746.893369,0,-972.327343,-815.879614,0,-844.374771,-487.499996,0,-1192.73612,-434.120438,0,-960.187565,-169.306942,0,-1269.283265,0.000041,0,-960.187564,169.306947,0,-1192.736129,434.120412,0,-844.374771,487.499995,0,-972.327396,815.87955,0,-626.717917,746.893334,0,-634.641629,1099.231554,0,-333.469627,916.20031,0,-220.408709,1250.000003,0

])

const indices = new Uint16Array([
	0, 1, 2, 1, 3, 2, 2, 3, 4, 3, 5, 4, 4, 5, 6, 5, 7, 6, 6, 7, 8, 7, 9, 8, 8, 9,
	10, 9, 11, 10, 10, 11, 12, 11, 13, 12, 12, 13, 14, 13, 15, 14, 14, 15, 16, 15,
	17, 16, 16, 17, 18, 17, 19, 18, 18, 19, 20, 19, 21, 20, 20, 21, 22, 21, 23,
	22, 22, 23, 24, 23, 25, 24, 24, 25, 26, 25, 27, 26, 26, 27, 28, 27, 29, 28,
	28, 29, 30, 29, 31, 30, 30, 31, 32, 31, 33, 32, 32, 33, 34, 33, 35, 34, 34,
	35, 0, 35, 1, 0,
])
const colors = new Float32Array([
	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
])
const normals = new Float32Array([
	0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0,
	1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0,
	0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1,
	0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0,
	1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0,
	0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1,
	0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0,
	1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0,
	0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1,
	0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0,
	1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0,
	0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1,
	0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1,
])

export function Comp({ positions }: { positions: RefObject<number[]>, delta: Number }) {
	const positionBuffer = useRef<BufferAttribute>(null)

	useFrame((_,delta ) => {
		if (positionBuffer.current && positions.current) {
			//positionBuffer.current.array.set(new Float32Array(positions.current),0)

			const newArray = new Float32Array(108)
			for (let i = 0; i < 108; i++) {
				//newArray[i] = positionBuffer.current.array[i]*(1-clock.getDelta())+positions.current[i]*clock.getDelta()
				
				newArray[i] = MathUtils.damp(
					positionBuffer.current.array[i],
					positions.current[i],
					1,
					delta
				)
			}
			positionBuffer.current.array = newArray
			//positionBuffer.current.array = new Float32Array(positions.current)
			positionBuffer.current.needsUpdate = true
			//console.log(positionBuffer.current.array)
		}
	})

	return (
		<mesh scale={0.001} castShadow receiveShadow>
			<bufferGeometry>
				<bufferAttribute
					array={new Float32Array(positions.current ?? new Array(108).fill(0))}
					ref={positionBuffer}
					attach="attributes-position"
					count={36}
					itemSize={3}
				/>
				<bufferAttribute
					attach="attributes-color"
					array={colors}
					count={colors.length / 3}
					itemSize={3}
				/>
				<bufferAttribute
					attach="attributes-normal"
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
			
			<meshStandardMaterial wireframe side={DoubleSide} color = {"white"} metalness={1}/>
			
		</mesh>
	)
}
