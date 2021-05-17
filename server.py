import socket
import cv2
import pickle
import struct
from pyzbar import pyzbar
import imutils

# Socket Create
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
print('HOST IP:', host_ip)
port = 9999
socket_address = (host_ip, port)

# Socket Bind
server_socket.bind(socket_address)

# Socket Listen
server_socket.listen(5)
print("LISTENING AT:", socket_address)


def read_barcodes(frame):
    barcodes = pyzbar.decode(frame)
    for barcode in barcodes:
        x, y, w, h = barcode.rect
        barcode_text = barcode.data.decode('utf-8')
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    return frame


# Socket Accept
while True:
    client_socket, addr = server_socket.accept()
    print('GOT CONNECTION FROM:', addr)
    if client_socket:
        vid = cv2.VideoCapture(0)

        while(vid.isOpened()):
            img, frame = vid.read()

            frame = imutils.resize(frame, width=600)
            img = read_barcodes(frame)

            a = pickle.dumps(img)
            message = struct.pack("Q", len(a))+a
            client_socket.sendall(message)

            cv2.imshow('TRANSMITTING VIDEO', img)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                client_socket.close()
