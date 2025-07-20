print("hi from main")
import socket

HOST = '10.33.48.24'  # Replace with Raspberry Pi's IP
PORT = 5001

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b'Hello from Ubuntu!')
    print("Message sent.")
