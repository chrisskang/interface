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

from utils import lerp, parse_input

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

#-----------------Arduino Communication-----------------

async def send_command_to_arduino(inputList):

    global command_queue
    for cmdList in inputList:
        command_queue.append(cmdList)
    
    if not command_in_progress:
        await process_command_queue()
    
    
    # if monitoring: print([hex(b) for b in message])
async def process_command_queue():
    
    global command_in_progress
    
    while command_queue:
        command_in_progress = True
        cmdList = command_queue.popleft()
        
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
        
        # Send the command
        arduino_writer_global.write(message)
        print(f"Sent command: {message.hex()}")
        
        # Wait for response
        await wait_for_response()
    
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
                print_debug_info(response)
                process_response(response)
                return
            print(f"Attempt {attempt+1}/{max_retry}: No response received.")

        except asyncio.TimeoutError:
            print(f"Attempt {attempt+1}/{max_retry}: Timeout occurred. Retrying...")
            continue  # Retry only on timeout

        break  # Break the loop if no timeout occurred, regardless of the content

    print("Max retries reached. Exiting without a successful response.")

async def listen_from_arduino():
    while True:
        await wait_for_response()

def process_response(response):
    """Process the response from Arduino."""

    # response를 바이트 단위로 변환
    byte_values = [b for b in response]
    
    if len(byte_values) < 2:
        print("Response is too short to process.")
        return
    
    id_byte = byte_values[0]

    # ID가 0~36 사이가 아니거나 데이터 길이가 2보다 작으면 종료
    if not (0 <= id_byte <= 36) or len(byte_values) < 2:
        print("Invalid ID or response length.")
        return
    
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
            else:
                print("Incomplete data for header 'R'")
        
        elif header in 'ACT':
            if index + 1 <= len(byte_values):
                val1 = byte_values[index]
                print(f"Header: {header} | Value: {val1}")
                index += 1
            else:
                print(f"Incomplete data for header '{header}'")
        
        else:
            print(f"Unknown header: {header}")
    if command_queue:
        asyncio.create_task(process_command_queue())



#-----------------Input Producer-----------------
async def producer():
    while True:
        input = await aioconsole.ainput("Choose input stream (manual : m / auto : a): ")
        if input == "a" or input == "auto":
            asyncio.create_task(send_loop_between(180, 2, loopBetween))
            print("Sending values 0-4 in the background. You can continue entering commands.")
        elif input == "" or input == "m" or input == "manual":
            await ard_input()
        else:
            print("Invalid input")

async def ard_input():
    user_input = await aioconsole.ainput("Enter command (e.g., '1:S', '1:A324', '1:A324,C32', '1:A324 2:C32'): ")
    if user_input:
        if user_input == '?':
            print("Read : S (sensor) P (pwm) R (eeprom)")
            print("Write : A (origin Angle) U (origin Pulse) C (currentThreshold) T (MaxNetwork) M (mosfet) V (pulse) L (LED)")
                    
        else:       
            parsed_input = parse_input(user_input)  
            if parsed_input is not None:
                await send_command_to_arduino(parsed_input)
            else:
                return

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

        await asyncio.gather(server_task, user_input_task)
        
        #await asyncio.gather(server_task, user_input_task)
    # except Exception as e:
    #     print(f"An error occurred: {e}")
    


if __name__ == "__main__":
    asyncio.run(main())
