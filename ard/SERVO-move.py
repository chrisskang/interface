import socket

# 모터 드라이버의 IP 주소와 포트 설정
MOTOR_IP = "192.168.0.2"
MOTOR_PORT = 3002

# UDP 소켓 생성
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(2)  # 응답 대기 시간 설정

# 모터 이동 명령어 프레임 구성
# 예: 모터를 위치 500으로 이동, 속도는 100으로 설정
relative_position  = 100  # 이동할 목표 위치
speed = 10     # 모터 속도

frame = bytearray([
    0xAA,               # Header
    0x0B,               # Length (프레임 타입과 8바이트 데이터 포함)
    0x01,               # Sync No
    0x00,               # Reserved
    0x35,               # Frame type: MoveSingleAxisIncPos
    (relative_position >> 24) & 0xFF,   # 상대위치 MSB
    (relative_position >> 16) & 0xFF,   # 상대위치
    (relative_position >> 8) & 0xFF,    # 상대위치
    relative_position & 0xFF,           # 상대위치 LSB
    (speed >> 24) & 0xFF,               # 속도 MSB
    (speed >> 16) & 0xFF,               # 속도
    (speed >> 8) & 0xFF,                # 속도
    speed & 0xFF                        # 속도 LSB
])

try:
    # 모터로 프레임 송신
    sock.sendto(frame, (MOTOR_IP, MOTOR_PORT))
    
    # 응답 수신 대기
    response, addr = sock.recvfrom(1024)
    
    # 응답 출력
    print("Received response:", response)
    
except socket.timeout:
    print("No response received. Please check the connection.")
    
finally:
    sock.close()
