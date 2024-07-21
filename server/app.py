#!/usr/bin/env python

import asyncio
import json
import logging

import websockets

interface_clients = set()
grasshopper_clients = set()
python_clients = set()

counter = 0

async def handler(websocket):
    #when new client connects
    if await existingClient(websocket):
        await startListening(websocket)
    elif not await existingClient(websocket):
        await login(websocket)


async def startListening(websocket):
    #when client is connected, start listening for messages
    if websocket.open:

        async for message in websocket:

            message = json.loads(message)
            await route(message, websocket)
    

async def route(msg, client):
    global counter
    counter += 1
    if client in interface_clients:
        print("message{0} received from interface_clients".format(counter))
        for ghClient in grasshopper_clients :
            await ghClient.send(json.dumps(msg))
            print("message{0} sent to gh_clients".format(counter))

    elif client in grasshopper_clients:
        print("message{0} received from grasshopper_clients".format(counter))
        
        for intClient in interface_clients :
            if intClient.open:
                await intClient.send(json.dumps(msg))
                print("message{0} sent to interface_clients".format(counter))


async def existingClient(ws):
    if ws in interface_clients or ws in grasshopper_clients or ws in python_clients:
        print("already logged in")
        return True
    else:
        return False

async def addToClientSet(obj, websocket):
 
    if obj["client"] == "interface" and websocket not in interface_clients:
        interface_clients.add(websocket)
        print("--------------------")
        print("new interface client added")
        print("interfaceClient : {0}".format(len(interface_clients)))
        print("--------------------")

    elif obj["client"] == "gh" and websocket not in grasshopper_clients:
        grasshopper_clients.add(websocket)
        print("--------------------")
        print("new gh client added")
        print("ghClient : {0}".format(len(grasshopper_clients)))
        print("--------------------")

    elif obj["client"] == "py" and websocket not in python_clients:
        python_clients.add(websocket)
        print("--------------------")
        print("new py client added")
        print("pythonClient : {0}".format(len(python_clients)))
        print("--------------------")
 

async def login(websocket):
    message = await websocket.recv() #wait for login message
    loginData = json.loads(message)
    
    assert loginData["type"] == "login", "login type not found, closing connection"
    await addToClientSet(loginData,websocket)
    
    await startListening(websocket)



#         elif obj["type"] == "positions":

#             for intClient in interface_clients :
#                 #if intClient.connected: add check connect

#                     await intClient.send(message)
#                     print("sent to interface_clients")
#             else:
#                     print("no interface client found")
                
            
#         elif obj["type"] == "angles":
#             if client in interface_clients :
#                 print("this is from interface_client")
#                 for ghClient in grasshopper_clients :
#                     await ghClient.send(message)
#                     print("sent to gh_clients")
#                 else:
#                     print("no interface client found")


#             elif client in grasshopper_clients:
#                 print("this is from grasshopper_clients")
#                 for intClient in interface_clients:
#                     await intClient.send(message)
#                     print("sent to interface_clients")
#                 else:
#                     print("no interface client found")

#                 for pyClients in python_clients :
#                     await pyClients.send(message)
#                     print("sent to python_clients")
#                 else:
#                     print("no python client found")
                

#             elif client in python_clients:
#                 print("this is from python_clients")
#                 for intClient in interface_clients :
#                     await intClient.send(message)
#                     print("sent to interface_clients")
#                 else:
#                     print("no interface client found")
            
                  #todo
        #kill the unwanted clients    




async def main():
    async with websockets.serve(handler, "", 8001):
        await asyncio.Future()  # run forever

# logger = logging.getLogger('websockets')
# logger.setLevel(logging.DEBUG)
# logger.addHandler(logging.StreamHandler())


if __name__ == "__main__":
    asyncio.run(main())