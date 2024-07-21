import asyncio
import websockets
import json

async def hello():
    uri = "ws://localhost:8001"
    async with websockets.connect(uri) as websocket:
        data = {"type": "login","client":"py" }
        data = json.dumps(data)
        await websocket.send(data)
        print (data)

        # greeting = await websocket.recv()
        # print(f"<<< {greeting}")

if __name__ == "__main__":
    asyncio.run(hello())