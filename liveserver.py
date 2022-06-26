import socket
import json
import keyboard
import time
import base64
import cv2
import numpy as np

HOST = "0.0.0.0"  # Standard loopback interface address (localhost)
PORT = 87  # Port to listen on (non-privileged ports are > 1023)


# Collect events until released
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    conn.send(b"OK")
    while True:
        adata = ""
        while True:
            data = conn.recv(1024).decode("utf-8")
            if not data:
                break
            adata += data
            if adata.endswith("Ths is the end of the json and the whole byte thingy lol"):
                adata = adata[:-56]
                break
        conn.send(b"OK")
        datajson = json.loads(adata)
        png_bytes = base64.b64decode(datajson["imgstream"])
        array = np.asarray(bytearray(png_bytes), dtype=np.uint8)
        image = cv2.imdecode(array, cv2.IMREAD_COLOR)
        cv2.imshow('Image', image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        

    


