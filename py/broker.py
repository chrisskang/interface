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

import serial
import time

# Serial port settings
SERIAL_PORT = 'COM4'  # Change this to your actual port
BAUD_RATE = 9600
TIMEOUT = 1  # Adjusted timeout

monitoring = False
start_time = 0
end_time = 0

# Serial object creation
#ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=TIMEOUT)

async def send_command(id, commands):
    """ Send commands to a specified ID.

    :param id: ID to send data to (uint8_t)
    :param commands: List of (header, value) tuples
    """
    if not (0 <= id <= 255):
        print(f"Error: ID {id} out of range. Must be between 0 and 255.")
        return

    if len(commands) == 0:
        print("Error: No commands provided.")
        return

    message = bytearray()
    message.append(id)  # ID를 uint8_t 형식으로 추가

    for header, value in commands:
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
                values = list(map(int, value.split(',')))
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

    # 패킷 종결자를 추가 (e.g., newline character)
    message.append(ord('\n'))

    if monitoring: print([hex(b) for b in message])

    ser.write(message)  # 바이트 배열을 전송
    # print(f"Sent command: {message.hex()}")
    # 1바이트 단위로 끊어서 출력
    #formatted_message = ' '.join(f'{byte:02x}' for byte in message)
    #print(f"Sent command: {formatted_message}")

async def read_response():
    """Read the response from the Arduino."""
    response = bytearray()
    
    while True:
        chunk = ser.read(1)
        if not chunk:
            break  # Stop reading if no data is available
        
        response.extend(chunk)
        
        # Check if the end of message indicator (0xFF 0xFF) is found
        if len(response) >= 3 and response[-3:] == b'\x99\x88\xFF':
            response = response[:-3]  # Remove the end indicator
            break
    
    if response:
        if monitoring: print(f"Received raw response: {response.decode(errors='ignore')}")
        byte_values = [f"0x{byte:02X}" for byte in response]  # 각 바이트를 hex로 변환
        if monitoring: 
            print("Byte-by-byte breakdown:")
            print(' '.join(byte_values))  # 바이트를 공백으로 구분하여 출력
        
        process_response(response)
    else:
        print("No response received.")

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

def send_command_and_measure_time(id, commands):
    """ Send a command and measure the time taken to receive the response.
    
    :param id: ID to send data to (uint8_t)
    :param commands: List of (header, value) tuples
    """
    send_command(id, commands)
    
    start_time = time.time()  # Record the start time
    response = read_response()  # Wait for response with a timeout

def parse_input(user_input):
    """ Parse user input into ID and list of (header, value) tuples.
    
    :param user_input: Input string from user
    :return: Tuple of ID and list of (header, value) tuples
    """
    parts = user_input.split()
    if len(parts) < 2:
        print("Error: Input must contain at least ID and one command.")
        return None, []

    try:
        id = int(parts[0])
    except ValueError:
        print("Error: ID should be an integer.")
        return None, []

    commands = []
    for part in parts[1:]:
        header = part[0]
        value = part[1:].strip() if len(part) > 1 else ''
        commands.append((header, value))
    
    return id, commands





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
    msgBuffer = json.dumps(message)
    if "toArd" in msgBuffer:
        await sendToArduino(msgBuffer)
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
        input = await aioconsole.ainput("Choose input stream (manual : m / auto : a): ")

        if input == "a" or input == "auto":
            asyncio.create_task(send_loop_between(180, 2, loopBetween))
            print("Sending values 0-4 in the background. You can continue entering commands.")

        elif input == "" or input == "m" or input == "manual":
            await ardInput()
            
        else:
            print("Invalid input")

async def ardInput():
    user_input = await aioconsole.ainput("Enter command (e.g., '1 S', '1 A324', '1 C32', '1 A324 C32', '1 L0,100,250'): ")
    if user_input:
        if user_input == '?':
            print("Read Commands:")
            print("  S (sensor)")
            print("  P (pwm)")
            print("  R (eeprom)")

            print("Write Commands:")
            print("  A ( int16: origin Angle) -32768 ~ 32767 : angle*100")
            print("  U ( int16: origin Pulse)")
            print("  C (uint8 : currentThreshold) 0 ~ 255 : A*10")
            print("  T (uint8 : MaxNetwork) 0 ~ 255 : max 25.5sec")
            print("  M (uint8 : mosfet) 0 | 1")
            print("  V (uint16: pulse) 500 ~ 2500")
            print("  L (uint8 : LED) 0 ~ 255 : L0,10,100")

        id, commands = parse_input(user_input)

        if id is not None and commands:
            start_time = time.time()
            await send_command(id, commands)
            response = await read_response()
            end_time = time.time()  # Record the end time
            elapsed_time = end_time - start_time
            print(f"Response received in {elapsed_time:.4f} seconds.")
            #send_command_and_measure_time(id, commands)

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
