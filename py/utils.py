#all the non async helper functions are here
import json

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
