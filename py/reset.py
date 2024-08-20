import serial
import time

def reset_arduino(port='COM4', baudrate=9600):
    """
    Perform a hard reset on the Arduino by toggling the DTR line.
    
    Args:
        port (str): The port where the Arduino is connected.
        baudrate (int): The baud rate for serial communication.
    """
    try:
        # Open the serial port with DTR initially set to False
        with serial.Serial(port, baudrate, dsrdtr=True) as ser:
            # Assert the DTR line (LOW)
            ser.dtr = False
            time.sleep(0.1)  # Small delay
            # Deassert the DTR line (HIGH) to reset the Arduino
            ser.dtr = True
            time.sleep(2)  # Give Arduino time to boot up

        print("Arduino reset successfully.")

    except serial.SerialException as e:
        print(f"Error: {e}")

# Usage
reset_arduino(
    
)  # Update port and baudrate as needed
