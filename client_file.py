import socket
import sys

HOST = '127.0.1.1'
PORT = 6542
ADDR = (HOST, PORT)
FORMAT = 'utf-8'
HEADER = 1024
SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def getPaddedLength(msg, format='utf-8'):
    msgInBinary = msg.encode(FORMAT)
    msgSize = sys.getsizeof(msgInBinary)
    msgSizeString = str(msgSize)
    requiredPaddingSize = HEADER - sys.getsizeof(''.encode(format)) - len(msgSizeString)
    padding = ' '.encode(format) * requiredPaddingSize
    msgSizePadded = padding + msgSizeString.encode(format)
    return msgSizePadded
    # it is already encoded


CLIENT = socket.socket()

CLIENT.connect(ADDR)
msg = input()
msgLength = getPaddedLength(msg)
# print(msgLength)
CLIENT.send(msgLength)
CLIENT.send(msg.encode(FORMAT))

recievedMsgLength = CLIENT.recv(1024)
bufferSize = int(recievedMsgLength)
recievedMsg = CLIENT.recv(bufferSize).decode(FORMAT)
print(recievedMsg)
