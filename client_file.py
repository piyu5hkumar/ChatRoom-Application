import socket
import sys
import threading
import time
import queue
from tkinter import *

HOST = '127.0.1.1'
PORT = 6542
ADDR = (HOST, PORT)
FORMAT = 'utf-8'
HEADER_LENGTH = 10


SEND_MESSAGE_QUEUE = queue.Queue()
RECIVE_MESSAGE_QUEUE = queue.Queue()





class Client:
    def __init__(self):
        self.clientSocket = socket.socket()
        self.state = 'disconnected'

    def connectToServer(self, ADDR):
        self.clientSocket.connect(ADDR)

    def disconnectFronServer(self):
        self.clientSocket.close()

    def addHeader(self, msg, format='utf-8', encoding=False):
        msgLength = len(msg)
        msgHeader = f'{len(msg):<{HEADER_LENGTH}}'
        msgWithHeader = msgHeader + msg

        if encoding:
            return msgWithHeader.encode(FORMAT)

        return msgWithHeader

    def setWidgets(self, messagesText, enterChatRoomButton, usernameEntry, wrongUsername, checkUsernameButton):
        self.messagesText = messagesText
        self.enterChatRoomButton = enterChatRoomButton
        self.usernameEntry = usernameEntry
        self.wrongUsername = wrongUsername
        self.checkUsernameButton = checkUsernameButton

    def sendMessage(self):
        while True:
            try:
                msg = SEND_MESSAGE_QUEUE.get()
                self.clientSocket.send(msg)
                time.sleep(1)
            except:
                break

    def messageToBeSent(self, msg):
        # while True:
        # msg = 'asdfff'
        msgWithHeader = self.addHeader(msg, encoding=True)
        SEND_MESSAGE_QUEUE.put(msgWithHeader)
        time.sleep(1)

    def printMessage(self):
        while True:
            Message = RECIVE_MESSAGE_QUEUE.get()

            if Message[0:5] == 'admin':
                if 'unsuccesful' in Message:
                    self.state = 'disconnected'
                    usernameError = 'username not available'
                    self.enterChatRoomButton.configure(state = DISABLED)
                    self.usernameEntry.configure(fg = 'red')
                    self.wrongUsername.configure(text = usernameError)
                    self.wrongUsername.place(relx = 1.0, rely = 1.0, anchor = 'se')
                else:
                    self.state = 'connected'
                    self.enterChatRoomButton.configure(state = NORMAL)
                    self.usernameEntry.configure(fg = 'black')
                    self.wrongUsername.configure(text = '')
                    self.checkUsernameButton.configure(state = DISABLED)
            else:
                self.messagesText.insert(INSERT, Message)
            
            time.sleep(1)

    def recieveMessage(self):
        fullMessage = ''
        while True:
            try:
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
            except:
                break
                
    def runThreads(self):
        recieveMessageThread = threading.Thread(target=self.recieveMessage, daemon=True)
        sendMessageThread = threading.Thread(target=self.sendMessage, daemon=True)
        printMessageThread = threading.Thread(target=self.printMessage, daemon=True)
        # inputMessageThread = threading.Thread(target=self.messageToBeSent, daemon=True)

        recieveMessageThread.start()
        sendMessageThread.start()
        printMessageThread.start()
        # inputMessageThread.start()

        # recieveMessageThread.join()
        # sendMessageThread.join()
        # printMessageThread.join()
        # inputMessageThread.join()


# client = Client(ADDR)
# client.runThreads()
