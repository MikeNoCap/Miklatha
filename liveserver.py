import socket
import json
import keyboard
import time

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 87  # Port to listen on (non-privileged ports are > 1023)

amount = 1


# Collect events until released
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    while True:
        if keyboard.is_pressed("UP"):
            conn.send(json.dumps({"device": "MOUSE", "move": "UP"}).encode("utf-8"))
            conn.recv(1024)
        if keyboard.is_pressed("RIGHT"):
            conn.send(json.dumps({"device": "MOUSE", "move": "RIGHT"}).encode("utf-8"))
            conn.recv(1024)
        if keyboard.is_pressed("DOWN"):
            conn.send(json.dumps({"device": "MOUSE", "move": "DOWN"}).encode("utf-8"))
            conn.recv(1024)
        if keyboard.is_pressed("LEFT"):
            conn.send(json.dumps({"device": "MOUSE", "move": "LEFT"}).encode("utf-8"))
            conn.recv(1024)
    


