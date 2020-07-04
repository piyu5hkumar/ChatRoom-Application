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


MESSAGE_QUEUE = queue.Queue()


CLIENTS = []
DISCONNECTED_CLIENTS = []
USERS = {
    'connected': '',
    'disconnected': '',
    'anonymous': '',
    'anom': '',
    'socket': '',
    'administrator': '',
    'admin': '',
    'message': '',
    'user': ''
}


def addHeader(msg, format='utf-8', encoding=False):
    msgLength = len(msg)
    msgHeader = f'{len(msg):<{HEADER_LENGTH}}'
    msgWithHeader = msgHeader + msg

    if encoding:
        return msgWithHeader.encode(FORMAT)

    return msgWithHeader


class Client:
    def __init__(self, connection, address):
        self.connection = connection
        self.IPaddress = address[0]
        self.port = address[1]
        self.userExists = False
        self.userName = None
        self.fullMessage = ''
        self.connection.settimeout(1)

    def inbox(self):
        try:
            msg = self.connection.recv(43)
        except socket.timeout as e:
            pass
        except:
            print('some error')
        else:
            if len(msg) != 0:
                self.fullMessage += msg.decode(FORMAT)

                while self.fullMessage != '':
                    msgLength = int(self.fullMessage[:HEADER_LENGTH])
                    chunkLength = HEADER_LENGTH + msgLength

                    if chunkLength > len(self.fullMessage):
                        break
                    else:
                        chunk = self.fullMessage[:chunkLength]
                        message = chunk[HEADER_LENGTH:]

                        if self.userExists == False:
                            if message not in USERS:
                                self.userExists = True
                                self.userName = message
                                USERS[message] = (self.IPaddress, self.port)
                                connectedMessageTuple = ('connected', self.userName)
                                MESSAGE_QUEUE.put(connectedMessageTuple)
                                userSuccess = 'admin > success'
                                userSuccess = addHeader(userSuccess, encoding = True)
                                self.connection.send(userSuccess)
                            else:
                                userError = 'admin > unsuccesful'
                                userError = addHeader(userError, encoding = True)
                                self.connection.send(userError)
                        else:
                            userMessageTupple = ('message', self.userName, message)
                            MESSAGE_QUEUE.put(userMessageTupple)
                        self.fullMessage = self.fullMessage[chunkLength:]
            else:
                if self.userExists == True:
                    del USERS[self.userName]
                    disconnectedMessageTuple = ('disconnected', self.userName)
                    MESSAGE_QUEUE.put(disconnectedMessageTuple)
                    print(f'{self.userName}: {self.IPaddress} at PORT ({self.port}) has been disconnected')

                else:
                    print(f'{self.IPaddress} at PORT ({self.port}) has been disconnected')

                self.connection.close()
                DISCONNECTED_CLIENTS.append(self)

    def outbox(self, message):
        try:
            self.connection.send(message)
        except ConnectionResetError as e:
            print('A client disconnected', e)

class Server:
    __instance = None

    @staticmethod
    def getInstance(addr):
        if Server.__instance == None:
            Server(addr)

        return Server.__instance

    def __init__(self, addr):
        if Server.__instance != None:
            raise Exception('A server is already there')
        else:
            self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.serverSocket.bind(addr)
            self.serverSocket.listen(5)
            print(f"[SERVER]: is listening at port: {addr[1]}")
            Server.__instance = self

    def acceptConnections(self):
        while True:
            connectionTupple = self.serverSocket.accept()
            client = Client(*connectionTupple)
            print(f"[CLIENT]: {client.IPaddress} is connected from port: {client.port}")
            CLIENTS.append(client)

    def removeDisconnectedClients(self):
        for disconnected_client in DISCONNECTED_CLIENTS:
            try:
                CLIENTS.remove(disconnected_client)
                del disconnected_client

            except ValueError as e:
                pass

        DISCONNECTED_CLIENTS.clear()

    def recieveMessages(self):
        while True:

            self.removeDisconnectedClients()
            for client in CLIENTS:
                status = client.inbox()

    def sendMessages(self):
        while True:
            messageTupple = MESSAGE_QUEUE.get()

            msg = ''
            if messageTupple[0] == 'message':
                msg = messageTupple[1] + ' > ' + messageTupple[2]

            elif messageTupple[0] == 'connected':
                msg = messageTupple[1] + ' has joined the chat'

            elif messageTupple[0] == 'disconnected':
                msg = messageTupple[1] + ' has left the chat'

            msgWithHeader = addHeader(msg, encoding=True)

            self.removeDisconnectedClients()
            for client in CLIENTS:
                if client.userName != messageTupple[1]:
                    client.outbox(msgWithHeader)
            time.sleep(1)

    def runThreads(self):
        acceptConnectionsThread = threading.Thread(target=self.acceptConnections, daemon=True)
        recieveMessagesThread = threading.Thread(target=self.recieveMessages, daemon=True)
        sendMessagesThread = threading.Thread(target=self.sendMessages, daemon=True)

        acceptConnectionsThread.start()
        recieveMessagesThread.start()
        sendMessagesThread.start()

        acceptConnectionsThread.join()
        recieveMessagesThread.join()
        sendMessagesThread.join()


server = Server(ADDR)
server.runThreads()
