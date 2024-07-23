import asyncio
import random
import aioconsole
import websockets
import json
from perlin_noise import PerlinNoise

import logging
# logger = logging.getLogger('websockets')
# logger.setLevel(logging.DEBUG)
# logger.addHandler(logging.StreamHandler())

#default 0
defaultData = {"type": "angles", "angles": [{"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}]}
#toLoopGoal
loopGoal = {"type": "angles", "angles": [{"a": 0, "t": 0}, {"a": 30, "t": 1}, {"a": 30, "t": 1}, {"a": 30, "t": 1}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}]}

#toLoopBetween
loopBetween ={"type": "angles", "angles": [{"a": 0, "t": 0}, {"a": -30, "t": 1}, {"a": 30, "t": 1}, {"a": -30, "t": 1}, {"a": 0, "t": 0}, {"a": -30, "t": 1}, {"a": 0, "t": 0}, {"a": -30, "t": 1}, {"a": 0, "t": 0}, {"a": -30, "t": 1}, {"a": 30, "t": 1}, {"a": 0, "t": 0}, {"a": 30, "t": 1}, {"a": -30, "t": 1}, {"a": 0, "t": 0}, {"a": -30, "t": 1}, {"a": 0, "t": 0}, {"a": -30, "t": 1}, {"a": 30, "t": 1}, {"a": -30, "t": 1}, {"a": 30, "t": 1}, {"a": -30, "t": 1}, {"a": 30, "t": 1}, {"a": -30, "t": 1}, {"a": 30, "t": 1}, {"a": -30, "t": 1}, {"a": 30, "t": 1}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": -30, "t": 1}, {"a": 30, "t": 1}, {"a": -30, "t": 1}, {"a": 30, "t": 1}, {"a": -30, "t": 1}, {"a": 0, "t": 0}, {"a": -30, "t": 1}]}
#twist
twist = {"type": "angles", "angles": [{"angle": 30, "toggle": 1}, {"angle": 60, "toggle": 1}, {"angle": -60, "toggle": 1}, {"angle": 15, "toggle": 1}, {"angle": 15, "toggle": 1}, {"angle": 15, "toggle": 1}, {"angle": -15, "toggle": 1}, {"angle": -15, "toggle": 1}, {"angle": -15, "toggle": 1}, {"angle": -15, "toggle": 1}, {"angle": -15, "toggle": 1}, {"angle": -15, "toggle": 1}, {"angle": 0, "toggle": 0}, {"angle": 0, "toggle": 0}, {"angle": 0, "toggle": 0}, {"angle": 0, "toggle": 0}, {"angle": 0, "toggle": 0}, {"angle": 0, "toggle": 0}, {"angle": 0, "toggle": 0}, {"angle": 0, "toggle": 0}, {"angle": 0, "toggle": 0}, {"angle": 0, "toggle": 0}, {"angle": 0, "toggle": 0}, {"angle": 0, "toggle": 0}, {"angle": -15, "toggle": 1}, {"angle": -15, "toggle": 1}, {"angle": -15, "toggle": 1}, {"angle": -15, "toggle": 1}, {"angle": -15, "toggle": 1}, {"angle": -15, "toggle": 1}, {"angle": 15, "toggle": 1}, {"angle": 15, "toggle": 1}, {"angle": 15, "toggle": 1}, {"angle": -60, "toggle": 1}, {"angle": 60, "toggle": 1}, {"angle": 30, "toggle": 1}]}
#lift
lift = {"type": "angles", "angles": [{"angle": 30, "toggle": 1}, {"angle": -15, "toggle": 1}, {"angle": 15, "toggle": 1}, {"angle": 15, "toggle": 1}, {"angle": -30, "toggle": 1}, {"angle": 15, "toggle": 1}, {"angle": -15, "toggle": 1}, {"angle": 15, "toggle": 1}, {"angle": -15, "toggle": 1}, {"angle": 30, "toggle": 1}, {"angle": -15, "toggle": 1}, {"angle": 15, "toggle": 1}, {"angle": 0, "toggle": 0}, {"angle": 0, "toggle": 0}, {"angle": 0, "toggle": 0}, {"angle": 0, "toggle": 0}, {"angle": 0, "toggle": 0}, {"angle": 0, "toggle": 0}, {"angle": 0, "toggle": 0}, {"angle": 0, "toggle": 0}, {"angle": 0, "toggle": 0}, {"angle": 0, "toggle": 0}, {"angle": 0, "toggle": 0}, {"angle": 0, "toggle": 0}, {"angle": -15, "toggle": 1}, {"angle": 15, "toggle": 1}, {"angle": -30, "toggle": 1}, {"angle": 15, "toggle": 1}, {"angle": -15, "toggle": 1}, {"angle": 15, "toggle": 1}, {"angle": -15, "toggle": 1}, {"angle": 30, "toggle": 1}, {"angle": -15, "toggle": 1}, {"angle": -15, "toggle": 1}, {"angle": 15, "toggle": 1}, {"angle": -30, "toggle": 1}]}


global noise


async def listenAndSend():
    # await asyncio.gather(
    #     listen(websocket),
    #     send(websocket)
    # )
    listen_task = asyncio.create_task(listen())
    send_task = asyncio.create_task(send())
    
    done, pending = await asyncio.wait(
        [listen_task, send_task],
        return_when=asyncio.FIRST_COMPLETED,
    )
    
    for task in pending:
        task.cancel()

def lerp(a, b, t):
    return a * (1.0 - t) + (b * t)

async def listen():

    async for message in websocket_global:
        await onReceived(message)

async def onReceived(message):
    # print ("Received message: {0}".format(message))
    # print ("")
    return




async def send_loop_between(totalTime, frameRate, goalRange):
    # generate lerped Json from loopGoal
    totalFrame = totalTime * frameRate
    for i in range(int(totalFrame)):

        bufferDict = await getBufferDictRandom(goalRange, i, totalFrame)

        await websocket_global.send(json.dumps(bufferDict))
        await asyncio.sleep(1/frameRate)

async def getBufferDictRandom(goal, currentFrame, totalFrame):
    bufferDict = defaultData
    

    for i in range(len(goal["angles"])):
        noise = PerlinNoise(octaves=8, seed=i)
            
        angleMax = goal["angles"][i]["a"]
        toggle = goal["angles"][i]["t"]
        bufferDict["angles"][i]["a"] = noise(i+(currentFrame/totalFrame)*10) * angleMax
        bufferDict["angles"][i]["t"] = toggle

    return bufferDict

async def send_loop(totalFrame, goalAngle):
    # generate lerped Json from loopGoal
    for i in range(totalFrame):
        bufferDict = getBufferDict(goalAngle, i, totalFrame)
        print("Sending frame: ", i)
        print(bufferDict)
        print("")
        await websocket_global.send(json.dumps(bufferDict))
        await asyncio.sleep(3 / totalFrame)

def getBufferDict(goal, currentFrame, totalFrame):
    bufferDict = defaultData
    lerpVal = currentFrame / (totalFrame - 1)  # Adjusted lerp value to start from 0 and end at 1

    for i in range(len(goal["angles"])):
        angle = lerp(defaultData["angles"][i]["a"], goal["angles"][i]["a"], lerpVal)
        toggle = goal["angles"][i]["t"]
        bufferDict["angles"][i]["a"] = angle
        bufferDict["angles"][i]["t"] = toggle
    return bufferDict
    
    
async def producer():
    while True:
        input = await takeInput()

        if input == "l":
            asyncio.create_task(send_loop_between(180, 2, loopBetween))
            
            print("Sending values 0-4 in the background. You can continue entering commands.")
        elif input == "1":
            return twist
        else:
            print("Invalid input")

async def send():
    while True:
        try:
            message = await producer()
            
            if message:
                assert isinstance(message, str)
                await websocket_global.send(message)
        except AssertionError:
            print("Message is not a string")
        except Exception as e:
            print(f"An error occurred: {e}")

async def takeInput():
    print("")
    message = await aioconsole.ainput("Enter message (0/1/2): ")
    print("")
    return message



async def login(websocket):
    loginData = {"type": "login","client":"py" }
    loginData = json.dumps(loginData)
    await websocket.send(loginData)
    #await websocket.send(json.dumps(defaultData))

async def main():
    uri = "ws://localhost:8001"
    async with websockets.connect(uri) as websocket:
        await login(websocket)
        global websocket_global
        websocket_global = websocket
        await listenAndSend()
        
if __name__ == "__main__":
    asyncio.run(main())