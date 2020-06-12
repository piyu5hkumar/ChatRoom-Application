import socket
import queue
import threading
import time
import sys


HOST = socket.gethostbyname(socket.gethostname())
PORT = 6542
ADDR = (HOST, PORT)
FORMAT = 'utf-8'
HEADER_LENGTH = 10

SEND_MESSAGE_QUEUE = queue.Queue()
RECIVE_MESSAGE_QUEUE = queue.Queue()


def addHeader(msg, format='utf-8', encoding=False):
    msgLength = len(msg)
    msgHeader = f'{len(msg):<{HEADER_LENGTH}}'
    msgWithHeader = msgHeader + msg

    if encoding:
        return msgWithHeader.encode(FORMAT)

    return msgWithHeader


def sendMessage():
    while True:
        msg = SEND_MESSAGE_QUEUE.get()
        conn.send(msg)
        time.sleep(1)


def inputMessage():
    while True:
        msg = input()
        msgWithHeader = addHeader(msg, encoding=True)
        SEND_MESSAGE_QUEUE.put(msgWithHeader)


def printMessage():
    while True:
        Message = RECIVE_MESSAGE_QUEUE.get()
        print(f'[CLIENT({addr[0]})]:', Message)
        time.sleep(1)


def recieveMessage():
    fullMessage = ''
    while True:
        msg = conn.recv(43)
        fullMessage += msg.decode(FORMAT)

        while fullMessage != '':
            msgLength = int(fullMessage[:HEADER_LENGTH])
            chunkLength = HEADER_LENGTH + msgLength

            if chunkLength > len(fullMessage):
                break
            else:
                chunk = fullMessage[:chunkLength]
                Message = chunk[HEADER_LENGTH:]
                RECIVE_MESSAGE_QUEUE.put(Message)
                fullMessage = fullMessage[chunkLength:]


SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SERVER.bind(ADDR)
print(ADDR)
SERVER.listen(5)
print(f"[SERVER]: is listening at port: {PORT}")

conn, addr = SERVER.accept()
print(f"[CLIENT]: {addr[0]} is connected from port: {addr[1]}")

recieveMessageThread = threading.Thread(target=recieveMessage, daemon=True)
sendMessageThread = threading.Thread(target=sendMessage, daemon=True)
printMessageThread = threading.Thread(target=printMessage, daemon=True)
inputMessageThread = threading.Thread(target=inputMessage, daemon=True)

recieveMessageThread.start()
sendMessageThread.start()
printMessageThread.start()
inputMessageThread.start()

recieveMessageThread.join()
sendMessageThread.join()
printMessageThread.join()
inputMessageThread.join()
