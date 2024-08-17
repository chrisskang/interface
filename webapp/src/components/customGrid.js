
import { Grid } from "@react-three/drei"

export function CustomGrid() {

	return (
		<Grid
    position={[0, -1.309, 0]}
    infiniteGrid
    cellSize={1}
    cellThickness={1.5}
    sectionSize={0.1}
    sectionThickness={1}
    fadeDistance={10}
    sectionColor={"white"}
    cellColor={"white"}
/>
	)
}
