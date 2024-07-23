import { Grid, OrbitControls, MeshReflectorMaterial, ContactShadows,BakeShadows,AccumulativeShadows, RandomizedLight } from "@react-three/drei"
import { Canvas } from "@react-three/fiber"
import { default as React } from "react"
import { Env } from "./components/env"
import { Comp } from "./components/mesh"
import { UI } from "./components/ui"
import { useSocket } from "./hooks/useSocket"

export default function App() {
	const { positions, send } = useSocket()

	return (
		<div
			style={{
				width: "100vw",
				height: "100vh",
			}}
		>
			<div
				style={{
					position: "absolute",
					top: 0,
					left: 0,
					padding: "1rem",
					color: "white",
					zIndex: 2,
					backgroundColor: "rgba(0, 0, 0, 0.5)",
					borderRadius: "12px",
				}}
			>
				<UI send={send} />
			</div>
			<Canvas shadows camera={{ position: [3, 2, 3], fov: 50 }}>
				<fog attach="fog" args={['#202020', 5, 20]} />
				<ambientLight intensity={0.015} />
				<spotLight position={[1, 5, 3]} intensity={3} angle={0.2} penumbra={1}  castShadow shadow-mapSize={2048} />
      			<spotLight position={[0, 10, -10]} intensity={3} angle={0.04} penumbra={2} castShadow shadow-mapSize={1024} />
				{/* <mesh receiveShadow position={[0, -1.31, 0]} rotation-x={-Math.PI / 2}>
					<planeGeometry args={[50, 50]} />
					<MeshReflectorMaterial />
				</mesh> */}
	
				<Comp positions={positions} />
				<hemisphereLight intensity={0.5} />
      			<ContactShadows resolution={1024} frames={1} position={[0, -1.3, 0]} scale={15} blur={0.5} opacity={1} far={20} />
      

				{/* <Grid
					position={[0, -1.1, 0]}
					infiniteGrid
					cellSize={1}
					cellThickness={1.5}
					sectionSize={0.1}
					sectionThickness={1}
					fadeDistance={10}
					sectionColor={"#ffffff"}
					cellColor={"#ffffff"}
				/> */}
	
				<Env />
					
				
				


				<OrbitControls enablePan={false} enableZoom={false} minPolarAngle={Math.PI / 2.2} maxPolarAngle={Math.PI / 2.2} />
			</Canvas>
		</div>
	)
}
