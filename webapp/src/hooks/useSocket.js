import { useEffect, useRef, useState } from "react"

export const useSocket = () => {
	const socket = useRef(undefined)
	const [connected, setConnected] = useState(false)

	const angles = useRef(new Array(360).fill(0))

	useEffect(() => {
		const connect = () => {
			console.log("Trying to connect to socket")

			socket.current = new WebSocket("ws://localhost:8001")

			socket.current.onopen = (event) => {
				console.log("OPEN: ", event)

				setConnected(true)

				send("login", "interface")
			}

			socket.current.onmessage = (event) => {
				if (typeof event.data === "string") {
					const message = JSON.parse(event.data)

					if (message.type === "angles") {
						angles.current = message.data
					}
				}
			}

			socket.current.onclose = (event) => {
				console.log(
					"Socket is closed. Reconnect will be attempted in 1 second.",
					event.reason,
				)

				setConnected(false)

				socket.current = null

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

	const send = (type, data) => {
		socket.current?.send(JSON.stringify({ type, data }))
	}

	return {
		socket: socket.current,
		connected,
		angles,
		send
	}
}