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
            'admin': ''
        }


def addHeader(msg, format='utf-8', encoding=False):
    msgLength = len(msg)
    msgHeader = f'{len(msg):<{HEADER_LENGTH}}'
    msgWithHeader = msgHeader + msg

    if encoding:
        return msgWithHeader.encode(FORMAT)

    return msgWithHeader


class Client:
    def __init__(self,connection, address):
        self.connection = connection
        self.address = address
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
                                USERS[message] = self.address
                                self.userName = message
                            else:
                                userError = 'Username not available'
                                userError = addHeader(userError, encoding=True)
                                self.connection.send(userError)
                        else:
                            userMessageTupple = (self.userName, message)
                            MESSAGE_QUEUE.put(userMessageTupple)
                        self.fullMessage = self.fullMessage[chunkLength:]
            else:
                print(f'{self.userName}: {self.address[0]} at PORT ({self.address[1]}) has been disconnected')
                self.connection.close()
                DISCONNECTED_CLIENTS.append(self)


    def outbox(self, message):

        self.connection.send(message)





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
            print(f"[CLIENT]: {client.address[0]} is connected from port: {client.address[1]}")
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

            userMessageTupple = MESSAGE_QUEUE.get()
            msg = userMessageTupple[0] + ' > ' + userMessageTupple[1]
            msgWithHeader = addHeader(msg, encoding=True)
            
            self.removeDisconnectedClients()            
            for client in CLIENTS:
                if client.userName != userMessageTupple[0]:
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

