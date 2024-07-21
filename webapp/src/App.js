import { Grid, OrbitControls } from "@react-three/drei"
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
				<group position={[0, 0, 0]}>
					{/* <Sphere /> */}
					<Comp positions={positions} />

					<Grid
						position={[0, -1.1, 0]}
						infiniteGrid
						cellSize={1}
						cellThickness={1.5}
						sectionSize={0.1}
						sectionThickness={1}
            fadeDistance={10}
						sectionColor={"#ffffff"}
						cellColor={"#ffffff"}
					/>
				</group>
				<Env />
				<OrbitControls enablePan={false} enableZoom={true} />
			</Canvas>
		</div>
	)
}
