import serial
import time

# Serial port settings
SERIAL_PORT = 'COM99'  # Change this to your actual port
BAUD_RATE = 115200
TIMEOUT = 1  # Adjusted timeout

# Serial object creation
ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=TIMEOUT)

def send_command(id, commands):
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

        if header in ['A', 'V']:
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

    ser.write(message)  # 바이트 배열을 전송
    print(f"Sent command: {message.hex()}")

def read_response():
    """ Read the response from the Arduino. """
    response = ser.read_until(b'\n').decode(errors='ignore').strip()  # Read until newline
    if response:
        print(f"Received response: {response}")
        return response
    return None

def send_command_and_measure_time(id, commands):
    """ Send a command and measure the time taken to receive the response.
    
    :param id: ID to send data to (uint8_t)
    :param commands: List of (header, value) tuples
    """
    send_command(id, commands)
    
    start_time = time.time()  # Record the start time
    response = None
    
    # Wait for response with a timeout
    response = read_response()

    end_time = time.time()  # Record the end time
    elapsed_time = end_time - start_time
    if response:
        print(f"Response received in {elapsed_time:.4f} seconds.")
    else:
        print(f"No response received within {TIMEOUT} seconds.")

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

def main():
    try:
        while True:
            user_input = input("Enter command (e.g., '1 S', '1 A324', '1 C32', '1 A324 C32', '1 L0,100,250'): ").strip()
            if user_input:
                id, commands = parse_input(user_input)
                if id is not None and commands:
                    send_command_and_measure_time(id, commands)
    except KeyboardInterrupt:
        print("Program interrupted.")
    finally:
        ser.close()
        print("Serial port closed.")

if __name__ == "__main__":
    main()
