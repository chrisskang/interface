import { OrbitControls, MeshReflectorMaterial} from "@react-three/drei"
import { Canvas } from "@react-three/fiber"
import { default as React } from "react"
import { Env } from "./components/env"
import { TriangleMesh } from "./components/mesh"
import { UI } from "./components/ui"
import { useSocket } from "./hooks/useSocket"
import { CustomGrid } from "./components/customGrid"
import { useControls, button, folder, Leva} from 'leva'
import { label } from "three/examples/jsm/nodes/Nodes.js"

export default function App() {
	const { positions, send } = useSocket()
	const datas = useControls({
		manual: {value: false, label: "Manual", order: -1},
      '1~12': folder(
		{
			1: 
				{label: '1',
				value: 0,
				min: -45,
				max: 45,
				step: 1,
				suffix: '°', order : 1},
				active1: {value: false, label: "Active", order: 1},
			2: 
				{label: '2',
				value: 0,
				min: -45,
				max: 45,
				step: 1,
				suffix: '°', order : 2},
				active2: {value: false, label: "Active", order: 2},
			3:
				{label: '3',
				value: 0,
				min: -45,
				max: 45,
				step: 1,
				suffix: '°', order : 3},
				active3: {value: false, label: "Active", order: 3},
			4:
				{label: '4',
				value: 0,
				min: -45,
				max: 45,
				step: 1,
				suffix: '°', order : 4},
				active4: {value: false, label: "Active", order: 4},
			5:
				{label: '5',
				value: 0,
				min: -45,
				max: 45,
				step: 1,
				suffix: '°', order : 5},
				active5: {value: false, label: "Active", order: 5},
			6:	
				{label: '6',
				value: 0,
				min: -45,
				max: 45,
				step: 1,
				suffix: '°', order : 6},
				active6: {value: false, label: "Active", order: 6},
			7:
				{label: '7',
				value: 0,
				min: -45,
				max: 45,
				step: 1,
				suffix: '°', order : 7},
				active7: {value: false, label: "Active", order: 7},
			8:
				{label: '8',
				value: 0,
				min: -45,
				max: 45,
				step: 1,
				suffix: '°', order : 8},
				active8: {value: false, label: "Active", order: 8},
			9:
				{label: '9',
				value: 0,
				min: -45,
				max: 45,
				step: 1,
				suffix: '°', order : 9},
				active9: {value: false, label: "Active", order: 9},
			10:
				{label: '10',
				value: 0,
				min: -45,
				max: 45,
				step: 1,
				suffix: '°', order : 10},
				active10: {value: false, label: "Active", order: 10},
			11:
				{label: '11',
				value: 0,
				min: -45,
				max: 45,
				step: 1,
				suffix: '°', order : 11},
				active11: {value: false, label: "Active", order: 11},
			12:
				{label: '12',
				value: 0,
				min: -45,
				max: 45,
				step: 1,
				suffix: '°', order : 12},
				active12: {value: false, label: "Active", order: 12},
   },
	  {collapsed : true}
	),
	'13~24': folder(
		{
			13: 
				{label: '13',
				value: 0,
				min: -45,
				max: 45,
				step: 1,
				suffix: '°', order : 13},
				active13: {value: false, label: "Active", order: 13},
			14:
				{label: '14',
				value: 0,
				min: -45,
				max: 45,
				step: 1,
				suffix: '°', order : 14},
				active14: {value: false, label: "Active", order: 14},
			15:
				{label: '15',
				value: 0,
				min: -45,
				max: 45,
				step: 1,
				suffix: '°', order : 15},
				active15: {value: false, label: "Active", order: 15},
			16:
				{label: '16',
				value: 0,
				min: -45,
				max: 45,
				step: 1,
				suffix: '°', order : 16},
				active16: {value: false, label: "Active", order: 16},
			17:
				{label: '17',
				value: 0,
				min: -45,
				max: 45,
				step: 1,
				suffix: '°', order : 17},
				active17: {value: false, label: "Active", order: 17},
			18:
				{label: '18',
				value: 0,
				min: -45,
				max: 45,
				step: 1,
				suffix: '°', order : 18},
				active18: {value: false, label: "Active", order: 18},
			19:
				{label: '19',
				value: 0,
				min: -45,
				max: 45,
				step: 1,
				suffix: '°', order : 19},
				active19: {value: false, label: "Active", order: 19},
			20:
				{label: '20',
				value: 0,
				min: -45,
				max: 45,
				step: 1,
				suffix: '°', order : 20},
				active20: {value: false, label: "Active", order: 20},
			21:
				{label: '21',
				value: 0,
				min: -45,
				max: 45,
				step: 1,
				suffix: '°', order : 21},
				active21: {value: false, label: "Active", order: 21},
			22:
				{label: '22',
				value: 0,
				min: -45,
				max: 45,
				step: 1,
				suffix: '°', order : 22},
				active22: {value: false, label: "Active", order: 22},
			23:
				{label: '23',
				value: 0,
				min: -45,
				max: 45,
				step: 1,
				suffix: '°', order : 23},
				active23: {value: false, label: "Active", order: 23},
			24:
				{label: '24',
				value: 0,
				min: -45,
				max: 45,
				step: 1,
				suffix: '°', order : 24},
				active24: {value: false, label: "Active", order: 24},		
   	},
	  {collapsed : true}
	),
   
    })

  

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
				<></>
			</div>


			<Canvas shadows camera={{ position: [3, 2, 3], fov: 50 }}>
				<Env />
				<fog attach="fog" args={['black', 5, 20]} />
				<ambientLight intensity={0.5} />
				<hemisphereLight intensity={3} />

				<directionalLight position={[0, 5, 5]} castShadow intensity={5} shadow-mapSize={2048} shadow-bias={-0.001}>
					<orthographicCamera attach="shadow-camera" args={[-8.5, 8.5, 8.5, -8.5, 0.1, 20]} />
				</directionalLight>


				<mesh receiveShadow position={[0, -1.31, 0]} rotation-x={-Math.PI / 2}>
					<planeGeometry args={[50, 50]}/>
					<meshLambertMaterial color = {"#636363"}/>
				</mesh>
	
				<TriangleMesh positions={positions}/>

				<CustomGrid/>

				<OrbitControls enablePan={false} enableZoom={false} minPolarAngle={Math.PI / 2.2} maxPolarAngle={Math.PI / 2.2} />
			</Canvas>
		</div>
	)
}
