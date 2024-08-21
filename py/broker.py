import asyncio
import random
import aioconsole
import websockets
import json
from perlin_noise import PerlinNoise
from collections import deque

import logging
# logger = logging.getLogger('websockets')
# logger.setLevel(logging.DEBUG)
# logger.addHandler(logging.StreamHandler())

import serial_asyncio

from utils import lerp, parse_input, translate_command_to_bytearray

monitoring = False

# Serial port settings
SERIAL_PORT = 'COM4'  # Change this to your actual port
BAUD_RATE = 9600
TIMEOUT = 1  # Adjusted timeout

start_time = 0
end_time = 0

response_callback = None

command_queue = deque()
command_in_progress = False


FRAME_RATE = 30

#define movement speed second for 1 degree of movement
MOVEMENT_SPEED = 0.5 #second per degree

#default 0
defaultData = {"type": "angles", "angles": [{"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}]}

goalPos1 = {"type": "angles", "angles": [{"a": 0, "t": 0}, {"a": 30, "t": 1}, {"a": 30, "t": 1}, {"a": 30, "t": 1}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}]}

loopBetween ={"type": "angles", "angles": [{"a": 0, "t": 0}, {"a": -30, "t": 1}, {"a": 30, "t": 1}, {"a": -30, "t": 1}, {"a": 0, "t": 0}, {"a": -30, "t": 1}, {"a": 0, "t": 0}, {"a": -30, "t": 1}, {"a": 0, "t": 0}, {"a": -30, "t": 1}, {"a": 30, "t": 1}, {"a": 0, "t": 0}, {"a": 30, "t": 1}, {"a": -30, "t": 1}, {"a": 0, "t": 0}, {"a": -30, "t": 1}, {"a": 0, "t": 0}, {"a": -30, "t": 1}, {"a": 30, "t": 1}, {"a": -30, "t": 1}, {"a": 30, "t": 1}, {"a": -30, "t": 1}, {"a": 30, "t": 1}, {"a": -30, "t": 1}, {"a": 30, "t": 1}, {"a": -30, "t": 1}, {"a": 30, "t": 1}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": -30, "t": 1}, {"a": 30, "t": 1}, {"a": -30, "t": 1}, {"a": 30, "t": 1}, {"a": -30, "t": 1}, {"a": 0, "t": 0}, {"a": -30, "t": 1}]}

twistPos = {"type": "angles", "angles": [{"angle": 30, "toggle": 1}, {"angle": 60, "toggle": 1}, {"angle": -60, "toggle": 1}, {"angle": 15, "toggle": 1}, {"angle": 15, "toggle": 1}, {"angle": 15, "toggle": 1}, {"angle": -15, "toggle": 1}, {"angle": -15, "toggle": 1}, {"angle": -15, "toggle": 1}, {"angle": -15, "toggle": 1}, {"angle": -15, "toggle": 1}, {"angle": -15, "toggle": 1}, {"angle": 0, "toggle": 0}, {"angle": 0, "toggle": 0}, {"angle": 0, "toggle": 0}, {"angle": 0, "toggle": 0}, {"angle": 0, "toggle": 0}, {"angle": 0, "toggle": 0}, {"angle": 0, "toggle": 0}, {"angle": 0, "toggle": 0}, {"angle": 0, "toggle": 0}, {"angle": 0, "toggle": 0}, {"angle": 0, "toggle": 0}, {"angle": 0, "toggle": 0}, {"angle": -15, "toggle": 1}, {"angle": -15, "toggle": 1}, {"angle": -15, "toggle": 1}, {"angle": -15, "toggle": 1}, {"angle": -15, "toggle": 1}, {"angle": -15, "toggle": 1}, {"angle": 15, "toggle": 1}, {"angle": 15, "toggle": 1}, {"angle": 15, "toggle": 1}, {"angle": -60, "toggle": 1}, {"angle": 60, "toggle": 1}, {"angle": 30, "toggle": 1}]}

liftPos = {"type": "angles", "angles": [{"angle": 30, "toggle": 1}, {"angle": -15, "toggle": 1}, {"angle": 15, "toggle": 1}, {"angle": 15, "toggle": 1}, {"angle": -30, "toggle": 1}, {"angle": 15, "toggle": 1}, {"angle": -15, "toggle": 1}, {"angle": 15, "toggle": 1}, {"angle": -15, "toggle": 1}, {"angle": 30, "toggle": 1}, {"angle": -15, "toggle": 1}, {"angle": 15, "toggle": 1}, {"angle": 0, "toggle": 0}, {"angle": 0, "toggle": 0}, {"angle": 0, "toggle": 0}, {"angle": 0, "toggle": 0}, {"angle": 0, "toggle": 0}, {"angle": 0, "toggle": 0}, {"angle": 0, "toggle": 0}, {"angle": 0, "toggle": 0}, {"angle": 0, "toggle": 0}, {"angle": 0, "toggle": 0}, {"angle": 0, "toggle": 0}, {"angle": 0, "toggle": 0}, {"angle": -15, "toggle": 1}, {"angle": 15, "toggle": 1}, {"angle": -30, "toggle": 1}, {"angle": 15, "toggle": 1}, {"angle": -15, "toggle": 1}, {"angle": 15, "toggle": 1}, {"angle": -15, "toggle": 1}, {"angle": 30, "toggle": 1}, {"angle": -15, "toggle": 1}, {"angle": -15, "toggle": 1}, {"angle": 15, "toggle": 1}, {"angle": -30, "toggle": 1}]}


global arduino_response_recorder
global noise


#-----------------Server Communication-----------------
async def server_login(websocket):
    loginData = {"type": "login","client":"py" }
    loginData = json.dumps(loginData)
    await websocket.send(loginData)

async def listen_from_server():

    async for message in websocket_global:
        await onReceived(message)

async def onReceived(message):
    print ("Received message from server: {0}".format(message))
    print ("")

#-----------------Animation-----------------
# async def loop(goalPosition, totalDuration, frameRate, random = False):
#     # generate lerped Json from loopGoal
#     totalFrame = totalDuration * frameRate

#     for i in range(totalFrame):


#     return

async def loop(goalPosition, totalDuration):
    #TODO loop between two positions

    currentPos = await getCurrentPos()
    



async def go_to_pos(goalPosition):
    currentPos = await getCurrentPos()
    print ("Current Position: {}".format(currentPos))
    #lerp between current pos to goal position with the speed of MOVEMENT_SPEED per degree
    
    currentPos
    # for angles in goalPosition["angles"]:
    #     print(angles)


async def getCurrentPos():
    #TODO: get current position from arduino
    
    for i in range(36):
        command_queue.append({"id": i, "commands": [("S", "P")]})
    recordedPos = []
    recordedPos.append(arduino_response_recorder) 
   
    
    return recordedPos

async def calibrate_angle():
    send_command_to_arduino()


# async def makeRandom(goal, currentFrame, totalFrame):
#     bufferDict = defaultData

#     for i in range(len(goal["angles"])):
#         noise = PerlinNoise(octaves=8, seed=i)
            
#         angleMax = goal["angles"][i]["a"]
#         toggle = goal["angles"][i]["t"]
#         bufferDict["angles"][i]["a"] = noise(i+(currentFrame/totalFrame)*10) * angleMax
#         bufferDict["angles"][i]["t"] = toggle

# async def send_loop(totalFrame, goalAngle):
#     # generate lerped Json from loopGoal
#     for i in range(totalFrame):
#         bufferDict = getBufferDict(goalAngle, i, totalFrame)
#         print("Sending frame: ", i)
#         print(bufferDict)
#         print("")
#         await websocket_global.send(json.dumps(bufferDict))
#         await asyncio.sleep(3 / totalFrame)
#     return bufferDict

# def getBufferDict(goal, currentFrame, totalFrame):
#     bufferDict = defaultData
#     lerpVal = currentFrame / (totalFrame - 1)  # Adjusted lerp value to start from 0 and end at 1

#     for i in range(len(goal["angles"])):
#         angle = lerp(defaultData["angles"][i]["a"], goal["angles"][i]["a"], lerpVal)
#         toggle = goal["angles"][i]["t"]
#         bufferDict["angles"][i]["a"] = angle
#         bufferDict["angles"][i]["t"] = toggle
#     return bufferDict

#-----------------Arduino Communication-----------------

async def send_command_to_arduino(inputList):
    #always input value should like this 
    #inputList = [{"id": 1, "commands": [("S", ""), ("P", "")]}, {"id": 2, "commands": [("P", ""), ("R", "")]}]

    global command_queue
    for cmdList in inputList:
        command_queue.append(cmdList)
    
    if not command_in_progress:
        await process_command_queue()
    

async def listen_from_arduino():
    while True:
        response = await wait_for_response()
        #print (response)
        #onReceivedFromArduino(response)
       
async def process_command_queue():
    
    global command_in_progress
    
    while command_queue:
        command_in_progress = True
        cmdList = command_queue.popleft()
 
        try:
            message = translate_command_to_bytearray(cmdList)
            if message is not None: 
                arduino_writer_global.write(message)
                print(f"Sent command: {message.hex()}")
            else:        
                raise TypeError 
        except TypeError:
            print('translation cmd -> byteArr error')

        # Wait for response
        response = await wait_for_response()
        translate_response(response)
        
    command_in_progress = False

async def wait_for_response():
    response = bytearray()
    max_retry = 5
    
    def print_debug_info(response):
        """ Helper function to print debugging information. """
        if monitoring:
            print(f"Received raw response: {response.decode(errors='ignore')}")
            byte_values = [f"0x{byte:02X}" for byte in response]
            print("Byte-by-byte breakdown:")
            print(' '.join(byte_values))

    for attempt in range(max_retry):
        try:
            while True:
                chunk = await asyncio.wait_for(arduino_reader_global.read(1), timeout=TIMEOUT)
                

                if not chunk:
                    break
                
                response.extend(chunk)
                
                if len(response) >= 3 and response[-3:] == b'\x99\x88\xFF':
                    response = response[:-3]
                    break
            
            if response:
                #print_debug_info(response)
                
                return response
            print(f"Attempt {attempt+1}/{max_retry}: No response received.")

        except asyncio.TimeoutError:
            print(f"Attempt {attempt+1}/{max_retry}: Timeout occurred. Retrying...")
            continue  # Retry only on timeout

        break  # Break the loop if no timeout occurred, regardless of the content

    print("Max retries reached. Exiting without a successful response.")

def translate_response(response):
    
    byte_values = [b for b in response]
    
    if len(byte_values) < 2:
        print("Response is too short to process.")
        return
    
    id_byte = byte_values[0]

    if not (0 <= id_byte <= 36) or len(byte_values) < 2:
        print("Invalid ID or response length.")
        return
    
    bufferData = {id_byte: {}}

    index = 1

    while index < len(byte_values):
        header = chr(byte_values[index])
        index += 1
       
        if header == 'S':
            if index + 3 <= len(byte_values):
                val1 = byte_values[index]
                val2 = byte_values[index + 1]
                val3 = int.from_bytes(byte_values[index + 2:index + 4], byteorder='little')
                if 32769 <= val3 <= 65535:
                    val3 = val3 - 65536  # 음수 변환
                print(f"{id_byte} : Sensor | {val1/10} v, {val2/10} a, {val3/100} °")
                index += 4
                bufferData[id_byte] = {"voltage": val1/10, "current": val2/10, "angle": val3/100}
            
            else:
                print("Incomplete data for header 'S'")
        
        elif header == 'P':
            if index + 5 <= len(byte_values):
                val1 = byte_values[index]
                val2 = int.from_bytes(byte_values[index + 1:index + 3], byteorder='little')
                val3 = byte_values[index + 3]
                val4 = byte_values[index + 4]
                val5 = byte_values[index + 5]
                print(f"{id_byte} : PWM | mosfet {val1}, servo {val2}, LED {val3}, {val4}, {val5}")
                index += 6
                bufferData[id_byte] = {"mosfet": val1, "servo": val2, "LED": [val3, val4, val5]}
            else:
                print("Incomplete data for header 'P'")
        
        elif header == 'R':
            if index + 6 <= len(byte_values):  # 총 6바이트를 읽어야 함
                val1 = int.from_bytes(byte_values[index:index + 2], byteorder='little')  # int16
                val2 = int.from_bytes(byte_values[index + 2:index + 4], byteorder='little')  # uint16
                val3 = byte_values[index + 4]  # uint8
                val4 = byte_values[index + 5]  # uint8
                print(f"{id_byte} : EEPROM | origin Angle {val1/100}, origin Pulse {val2}, current Threshold {val3/10}, Max Network Loss {val4/10}")
                index += 6  # 6바이트를 읽었으므로 인덱스를 6 증가시킴
                bufferData[id_byte] = {"originAngle": val1/100, "originPulse": val2, "currentThreshold": val3/10, "maxNetworkLoss": val4/10}
            else:
                print("Incomplete data for header 'R'")
        
        elif header in 'ACT':
            if index + 1 <= len(byte_values):
                val1 = byte_values[index]
                print(f"Header: {header} | Value: {val1}")
                index += 1
                bufferData[id_byte] = {header: val1}
            else:
                print(f"Incomplete data for header '{header}'")
        
        else:
            print(f"Unknown header: {header}")
    return bufferData


def onReceivedFromArduino(response):
    """Process the response from Arduino."""

    try:
        data = translate_response(response)
        if data is not None: 

            arduino_response_recorder.append(data)
        else:        
            raise TypeError 
    except TypeError:
        print('translation cmd -> byteArr error')

    if command_queue:
        asyncio.create_task(process_command_queue())



#-----------------Input Producer-----------------
async def producer():
    while True:
        input = await aioconsole.ainput("Choose input stream (manual : m / auto : a / calibrate : c): ")
        if input == "a" or input == "auto":
            await auto_input()
            
        elif input == "m" or input == "manual":
            await manual_input()
        elif input == "c":
            await calibrate_angle()

        else:
            print("Invalid input")

async def auto_input():
    pos_input = await aioconsole.ainput("Select Pos - Twist(T) / Lift(L) / Random(R): ")
    if pos_input == "T" or pos_input == "t":
        goalPos = twistPos
    elif pos_input == "L" or pos_input == "l":
        goalPos = liftPos
    elif pos_input == "R" or pos_input == "r":
        angleToggleInput = await aioconsole.ainput("Input max angle range/ number of toggle (eg. 30/18): ")

        maxangle = int(angleToggleInput.split("/")[0])
        numToggle = int(angleToggleInput.split("/")[1])

        goalPos = {"type": "angles", "angles": []}

        if numToggle > 36:
            raise ValueError("The number of toggles cannot exceed the total number of positions (36).")

        angles_list = [{"a": 0, "t": 0} for _ in range(36)]

        toggle_indices = random.sample(range(36), numToggle)
        
        for index in toggle_indices:
            angles_list[index] = {"a": random.randint(-maxangle, maxangle), "t": 1}

        goalPos = {"type": "angles", "angles": angles_list}      
    else:
        print("Invalid input")
 
    if pos_input is not None:
        move_input = await aioconsole.ainput("Select movement - Loop(L) / Single(S): ")
        if move_input == "L" or move_input == "l":
            totalTime = await aioconsole.ainput("Enter total time to loop(s) : ")
            await loop(goalPos, totalTime)
        elif move_input == "S" or move_input == "s":
            await go_to_pos(goalPos)
            #asyncio.create_task(go_to_pos(goalPos))
        else:
            print("Invalid input")

async def manual_input():
    user_input = await aioconsole.ainput("Enter command (e.g., '1:S', '1:A324', '1:A324,C32', '1:A324 2:C32'): ")
    if user_input:
        if user_input == '?':
            print("Read : S (sensor) P (pwm) R (eeprom)")
            print("Write : A (origin Angle) U (origin Pulse) C (currentThreshold) T (MaxNetwork) M (mosfet) V (pulse) L (LED)")
                    
        else:       
            parsed_input = parse_input(user_input)
            
            # for cmdList in parsed_input:
            #     for cmds in cmdList['commands']:
            #         if "X" in cmds:
            #             arduino_reader_global.reset_input_buffer()
            #             arduino_reader_global.reset_output_buffer()
            #             arduino_writer_global.reset_input_buffer()
            #             arduino_writer_global.reset_output_buffer()

            try:
                if parsed_input is not None: 
                    await send_command_to_arduino(parsed_input)
                else:        
                    raise TypeError 
            except TypeError:
                print('parsing error')
                pass


async def main():
    uri = "ws://localhost:8001"
    
    # Open the serial port
    arduino_reader, arduino_writer = await serial_asyncio.open_serial_connection(
    url=SERIAL_PORT, baudrate=BAUD_RATE
    )

    global arduino_reader_global, arduino_writer_global
    arduino_reader_global = arduino_reader
    arduino_writer_global = arduino_writer
    
    # try:
    async with websockets.connect(uri) as websocket:
        await server_login(websocket)
        global websocket_global
        websocket_global = websocket

        

        server_task = asyncio.create_task(listen_from_server())

        user_input_task = asyncio.create_task(producer())

        #arduino_task = asyncio.create_task(listen_from_arduino())

        await asyncio.gather(server_task, user_input_task)
        
    # except Exception as e:
    #     print(f"An error occurred: {e}")
    


if __name__ == "__main__":
    asyncio.run(main())
