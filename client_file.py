import socket
import sys
import threading
import time
import queue


HOST = '127.0.1.1'
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


class Client:
    def __init__(self, addr):
        self.clientSocket = socket.socket()
        self.clientSocket.connect(addr)

    def sendMessage(self):
        while True:
            msg = SEND_MESSAGE_QUEUE.get()
            self.clientSocket.send(msg)
            time.sleep(1)

    def inputMessage(self):
        while True:
            msg = input()
            msgWithHeader = addHeader(msg, encoding=True)
            SEND_MESSAGE_QUEUE.put(msgWithHeader)

    def printMessage(self):
        while True:
            Message = RECIVE_MESSAGE_QUEUE.get()
            print(Message)
            time.sleep(1)

    def recieveMessage(self):
        fullMessage = ''
        while True:
            msg = self.clientSocket.recv(43)
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

    def runThreads(self):
        recieveMessageThread = threading.Thread(target=self.recieveMessage, daemon=True)
        sendMessageThread = threading.Thread(target=self.sendMessage, daemon=True)
        printMessageThread = threading.Thread(target=self.printMessage, daemon=True)
        inputMessageThread = threading.Thread(target=self.inputMessage, daemon=True)

        recieveMessageThread.start()
        sendMessageThread.start()
        printMessageThread.start()
        inputMessageThread.start()

        recieveMessageThread.join()
        sendMessageThread.join()
        printMessageThread.join()
        inputMessageThread.join()


client = Client(ADDR)
client.runThreads()
