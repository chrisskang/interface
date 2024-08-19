def send_command_to_arduino(id, commands):

    if not (0 <= id <= 255):
        print(f"Error: ID {id} out of range. Must be between 0 and 255.")
        return

    if len(commands) == 0:
        print("Error: No commands provided.")
        return

    message = bytearray([id])  # ID를 uint8_t 형식으로 추가

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

    message.append(ord('\n'))
    print(f"Sent command: {message.hex()}")



if __name__ == "__main__":
   id = [1,]
   send_command_to_arduino()



