import { Grid, OrbitControls } from "@react-three/drei";
import { Canvas } from "@react-three/fiber";
import React from "react";
import { Env } from "./components/env";
import { Comp } from "./components/mesh";
import { useSocket } from "./hooks/useSocket";

export default function App() {
  const { angles, send } = useSocket()

  return (
    <Canvas shadows camera={{ position: [0, 1, 10], fov: 50 }}>
      <group position={[0, 0, 0]}>
        {/* <Sphere /> */}
        <Comp />

        <Grid
          position={[0, -1.1, 0]}
          infiniteGrid
          cellSize={10}
          cellThickness={2}
          sectionSize={0.1}
          sectionThickness={0.75}
          sectionColor={"#ffffff"}
          cellColor={"#ffffff"}
        />
      </group>
      <Env />
      <OrbitControls enablePan={false} enableZoom={true} />
    </Canvas>
  );
}
