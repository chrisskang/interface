import { useEffect, useRef, useState } from "react"

export const useSocket = () => {
	const socket = useRef<WebSocket | undefined>(undefined)
	const [connected, setConnected] = useState(false)

	const positions = useRef(new Array(108).fill(0))

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
