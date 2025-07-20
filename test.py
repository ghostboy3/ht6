import rpi_gpio as GPIO
import socket
import time
print("hello world ")

HOST = '0.0.0.0'  # Listen on all interfaces
PORT = 5001       # Pick an unused port
LED_PIN = 17
GPIO.setup(LED_PIN, GPIO.OUT)


def on():
    GPIO.output(LED_PIN, GPIO.HIGH)
    time.sleep(0.5)
def off():
    GPIO.output(LED_PIN, GPIO.LOW)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Listening on {HOST}:{PORT}...")
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        off()
        while True:
            data = conn.recv(1024)
            if not data:
                break
            message = data.decode().strip().lower()
            print(message)
            if message == 'on':
                on()
                print("Received:", data.decode())
            else:
                off()
                # print("Received:", data.decode())