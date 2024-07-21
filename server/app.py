#!/usr/bin/env python

import asyncio
import json
import logging

import websockets

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

        elif obj["type"] == "positions":

            for intClient in interface_clients :
                    await intClient.send(message)
                    print("sent to interface_clients")
            else:
                    print("no interface client found")
                

            
        elif obj["type"] == "angles":
            if client in interface_clients :
                print("this is from interface_client")
                for ghClient in grasshopper_clients :
                    await ghClient.send(message)
                    print("sent to gh_clients")
                else:
                    print("no interface client found")


            elif client in grasshopper_clients:
                print("this is from grasshopper_clients")
                for intClient in interface_clients:
                    await intClient.send(message)
                    print("sent to interface_clients")
                else:
                    print("no grasshopper client found")

                for pyClients in python_clients :
                    await pyClients.send(message)
                    print("sent to python_clients")
                else:
                    print("no python client found")
                

            elif client in python_clients:
                print("this is from python_clients")
                for intClient in interface_clients :
                    await intClient.send(message)
                    print("sent to interface_clients")
                else:
                    print("no python client found")
            
              

def addToClientSet(obj, websocket):
 
    if obj["client"] == "interface":
            interface_clients.add(websocket)
            print("interface client added")

    elif obj["client"] == "gh":
        grasshopper_clients.add(websocket)
        print("gh client added")

    elif obj["client"] == "py":
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