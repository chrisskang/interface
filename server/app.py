#!/usr/bin/env python

import asyncio
import json
import logging
import gzip
import sys
import websockets

interface_clients = set()
grasshopper_clients = set()
python_clients = set()

counter = 0

async def handler(websocket):
    #when new client connects
    try:
        if await existingClient(websocket):
            await startListening(websocket)
        elif not await existingClient(websocket):
            await login(websocket)

    except (websockets.exceptions.ConnectionClosedError, websockets.exceptions.ConnectionClosedOK) as e:
        if websocket in interface_clients:
            interface_clients.remove(websocket)
            print("--------------------")
            print("interface client removed")
            print("interfaceClient : {0}".format(len(interface_clients)))
            print("--------------------")
        elif websocket in grasshopper_clients:
            grasshopper_clients.remove(websocket)
            print("--------------------")
            print("gh client removed")
            print("ghClient : {0}".format(len(grasshopper_clients)))
            print("--------------------")
        elif websocket in python_clients:
            python_clients.remove(websocket)
            print("--------------------")
            print("py client removed")
            print("pyClient : {0}".format(len(python_clients)))
            print("--------------------")


        # print("connection closed")
        # print(e)
    



async def startListening(websocket):
    #when client is connected, start listening for messages
    if websocket.open:
        async for message in websocket:
            print(message)
            message = json.loads(message)

            await route(message, websocket)
    

async def route(msg, client):
    global counter
    counter += 1
    if client in interface_clients:
        print("message{0} received from interface_clients".format(counter))
        #await sendMessageToClient("gh", msg)
        await sendMessageToClient("py", msg)

    elif client in grasshopper_clients:
        print("message{0} received from grasshopper_clients".format(counter)) 
        await sendMessageToClient("interface", msg)
        await sendMessageToClient("py", msg)
    
    elif client in python_clients:
        print("message{0} received from py_clients".format(counter))
        await sendMessageToClient("interface", msg)
        await sendMessageToClient("gh", msg)


async def sendMessageToClient(clientType, msg):
    if clientType == "interface":
        for intClient in interface_clients :
            if intClient.open:
                await intClient.send(json.dumps(msg))
                print("message{0} sent to interface_clients".format(counter))
    elif clientType == "gh":
        for ghClient in grasshopper_clients :
            await ghClient.send(json.dumps(msg))
            print("message{0} sent to gh_clients".format(counter))
    elif clientType == "py":
        for pyClients in python_clients :
            await pyClients.send(json.dumps(msg))
            print("message{0} sent to py_clients".format(counter))

def check_payload_size(message, max_size=65536):
    print("Raw message:", message)
    print("Message type:", type(message))
    message_size = len(message)
    print("String length:", message_size)
    encoded = message.encode('utf-8')
    print("UTF-8 encoded length:", len(encoded))
    print("Message size:", message_size)




def compress_json_string(json_string):
    return gzip.compress(json_string.encode('utf-8'))

def decompress_json_string(compressed_data):
    return gzip.decompress(compressed_data).decode('utf-8')

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




async def main():
    async with websockets.serve(handler, "", 8001):
        await asyncio.Future()  # run forever

logger = logging.getLogger('websockets')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())


if __name__ == "__main__":
    asyncio.run(main())