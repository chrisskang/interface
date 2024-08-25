import socket

# 모터의 IP 주소와 포트 설정
MOTOR_IP = "192.168.0.2"  # 모터의 IP 주소
MOTOR_PORT = 3002         # 메뉴얼에서 명시된 사용자 라이브러리용 포트

# UDP 소켓 생성
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(2)  # 응답 대기 시간 설정

# 간단한 통신 확인을 위한 프레임 (예: 모터 상태 요청)
# 0xAA, Length, Sync No, 0X00, frame type, data
frame = bytearray([0xAA,    # Header, 0xAA 
                   0x04,    # Length
                   0x01,    # Sync No
                   0x00,    # Reserved, 0x00
                   0x2A,    # frame type, 0x05: 모터 상태 요청
                   0x00
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
