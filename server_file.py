import socket


HOST = socket.gethostbyname(socket.gethostname())
PORT = 6542
ADDR = (HOST, PORT)
FORMAT = 'utf-8'
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


SERVER.bind(ADDR)
print(ADDR)
# this means we will have a backlog of 5 unsuccessful connections
SERVER.listen(5)
print(f"[SERVER]: is listening at port: {PORT}")


while True:
    conn, addr = SERVER.accept()
    print(f"[CLIENT]: {addr[0]} is connected from port: {addr[1]}")
    recievedMsgLength = conn.recv(1024)
    bufferSize = int(recievedMsgLength)
    # No need to decode it(if you want you can), because even if you decode it
    # it will change its format from binary to string,but we can directly get integral value using int

    # print(recievedMsgLength)
    print(f'[SERVER]: recieving a message of {int(bufferSize)} bytes')

    recievedMsg = conn.recv(bufferSize)
    recievedMsg = recievedMsg.decode(FORMAT)
    print(f"[CLIENT]: {recievedMsg}")

    print("[SERVER]: echoing back...")

    conn.send(recievedMsgLength)
    conn.send(recievedMsg.encode(FORMAT))
    print("[SERVER]: echoed")

    conn.close()
