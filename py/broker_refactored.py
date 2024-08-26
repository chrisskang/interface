from collections import deque
import random
import time
import aioconsole
import serial_asyncio
import asyncio
import websockets
import json

SERIAL_PORT = "COM5"
BAUD_RATE = 9600
uri = "ws://localhost:8001"

#-----------------Global Variables-----------------
twistPos = {"type": "angles", "angles": [{"a": 30, "t": 1}, {"a": 60, "t": 1}, {"a": -60, "t": 1}, {"a": 15, "t": 1}, {"a": 15, "t": 1}, {"a": 15, "t": 1}, {"a": -15, "t": 1}, {"a": -15, "t": 1}, {"a": -15, "t": 1}, {"a": -15, "t": 1}, {"a": -15, "t": 1}, {"a": -15, "t": 1}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": -15, "t": 1}, {"a": -15, "t": 1}, {"a": -15, "t": 1}, {"a": -15, "t": 1}, {"a": -15, "t": 1}, {"a": -15, "t": 1}, {"a": 15, "t": 1}, {"a": 15, "t": 1}, {"a": 15, "t": 1}, {"a": -60, "t": 1}, {"a": 60, "t": 1}, {"a": 30, "t": 1}]}

liftPos = {"type": "angles", "angles": [{"a": 30, "t": 1}, {"a": -15, "t": 1}, {"a": 15, "t": 1}, {"a": 15, "t": 1}, {"a": -30, "t": 1}, {"a": 15, "t": 1}, {"a": -15, "t": 1}, {"a": 15, "t": 1}, {"a": -15, "t": 1}, {"a": 30, "t": 1}, {"a": -15, "t": 1}, {"a": 15, "t": 1}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": 0, "t": 0}, {"a": -15, "t": 1}, {"a": 15, "t": 1}, {"a": -30, "t": 1}, {"a": 15, "t": 1}, {"a": -15, "t": 1}, {"a": 15, "t": 1}, {"a": -15, "t": 1}, {"a": 30, "t": 1}, {"a": -15, "t": 1}, {"a": -15, "t": 1}, {"a": 15, "t": 1}, {"a": -30, "t": 1}]}

command_queue = deque()
command_in_progress = False

monitoring = True
arduino_response_recorder = None

MAX_SEND_RETRIES = 2
BACKOFF_FACTOR = 1.1

TIMEOUT = 0.2

#-----------------Server Functions-----------------
async def server_login(websocket):
    loginData = {"type": "login","client":"py" }
    loginData = json.dumps(loginData)
    await websocket.send(loginData)

async def listen_from_server():

    async for message in websocket_global:
        await serverOnReceived(message)

async def serverOnReceived(message):
    print ("Received message from server: {0}".format(message))
    print ("")

#-----------------Arduino Functions-----------------
async def send_command_to_arduino(cmdList):
    #cmdList example : [{"id": 1, "commands": [("S", ""), ("P", "")]}, {"id": 2, "commands": [("P", ""), ("R", "")]}]
    global command_queue
    global command_in_progress

    for cmds in cmdList:
        command_queue.append(cmds)

    if not command_in_progress:
        command_in_progress = True
        await process_command_queue()

async def process_command_queue():
    global command_queue
    global command_in_progress
    global arduino_response_recorder
    failed = []

    while command_queue:
        
        cmd = command_queue[0]
        byteMsg = await command_to_bytearray(cmd)
        targetID = cmd['id']

        # Flush any remaining data in the buffer
        await flush_incoming_data()
        # Send command
        arduino_writer_global.write(byteMsg)
        await arduino_writer_global.drain()
        if arduino_response_recorder is not None:
            arduino_response_recorder.clear()
        
        if monitoring:
            print(f"Sent command: {cmd, byteMsg.hex()}")
        
        response = await wait_for_response(targetID)
        
        if response is not None:
            if monitoring:
                print(f"Command successful: {cmd}, Response: {response.hex()}")
            arduino_response_recorder = await translate_response(response)
            command_queue.popleft() #delete the command that has been sent

        else:
            print(f"Command failed on: {cmd["id"]} / maintenance and moving to the end")
            await perform_maintenance(cmd["id"])
            if "attempt" not in cmd:
                cmd["attempt"] = 1
            else:
                cmd["attempt"] += 1
            command_queue.append(command_queue.popleft()) #move the command to the end of the queue
        
        if "attempt" in cmd:
            if cmd["attempt"] >= MAX_SEND_RETRIES:
                failed.append(cmd['id'])
                command_queue.remove(cmd)
        
        if not command_queue and failed:
            print(f"Reached maximum retries on all, Command failed on : {', '.join(str(id) for id in failed)}")

    command_in_progress = False

async def wait_for_response(targetID):

    PACKET_END = b'\x99\x88\xFF'

    response = bytearray()
    start_time = time.time()

    while True:
        try:

            chunk = await asyncio.wait_for(arduino_reader_global.read(1), timeout=TIMEOUT)
            if not chunk:
                break
            response.extend(chunk)
            
            if len(response) >= len(PACKET_END) and response[-len(PACKET_END):] == PACKET_END:
                if len(response) >= 5 and int(targetID) == response[0]:
                    end_time = time.time()
                    #print(f"Response received in {end_time - start_time:.4f} seconds.")
                    return response[:-3]
                else:
                    print("Response received but not for the target ID or invalid format.")
                    return None
        
        except asyncio.TimeoutError:
            break
    return None

async def perform_maintenance(id):
    print (f"Performing maintenance... on {id}")
    await asyncio.sleep(0.1)

async def flush_incoming_data():
    """Flushes any remaining data in the buffer."""
    try:
        while arduino_reader_global.at_eof() is False:
            await asyncio.wait_for(arduino_reader_global.read(100), timeout=0.1)
    except asyncio.TimeoutError:
        pass  # Timeout is expected when the buffer is empty
#------------------Move Functions------------------
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

async def calibrate(id, pulse):

    #check if origin is calibrated
    data = await getArduinoData(id, "originPulse")
    if data > 1300 and data < 1700:
        print ("Origin is calibrated")

    #turn mosfet off
    await send_command_to_arduino([{"id": id, "commands": [("M", 0)]}])
    await asyncio.sleep(1)
    
    #check mosfet turned off
    if await getArduinoData(id, "mosfet"):
        print("mosfet is not turned off")
        return
    else:
        print("mosfet is successfully turned off")
    
    pulseReady = await set_pulse_to_current_angle(id)
    await asyncio.sleep(1)

    mosfetData = await turn_on_mosfet(id, pulseReady)
    print (mosfetData)
    # if await turnOnMosfet(id):
    #     await asyncio.sleep(1)
    #     goal = 500
    #     print("mosfet is on and driving to ", goal)

    #     await single_driveTo(id, goal, False)
    #     #TODO record position

    # return

async def checkAll():
    #get status of all

    status = []

    for i in range(1, 37):
    
        await send_command_to_arduino([{"id": i, "commands": [("S", ""),("P", ""),("R", "")]}])

        if arduino_response_recorder is not None and i in arduino_response_recorder:
            status.append(arduino_response_recorder.copy())

    for record in status:
        print(record)
            


    

#------------------Control Functions---------------
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

    if arduino_response_recorder is None:
        print("No response from arduino")
        return None

    if id in arduino_response_recorder:
        return arduino_response_recorder[id][requestType]
    else:
        print("Response id do not match")

async def turn_on_mosfet(id,pulseReady):
    if pulseReady:
        await send_command_to_arduino([{"id": id, "commands": [("M", 1)]}])
        await asyncio.sleep(0.5)
        return await getArduinoData(id, "mosfet")
    else:
        print("Pulse is not ready")
        return False

async def set_pulse_to_current_angle(id):
    current_angle = await getArduinoData(id, "angle")
    current_pulse = await angle_to_pulse(current_angle)

    #set pulse to match current position
    await send_command_to_arduino([{"id": id, "commands": [("V", current_pulse)]}])

    return abs(await getArduinoData(id, "pulse")-int(current_pulse)) < 10

#------------------Util Functions------------------
async def parse_manual_input(user_input):
    #input format: 1:S, 1:A324, 1:A324,C32, 1:A324 2:C32
    
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
    
    #output format: [{'id': '1', 'commands': [('S', ''), ('A', '324')]}, {'id': '2', 'commands': [('C', '32')]}]
    return cmdList

async def command_to_bytearray(cmdList):
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

async def translate_response(response):
    if response is None:
        return None
    
    byte_values = [b for b in response]
    
    if len(byte_values) < 2:
        print("Response is too short to process.")
        return None
    
    id_byte = byte_values[0]

    if not (0 <= id_byte <= 36) or len(byte_values) < 2:
        print("Invalid ID or response length.")
        return None
    
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

async def angle_to_pulse(a):
    #angle per 50 == 4.1
    PulsePerDegree = 12.2
    return PulsePerDegree*a

#------------------User Input Functions------------------
async def producer():
    while True:
        input = await aioconsole.ainput("Choose input stream (manual : m / auto : a / calibrate : c / checkAll : q): ")
        if input == "a" or input == "auto":
            await auto_input()
        elif input == "m" or input == "manual":
            await manual_input()
        elif input == "c":
            await calibrate_input()
        elif input == "q":
            await checkAll()
        else:
            print("Invalid input")

async def auto_input():
    pos_input = await aioconsole.ainput("Select Pos - Twist(T) / Lift(L) / Random(R): ")
    if pos_input == "T" or pos_input == "t":
        goalPos = twistPos
    elif pos_input == "L" or pos_input == "l":
        goalPos = liftPos
    elif pos_input == "R" or pos_input == "r":
        angleToggleInput = await aioconsole.ainput("Input max angle range / number of toggle (eg. 30/18): ")

        maxangle = int(angleToggleInput.split("/")[0])
        numToggle = int(angleToggleInput.split("/")[1])

        goalPos = {"type": "angles", "angles": []}

        if numToggle > 36:
            raise ValueError("The number of toggles cannot exceed the total number of motors (36).")

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
        else:
            print("Invalid input")

async def manual_input():
    manual_command = await aioconsole.ainput("Enter command (e.g., '1:S', '1:A324', '1:A324,C32', '1:A324 2:C32'): ")
    if manual_command:
        if manual_command == '?':
            print("Read : S (sensor) P (pwm) R (eeprom)")
            print("Write : A (origin Angle) U (origin Pulse) C (currentThreshold) T (MaxNetwork) M (mosfet) V (pulse) L (LED)")
                    
        else:       
            parsed_input = await parse_manual_input(manual_command)
   
            if parsed_input is not None: 
                await send_command_to_arduino(parsed_input)
            else:        
                print("Invalid input")
   

async def calibrate_input():
    user_input = await aioconsole.ainput("Enter id and pulse (eg. 32/200): ")
    if user_input:
        id = int(user_input.split("/")[0])
        pulse = int(user_input.split("/")[1])
    
        await calibrate(id, pulse)



async def main():
    uri = "ws://localhost:8001"
    
    #Open the serial port
    arduino_reader, arduino_writer = await serial_asyncio.open_serial_connection(
    url=SERIAL_PORT, baudrate=BAUD_RATE
    )

    global arduino_reader_global, arduino_writer_global
    arduino_reader_global = arduino_reader
    arduino_writer_global = arduino_writer
    
    async with websockets.connect(uri) as websocket:
        await server_login(websocket)
        global websocket_global
        websocket_global = websocket

        server_task = asyncio.create_task(listen_from_server())

        user_input_task = asyncio.create_task(producer())

        await asyncio.gather(server_task, user_input_task)

    


if __name__ == "__main__":
    asyncio.run(main())
