import { Environment } from "@react-three/drei"
import { useControls } from "leva"
import { useState, useTransition } from "react"
import React from "react"

export function Env() {

    return <Environment preset={"warehouse"} background blur={0.65} />
  }
  