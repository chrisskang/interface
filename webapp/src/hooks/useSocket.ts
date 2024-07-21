import { useEffect, useRef, useState } from "react"

export const useSocket = () => {
	const socket = useRef<WebSocket | undefined>(undefined)
	const [connected, setConnected] = useState(false)

	const positions = useRef(new Float32Array(
		[
			0,975,0,220.408726,1250,0,333.469624,916.200311,0,634.641613,1099.231563,0,626.717875,746.893369,0,972.327343,815.879614,0,844.374771,487.499996,0,1192.73612,434.120438,0,960.187565,169.306942,0,1269.283265,-0.000041,0,960.187564,-169.306947,0,1192.736129,-434.120412,0,844.374771,-487.499995,0,972.327396,-815.87955,0,626.717917,-746.893334,0,634.641629,-1099.231554,0,333.469627,-916.20031,0,220.408709,-1250.000003,0,0,-975,0,-220.408726,-1250,0,-333.469624,-916.200311,0,-634.641613,-1099.231563,0,-626.717875,-746.893369,0,-972.327343,-815.879614,0,-844.374771,-487.499996,0,-1192.73612,-434.120438,0,-960.187565,-169.306942,0,-1269.283265,0.000041,0,-960.187564,169.306947,0,-1192.736129,434.120412,0,-844.374771,487.499995,0,-972.327396,815.87955,0,-626.717917,746.893334,0,-634.641629,1099.231554,0,-333.469627,916.20031,0,-220.408709,1250.000003,0
]
	))

	useEffect(() => {
		const connect = () => {
			console.log("Trying to connect to socket")

			socket.current = new WebSocket("ws://localhost:8001")

			socket.current.onopen = (event) => {
				console.log("OPEN: ", event)

				setConnected(true)

				send({ type: "login", client: "interface" })
			}

			socket.current.onmessage = (event) => {
				if (typeof event.data === "string") {
					const message = JSON.parse(event.data)
	

					if (message.type === "positions") {
		
					positions.current = message["positions"]
					//console.log("positions.current: ", positions.current)
					}
				}
			}

			socket.current.onclose = (event) => {
				console.log(
					"Socket is closed. Reconnect will be attempted in 1 second.",
					event.reason,
				)

				setConnected(false)

				socket.current = undefined

				setTimeout(() => {
					connect()
				}, 1000)
			}

			socket.current.onerror = (event) => {
				console.log("ERROR: ", event)
			}
		}
		connect()

		if (socket) return () => socket.current?.close()
	}, [])

	const send = (data: any) => {
		if (socket.current) {
			if (socket.current.readyState === WebSocket.OPEN) {
				socket.current.send(JSON.stringify(data))
			}
		}
	}

	return {
		socket: socket.current,
		connected,
		positions,
		send,
	}
}
