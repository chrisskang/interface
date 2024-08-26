import asyncio
import math
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

monitoring = False

# Serial port settings
SERIAL_PORT = 'COM5'  # Change this to your actual port
BAUD_RATE = 9600
TIMEOUT = 1  # Adjusted timeout

start_time = 0
end_time = 0


command_queue = deque()
command_in_progress = False


FRAME_RATE = 30

#define movement speed second for 1 degree of movement
MOVEMENT_SPEED = 0.5 #second per degree
MINPULSE = 10

#TODO SOLVE THIS EQUATION
# PulsePerDegree = 12.2 #angle per 50 == 4.1

# time_per_pulse = MOVEMENT_SPEED / PulsePerDegree

# SLEEP_TIME = MINPULSE * time_per_pulse

#print(f"SLEEP_TIME: {SLEEP_TIME} seconds")


#default 0
defaultData = {"type": "angles", "angles": [{"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}]}

goalPos1 = {"type": "angles", "angles": [{"a": 0, "t": 0}, {"a": 30, "t": 1}, {"a": 30, "t": 1}, {"a": 30, "t": 1}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}]}

loopBetween ={"type": "angles", "angles": [{"a": 0, "t": 0}, {"a": -30, "t": 1}, {"a": 30, "t": 1}, {"a": -30, "t": 1}, {"a": 0, "t": 0}, {"a": -30, "t": 1}, {"a": 0, "t": 0}, {"a": -30, "t": 1}, {"a": 0, "t": 0}, {"a": -30, "t": 1}, {"a": 30, "t": 1}, {"a": 0, "t": 0}, {"a": 30, "t": 1}, {"a": -30, "t": 1}, {"a": 0, "t": 0}, {"a": -30, "t": 1}, {"a": 0, "t": 0}, {"a": -30, "t": 1}, {"a": 30, "t": 1}, {"a": -30, "t": 1}, {"a": 30, "t": 1}, {"a": -30, "t": 1}, {"a": 30, "t": 1}, {"a": -30, "t": 1}, {"a": 30, "t": 1}, {"a": -30, "t": 1}, {"a": 30, "t": 1}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": -30, "t": 1}, {"a": 30, "t": 1}, {"a": -30, "t": 1}, {"a": 30, "t": 1}, {"a": -30, "t": 1}, {"a": 0, "t": 0}, {"a": -30, "t": 1}]}

twistPos = {"type": "angles", "angles": [{"a": 30, "t": 1}, {"a": 60, "t": 1}, {"a": -60, "t": 1}, {"a": 15, "t": 1}, {"a": 15, "t": 1}, {"a": 15, "t": 1}, {"a": -15, "t": 1}, {"a": -15, "t": 1}, {"a": -15, "t": 1}, {"a": -15, "t": 1}, {"a": -15, "t": 1}, {"a": -15, "t": 1}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": -15, "t": 1}, {"a": -15, "t": 1}, {"a": -15, "t": 1}, {"a": -15, "t": 1}, {"a": -15, "t": 1}, {"a": -15, "t": 1}, {"a": 15, "t": 1}, {"a": 15, "t": 1}, {"a": 15, "t": 1}, {"a": -60, "t": 1}, {"a": 60, "t": 1}, {"a": 30, "t": 1}]}

liftPos = {"type": "angles", "angles": [{"a": 30, "t": 1}, {"a": -15, "t": 1}, {"a": 15, "t": 1}, {"a": 15, "t": 1}, {"a": -30, "t": 1}, {"a": 15, "t": 1}, {"a": -15, "t": 1}, {"a": 15, "t": 1}, {"a": -15, "t": 1}, {"a": 30, "t": 1}, {"a": -15, "t": 1}, {"a": 15, "t": 1}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": -15, "t": 1}, {"a": 15, "t": 1}, {"a": -30, "t": 1}, {"a": 15, "t": 1}, {"a": -15, "t": 1}, {"a": 15, "t": 1}, {"a": -15, "t": 1}, {"a": 30, "t": 1}, {"a": -15, "t": 1}, {"a": -15, "t": 1}, {"a": 15, "t": 1}, {"a": -30, "t": 1}]}


arduino_response_recorder = None

working_id = [4,7]
#working_id = [3,4,7,8,31,32,35,36]

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
    totalDuration = int(totalDuration)
    totalFrame = totalDuration * FRAME_RATE

    data = await parseGoalBasedOnWorkingID(goalPosition)
    for i in range(len(data)):
        #get current position
        currentPos = await getArduinoData(i, "angle")
        #get goal position
        goalPos = data[i]["angle"]
        #turn on mosfet 
        await turnOnMosfet(i)
    #--> all motors are turned on and ready
    #--> start loop
    # for i in range(totalFrame):
    #     for i in range(len(data)):
    #         await single_driveTo(data[i]["id"], angle_to_pulse(lerp(currentPos, goalPos, i/totalFrame)))
    #     await asyncio.sleep(1/FRAME_RATE)

    return


async def go_to_posALL(goalPosition):
    #parse with working ones
    data = await parseGoalBasedOnWorkingID(goalPosition)

    #turn on mosfet
    # for i in range(len(data)):
    #     await turnOnMosfet(data[i]["id"])
    
    await multiple_driveTo(data)


async def parseGoalBasedOnWorkingID(goalPosition):
    data = []

    for i in range(36):
        if i in working_id:
            if goalPosition['angles'][i]['t'] == 1:
                data.append({"id" : i, "angle" : goalPosition['angles'][i]['a']})
    
    return data

async def calibrate_angle():

    id = 32
    #turn mosfet off
    await send_command_to_arduino([{"id": id, "commands": [("M", 0)]}])
    await asyncio.sleep(1)
    
    #check mosfet turned off
    if await getArduinoData(id, "mosfet"):
        print("mosfet is not turned off")
        return
    else:
        print("mosfet is successfully turned off")
    
    
    if await turnOnMosfet(id):
        await asyncio.sleep(1)
        goal = 500
        print("mosfet is on and driving to ", goal)

        await single_driveTo(id, goal, False)
        #TODO record position

    return

async def turnOnMosfet(id):

    current_angle = await getArduinoData(id, "angle")
    current_pulse = angle_to_pulse(current_angle)

    #set pulse to match current position
    await send_command_to_arduino([{"id": id, "commands": [("V", current_pulse)]}])

    #turnon mosfet
    await send_command_to_arduino([{"id": id, "commands": [("M", 1)]}])
    #wait for 0.5 second
    await asyncio.sleep(0.5)

    #check if mosfet is still on
    return await getArduinoData(id, "mosfet")

async def multiple_driveTo(parsedPositions):
    #get current angle and max step
    maxStep = 0
    currentPositions = []
    for i in range(len(parsedPositions)):
        currentPositions.append({"id": parsedPositions[i]['id'], "currentAngle": 10, "currentPulse": angle_to_pulse(10),"goalAngle": parsedPositions[i]['angle'], "goalPulse": angle_to_pulse(parsedPositions[i]['angle'])})
        goal_range = angle_to_pulse(10)


    goal_range = 0

    for i in range(len(currentPositions)):
        
        #print (currentPositions[i])
        goal_range = currentPositions[i]["goalPulse"] - currentPositions[i]["currentPulse"]

        stepCount = goal_range/MINPULSE
        
        maxStepBuffer = math.ceil(abs(stepCount))
        if maxStepBuffer > maxStep:
            maxStep = maxStepBuffer
    
    # for i in range(maxStep):
    #     for j in range(len(currentPositions)):
    #         goal_range = currentPositions[j]["goalPulse"] - currentPositions[j]["currentPulse"]
    #         bufferStep = goal_range/maxStep

    #         if currentPositions[j]["goalPulse"] < currentPositions[j]["currentPulse"]:
    #             bufferStep = -bufferStep
    #         #await send_command_to_arduino([{"id": currentPositions[j]["id"], "commands": [("V", currentPositions[j]["currentPulse"] + bufferStep)]}])
    #         print("Driving {} to: ".format(currentPositions[j]["id"]), currentPositions[j]["currentPulse"] + bufferStep)
    #         await asyncio.sleep(0.1)

    #     if i == maxStep-1:
    #         for j in range(len(currentPositions)):
    #             #await send_command_to_arduino([{"id": currentPositions[j]["id"], "commands": [("V", currentPositions[j]["goalPulse"])]})
    #             print("Reached goal pulse at: ", currentPositions[j]["goalPulse"])
    #             print("mosfet is :", await getArduinoData(currentPositions[j]["id"], "mosfet"))
    #             print("current pulse is :", await getArduinoData(currentPositions[j]["id"], "pulse"))
    #             print("current angle is :", await getArduinoData(currentPositions[j]["id"], "angle"))

    print (maxStep)
    
    
    
    # for i in range(len(parsedPositions)):
    #     print (i)

async def single_driveTo(id, goalPulse, calibrate = False):
    #send pulse command incrementally
    currentPulse = await getArduinoData(id, "pulse")
    originPulse = await getArduinoData(id, "originPulse")

    currentPulseNormalized = currentPulse - originPulse #make it normalized to origin
    goal_range = goalPulse - currentPulseNormalized

    stepCount = goal_range/MINPULSE
    
    #check if mosfet is on
    if await getArduinoData(id, "mosfet"):
        
        for i in range(math.ceil(abs(stepCount))):

            bufferStep = i * MINPULSE
            if goal_range < 0:
                bufferStep = -bufferStep
            
            await send_command_to_arduino([{"id": id, "commands": [("V", currentPulseNormalized + bufferStep)]}])
            print("Driving to: ", currentPulseNormalized + bufferStep)
            await asyncio.sleep(0.1)
            # if calibrate:
            #     angle = await getArduinoData(id, "angle")
            #     pulse = await getArduinoData(id, "pulse")

            #     json_data = {"id": id, "goalPulse": pulse, "angle": angle}
            #     with open('calibration.json', 'a') as f:
            #         json.dump(json_data, f)
            #         f.write('\n')

            if i == math.ceil(abs(stepCount))-1:

                await send_command_to_arduino([{"id": id, "commands": [("V", goalPulse)]}])
                print("Reached goal pulse at: ", goalPulse)

                print("mosfet is :", await getArduinoData(id, "mosfet"))
                print("current pulse is :", await getArduinoData(id, "pulse"))
                print("current angle is :", await getArduinoData(id, "angle"))

    elif not await getArduinoData(id, "mosfet"):
        if await turnOnMosfet():
            single_driveTo(id, goalPulse)
    
async def getArduinoData(id,requestType):
    global arduino_response_recorder
    S_data = ["voltage", "current", "angle"]
    P_data = ["mosfet", "pulse", "LED"]
    R_data = ["originAngle", "originPulse", "currentThreshold", "maxNetworkLoss"]
        
    if requestType in S_data:
        await send_command_to_arduino([{"id": id, "commands": [("S", "")]}])
    elif requestType in P_data:
        await send_command_to_arduino([{"id": id, "commands": [("P", "")]}])
    elif requestType in R_data:
        await send_command_to_arduino([{"id": id, "commands": [("R", "")]}])

    try:
        id in arduino_response_recorder
    except:
        print("id do not match")
    
    else:
        return arduino_response_recorder[id][requestType]

def lerp(a, b, t):
    return a * (1.0 - t) + (b * t)

def parse_input(user_input):
    try:
        user_input.split()[0].split(":")[1]
    except:
        print("Invalid user input")
        return
    cmdList = []

    for index, parts in enumerate(user_input.split()):
        parts = parts.split(':')

        id = parts[0]
        cmds = parts[1]
        
        cmdList.append({})
        cmdList[index]['id'] = id
        cmdList[index]['commands'] = []
    
        for part in cmds.split(','):
            header = part[0]
            value = part[1:].strip() if len(part) > 1 else ''
            cmdList[index]['commands'].append((header, value))
        
    return cmdList

def translate_command_to_bytearray(cmdList):
    message = bytearray()
    message.append(int(cmdList['id']))
    
    for cmd in cmdList['commands']:
        header = cmd[0]
        value = cmd[1]
       
        if len(header) != 1 or not header.isalpha():
            print(f"Error: Header '{header}' must be a single alphabetic character.")
            return
        
        message.append(ord(header))  # Header를 ASCII 값으로 추가

        if header in ['A', 'V','U']:
            # 데이터가 int16_t 형식일 때
            try:
                int16_value = int(value)
                message.extend(int16_value.to_bytes(2, byteorder='little', signed=True))
            except ValueError:
                print(f"Error: Data '{value}' should be an integer for '{header}' header.")
                return
        elif header in ['C', 'T', 'M']:
            # 데이터가 int8_t 형식일 때
            try:
                int8_value = int(value)
                if not (0 <= int8_value <= 255):
                    print(f"Error: Value '{int8_value}' for header '{header}' out of range (0-255).")
                    return
                message.append(int8_value & 0xFF)
            except ValueError:
                print(f"Error: Data '{value}' should be an integer for '{header}' header.")
                return
        elif header == 'L':
            # 데이터가 3개의 int8_t 형식일 때
            try:
                values = list(map(int, value.split('/')))
                if len(values) != 3:
                    print(f"Error: Header 'L' requires exactly 3 values.")
                    return
                for val in values:
                    if not (0 <= val <= 255):
                        print(f"Error: Value '{val}' for 'L' header out of range (0-255).")
                        return
                    message.append(val & 0xFF)
            except ValueError:
                print(f"Error: Data '{value}' should be a comma-separated list of integers for 'L' header.")
                return
        elif header in ['S', 'P', 'R','H','X']:
            # 헤더가 'S', 'P', 'R'인 경우 값 없음
            pass
        else:
            print(f"Error: Unsupported header '{header}'.")
            return
        
    message.append(ord('\n'))
    return message

def angle_to_pulse(a):
    #angle per 50 == 4.1
    PulsePerDegree = 12.2
    return PulsePerDegree*a


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
    global arduino_response_recorder
    
    while command_queue:
        command_in_progress = True
        cmdList = command_queue.popleft()
 
        try:

            for cmd in cmdList['commands']:
                if cmd[0] == 'X':
                    reset_serial_buffers()
                    cmdList['commands'].remove(cmd)

            message = translate_command_to_bytearray(cmdList)
            if message is not None: 
                arduino_writer_global.write(message)
                if monitoring:
                    print(f"Sent command: {message.hex()}")
            else:        
                raise TypeError 
        except TypeError:
            print('translation cmd -> byteArr error')

        # Wait for response
        response = await wait_for_response()
        arduino_response_recorder = translate_response(response, monitoring)
        #print (arduino_response_recorder)
        
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
                print(response)
                if monitoring:
                    print_debug_info(response)
                
                return response
            print(f"Attempt {attempt+1}/{max_retry}: No response received.")

        except asyncio.TimeoutError:
            print(f"Attempt {attempt+1}/{max_retry}: Timeout occurred. Retrying...")
            continue  # Retry only on timeout

        break  # Break the loop if no timeout occurred, regardless of the content

    print("Max retries reached. Exiting without a successful response.")

def translate_response(response, monitoring = 0):
    if response is None:
        return
    
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
                if monitoring:
                    print(f"{id_byte} : Sensor | {val1/10} v, {val2/10} a, {val3/100} °")
                index += 4
                bufferData[id_byte].update({"voltage": val1/10, "current": val2/10, "angle": val3/100})
            
            else:
                print("Incomplete data for header 'S'")
        
        elif header == 'P':
            if index + 5 <= len(byte_values):
                val1 = byte_values[index]
                val2 = int.from_bytes(byte_values[index + 1:index + 3], byteorder='little')
                val3 = byte_values[index + 3]
                val4 = byte_values[index + 4]
                val5 = byte_values[index + 5]
                if monitoring:
                    print(f"{id_byte} : PWM | mosfet {val1}, pulse {val2}, LED {val3}, {val4}, {val5}")
                index += 6
                bufferData[id_byte].update({"mosfet": val1, "pulse": val2, "LED": [val3, val4, val5]})
            else:
                print("Incomplete data for header 'P'")
        
        elif header == 'R':
            if index + 6 <= len(byte_values):  # 총 6바이트를 읽어야 함
                val1 = int.from_bytes(byte_values[index:index + 2], byteorder='little')  # int16
                val2 = int.from_bytes(byte_values[index + 2:index + 4], byteorder='little')  # uint16
                val3 = byte_values[index + 4]  # uint8
                val4 = byte_values[index + 5]  # uint8
                if monitoring:
                    print(f"{id_byte} : EEPROM | origin Angle {val1/100}, origin Pulse {val2}, current Threshold {val3/10}, Max Network Loss {val4/10}")
                index += 6  # 6바이트를 읽었으므로 인덱스를 6 증가시킴
                bufferData[id_byte].update({"originAngle": val1/100, "originPulse": val2, "currentThreshold": val3/10, "maxNetworkLoss": val4/10})
            else:
                print("Incomplete data for header 'R'")
        
        elif header in 'ACT':
            if index + 1 <= len(byte_values):
                val1 = byte_values[index]
                if monitoring:
                    print(f"Header: {header} | Value: {val1}")
                index += 1
                bufferData[id_byte].update({header: val1})
            else:
                print(f"Incomplete data for header '{header}'")
        
        elif header in 'MVL':
            if monitoring:
                print(f"Write {header} command sent ")

        else:
            print(f"Unknown header: {header}")
    return bufferData


def onReceivedFromArduino(response):
    """Process the response from Arduino."""

    try:
        data = translate_response(response, monitoring)
        if data is not None: 

            arduino_response_recorder.append(data)
        else:        
            raise TypeError 
    except TypeError:
        print(data)
        print('translation cmd -> byteArr error')

    if command_queue:
        asyncio.create_task(process_command_queue())

def reset_serial_buffers():
    arduino_writer_global.transport.serial.reset_input_buffer()

    arduino_writer_global.transport.serial.reset_output_buffer()
    print("Resetting buffer")

#-----------------Input Producer-----------------
async def producer():
    while True:
        input = await aioconsole.ainput("Choose input stream (manual : m / auto : a / calibrate : c / reset : r): ")
        if input == "a" or input == "auto":
            await auto_input()
            
        elif input == "m" or input == "manual":
            await manual_input()
        elif input == "c":
            await calibrate_angle()
        elif input == "r":
            reset_serial_buffers()

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
            await go_to_posALL(goalPos)
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

            try:
                if parsed_input is not None: 
                    await send_command_to_arduino(parsed_input)
                    print(arduino_response_recorder)
                else:        
                    raise TypeError 
            except TypeError:
                print('parsing error')
                pass

async def main():
    uri = "ws://localhost:8001"
    
    #Open the serial port
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
