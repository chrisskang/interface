import socket
import struct

# 모터의 IP 주소와 포트 설정
MOTOR_IP = "192.168.0.2"  # 모터의 IP 주소
MOTOR_PORT = 3002         # 메뉴얼에서 명시된 사용자 라이브러리용 포트

# UDP 소켓 생성
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(2)  # 응답 대기 시간 설정

def parse_manual_command(command):
    """
    Parse manual command input and return frame and additional data.
    """
    parts = command.split()
    frame_type_str = parts[0]
    frame_type = int(frame_type_str[1:], 16)  # Skip the 'x' and convert to hex
    
    additional_data = []
    for part in parts[1:]:
        if 'x' in part:
            size, value = part.split('x')
            size = int(size)
            value = int(value)
            if size == 4:
                additional_data.extend(struct.pack('>I', value))
            elif size == 2:
                additional_data.extend(struct.pack('>H', value))
            elif size == 24:
                additional_data.extend(bytearray(24))  # 24-byte zero-filled
            elif size == 1:
                additional_data.append(value & 0xFF)  # Ensure value is 1 byte
            else:
                raise ValueError(f"Unsupported size: {size}")
        else:
            raise ValueError(f"Invalid format: {part}")

    return frame_type, additional_data

def get_frame_from_input():
    """
    Get the frame data based on user input.
    """
    command = input("Enter command (stop, en 1, en 0, info, x<frame_type> [size x data]): ").strip()

    if command.lower() == 'stop':
        frame_type = 0x31
        additional_data = []

    elif command.lower().startswith('run'):
        try:
            _, val1, val2 = command.split()
            val1 = int(val1)
            val2 = int(val2)
            # Check values are within 4-byte integer range
            if not (0 <= val1 <= 0xFFFFFFFF) or not (0 <= val2 <= 0xFFFFFFFF):
                raise ValueError("Values must be within the 4-byte integer range (0 to 4294967295).")
            frame_type = 0x35
            additional_data = struct.pack('>II', val1, val2)
        except (ValueError, IndexError):
            print("Invalid 'run' command format. Use 'run <val1> <val2>' with values in range 0 to 4294967295.")
            return None

    elif command.lower() == 'info':
        frame_type = 0x05
        additional_data = []

    elif command.lower().startswith('en'):
        try:
            _, value = command.split()
            value = int(value)
            if value not in (0, 1):
                raise ValueError("Invalid value for 'en' command. Must be 0 or 1.")
            frame_type = 0x2A
            additional_data = [value]
        except (ValueError, IndexError):
            print("Invalid 'en' command format. Use 'en 0' or 'en 1'.")
            return None

    elif command.lower().startswith('x'):
        try:
            frame_type, additional_data = parse_manual_command(command)
        except ValueError as e:
            print(f"Error parsing manual command: {e}")
            return None

    else:
        print("Invalid command format.")
        return None

    # 프레임 구성
    # Header: 0xAA, Length: 3 (기본 바이트 3개) + 추가 데이터 길이, Sync No: 0x01, Reserved: 0x00
    header = 0xAA
    sync_no = 0x01
    reserved = 0x00
    length = 3 + len(additional_data)  # 기본 길이 3 바이트 + 추가 데이터 길이
    frame = bytearray([header, length, sync_no, reserved, frame_type] + list(additional_data))

    return frame

def parse_frame(frame):
    """
    Parse received frame into components.
    """
    header = frame[0]
    length = frame[1]
    sync_no = frame[2]
    reserved = frame[3]
    frame_type = frame[4]
    additional_data = frame[5:]

    return header, length, sync_no, reserved, frame_type, additional_data

def process_additional_data(frame_type, additional_data):
    """
    Process additional data based on frame type.
    """
    if additional_data:
        status = additional_data[0]
        print(f"Communication status: {status:02X}")
        
        if frame_type in {0x51, 0x53, 0x54, 0x56}:
            if len(additional_data) >= 5:
                # Extract 4-byte integers
                values = []
                for i in range(1, len(additional_data), 4):
                    if i + 3 < len(additional_data):
                        value = struct.unpack('>I', bytes(additional_data[i:i+4]))[0]
                        values.append(value)
                print(f"Additional data (4-byte numbers): {values}")
            else:
                print("Error: Not enough data for 4-byte number.")
        elif frame_type == 0x81:
            try:
                num1, num2, num3 = struct.unpack('>III', bytes(additional_data[:12]))
                num4, num5 = struct.unpack('>HH', bytes(additional_data[12:16]))
                data = additional_data[16:40]
                
                print(f"4-byte numbers: {num1}, {num2}, {num3}")
                print(f"2-byte numbers: {num4}, {num5}")
                print(f"24-byte data: {data.hex()}")
            except struct.error as e:
                print(f"Error parsing additional data for frame type 0x81: {e}")
        else:
            # Display additional data in hex format
            print("Additional data:", " ".join(f"{byte:02X}" for byte in additional_data))
    else:
        print("No additional data.")

try:
    while True:
        # 사용자 입력으로부터 프레임 구성
        frame = get_frame_from_input()
        if frame is None:
            print("Skipping invalid input.")
            continue  # 잘못된 입력이 들어오면 다시 명령어를 입력받음
        
        if frame == 'exit':
            print("Exiting...")
            break
        
        # 송신 데이터 출력
        print("Sending frame:", " ".join(f"{byte:02X}" for byte in frame))
        
        # 모터로 프레임 송신
        try:
            sock.sendto(frame, (MOTOR_IP, MOTOR_PORT))
        except Exception as e:
            print(f"Failed to send frame: {e}")
            continue
        
        # 응답 수신 대기
        try:
            response, addr = sock.recvfrom(1024)
            # 응답 파싱
            response_header, _, response_sync_no, response_reserved, response_frame_type, response_additional_data = parse_frame(response)
            
            # 송신 프레임 파싱
            sent_header, _, sent_sync_no, sent_reserved, sent_frame_type, _ = parse_frame(frame)

            # 송신과 수신 데이터 비교
            if (response_header == sent_header and
                response_sync_no == sent_sync_no and
                response_reserved == sent_reserved and
                response_frame_type == sent_frame_type):
                # 수신 데이터 처리
                print(f"Received frame type: {response_frame_type:02X}")
                process_additional_data(response_frame_type, response_additional_data)
            else:
                print("Error: Received frame does not match the sent frame.")
                print(f"Sent frame: {' '.join(f'{byte:02X}' for byte in frame)}")
                print(f"Received frame: {' '.join(f'{byte:02X}' for byte in response)}")
        
        except socket.timeout:
            print("No response received. Please check the connection.")
        except Exception as e:
            print(f"Failed to receive or process response: {e}")

finally:
    sock.close()
