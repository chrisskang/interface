import asyncio
import aioconsole
import websockets
import json

import logging
# logger = logging.getLogger('websockets')
# logger.setLevel(logging.DEBUG)
# logger.addHandler(logging.StreamHandler())

testdata0 = {"type": "angles", "angles": [{"angle": "0", "toggle": "0"}, {"angle": "0", "toggle": "0"}, {"angle": "0", "toggle": "0"}, {"angle": "0", "toggle": "0"}, {"angle": "0", "toggle": "0"}, {"angle": "0", "toggle": "0"}, {"angle": "0", "toggle": "0"}, {"angle": "0", "toggle": "0"}, {"angle": "0", "toggle": "0"}, {"angle": "0", "toggle": "0"}, {"angle": "0", "toggle": "0"}, {"angle": "0", "toggle": "0"}, {"angle": "0", "toggle": "0"}, {"angle": "0", "toggle": "0"}, {"angle": "0", "toggle": "0"}, {"angle": "0", "toggle": "0"}, {"angle": "0", "toggle": "0"}, {"angle": "0", "toggle": "0"}, {"angle": "0", "toggle": "0"}, {"angle": "0", "toggle": "0"}, {"angle": "0", "toggle": "0"}, {"angle": "0", "toggle": "0"}, {"angle": "0", "toggle": "0"}, {"angle": "0", "toggle": "0"}, {"angle": "0", "toggle": "0"}, {"angle": "0", "toggle": "0"}, {"angle": "0", "toggle": "0"}, {"angle": "0", "toggle": "0"}, {"angle": "0", "toggle": "0"}, {"angle": "0", "toggle": "0"}, {"angle": "0", "toggle": "0"}, {"angle": "0", "toggle": "0"}, {"angle": "0", "toggle": "0"}, {"angle": "0", "toggle": "0"}, {"angle": "0", "toggle": "0"}, {"angle": "0", "toggle": "0"}]}

#twist
testdata1 = {"type": "angles", "angles": [{"angle": 30, "toggle": 1}, {"angle": 60, "toggle": 1}, {"angle": -60, "toggle": 1}, {"angle": 15, "toggle": 1}, {"angle": 15, "toggle": 1}, {"angle": 15, "toggle": 1}, {"angle": -15, "toggle": 1}, {"angle": -15, "toggle": 1}, {"angle": -15, "toggle": 1}, {"angle": -15, "toggle": 1}, {"angle": -15, "toggle": 1}, {"angle": -15, "toggle": 1}, {"angle": 0, "toggle": 0}, {"angle": 0, "toggle": 0}, {"angle": 0, "toggle": 0}, {"angle": 0, "toggle": 0}, {"angle": 0, "toggle": 0}, {"angle": 0, "toggle": 0}, {"angle": 0, "toggle": 0}, {"angle": 0, "toggle": 0}, {"angle": 0, "toggle": 0}, {"angle": 0, "toggle": 0}, {"angle": 0, "toggle": 0}, {"angle": 0, "toggle": 0}, {"angle": -15, "toggle": 1}, {"angle": -15, "toggle": 1}, {"angle": -15, "toggle": 1}, {"angle": -15, "toggle": 1}, {"angle": -15, "toggle": 1}, {"angle": -15, "toggle": 1}, {"angle": 15, "toggle": 1}, {"angle": 15, "toggle": 1}, {"angle": 15, "toggle": 1}, {"angle": -60, "toggle": 1}, {"angle": 60, "toggle": 1}, {"angle": 30, "toggle": 1}]}
#lift
testdata2 = {"type": "angles", "angles": [{"angle": 30, "toggle": 1}, {"angle": -15, "toggle": 1}, {"angle": 15, "toggle": 1}, {"angle": 15, "toggle": 1}, {"angle": -30, "toggle": 1}, {"angle": 15, "toggle": 1}, {"angle": -15, "toggle": 1}, {"angle": 15, "toggle": 1}, {"angle": -15, "toggle": 1}, {"angle": 30, "toggle": 1}, {"angle": -15, "toggle": 1}, {"angle": 15, "toggle": 1}, {"angle": 0, "toggle": 0}, {"angle": 0, "toggle": 0}, {"angle": 0, "toggle": 0}, {"angle": 0, "toggle": 0}, {"angle": 0, "toggle": 0}, {"angle": 0, "toggle": 0}, {"angle": 0, "toggle": 0}, {"angle": 0, "toggle": 0}, {"angle": 0, "toggle": 0}, {"angle": 0, "toggle": 0}, {"angle": 0, "toggle": 0}, {"angle": 0, "toggle": 0}, {"angle": -15, "toggle": 1}, {"angle": 15, "toggle": 1}, {"angle": -30, "toggle": 1}, {"angle": 15, "toggle": 1}, {"angle": -15, "toggle": 1}, {"angle": 15, "toggle": 1}, {"angle": -15, "toggle": 1}, {"angle": 30, "toggle": 1}, {"angle": -15, "toggle": 1}, {"angle": -15, "toggle": 1}, {"angle": 15, "toggle": 1}, {"angle": -30, "toggle": 1}]}

testdata0 = json.dumps(testdata0)
testdata1 = json.dumps(testdata1)
testdata2 = json.dumps(testdata2)

async def listenAndSend(websocket):
    # await asyncio.gather(
    #     listen(websocket),
    #     send(websocket)
    # )
    listen_task = asyncio.create_task(listen(websocket))
    send_task = asyncio.create_task(send(websocket))
    
    done, pending = await asyncio.wait(
        [listen_task, send_task],
        return_when=asyncio.FIRST_COMPLETED,
    )
    
    for task in pending:
        task.cancel()



async def listen(websocket):

    async for message in websocket:
        await onReceived(message)

async def onReceived(message):
    print (message)


async def send(websocket):

    while True:
        await asyncio.sleep(0.75)
        message = await takeInput()
        if message == "0":
            await websocket.send(testdata0)
        elif message == "1":
            await websocket.send(testdata1)
        elif message == "2":
            await websocket.send(testdata2)
        else:
            print("Invalid input")

async def takeInput():
    print("")
    message = await aioconsole.ainput("Enter message (0/1/2): ")
    print("")
    return message

async def main():
    uri = "ws://localhost:8001"
    async with websockets.connect(uri) as websocket:
        await login(websocket)
        await listenAndSend(websocket)

async def login(websocket):
    loginData = {"type": "login","client":"py" }
    loginData = json.dumps(loginData)
    await websocket.send(loginData)

        
if __name__ == "__main__":
    asyncio.run(main())