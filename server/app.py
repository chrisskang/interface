#!/usr/bin/env python

import asyncio
import json
import websockets

import logging


interface_clients = set()
grasshopper_clients = set()
python_clients = set()

async def handler(client):
    async for message in client:
        print(message)
        obj = json.loads(message)
        
        try:
            assert "type" in obj
        except AssertionError:
            print("no type in message")
            return
        
        if obj["type"] == "login":
            addToClientSet(obj, client)

        elif obj["type"] == "angle":
            if client in interface_clients :
                print("this is from interface_client")

                print("sent to grasshopper_clients")

            elif client in grasshopper_clients:
                print("this is from grasshopper_clients")
                for intClient in interface_clients :
                    await intClient.send(message)
                    print("sent to interface_clients")
                else:
                    print("client not in interface_clients")
                

            elif client in python_clients:
                print("this is from python_clients")
            
              

def addToClientSet(obj, websocket):
    if obj["client"] == "interface":
            interface_clients.add(websocket)
            print("interface client added")
    elif obj["type"] == "login":
        if obj["client"] == "gh":
            grasshopper_clients.add(websocket)
            print("gh client added")
    elif obj["type"] == "login":
        if obj["client"] == "py":
            python_clients.add(websocket)
            print("py client added")


async def main():
    async with websockets.serve(handler, "", 8001):
        await asyncio.Future()  # run forever

# logger = logging.getLogger('websockets')
# logger.setLevel(logging.DEBUG)
# logger.addHandler(logging.StreamHandler())

if __name__ == "__main__":
    asyncio.run(main())