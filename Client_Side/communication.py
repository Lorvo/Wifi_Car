import socket

class CarConn:
    def __init__(self, add, port, buffSize):
        self.connected = False
        self.address = add
        self.port = port
        self.buffSize = buffSize
        self.comm = self.connect()

    def connect(self):
        try:
            TCPserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            TCPserver.connect((self.address, self.port))
            self.connected = True
            print("Connected successfully!")
            return TCPserver

        except:
            self.connected = False
            print(f"[CONNECTION ERROR]")

    def sendData(self, data):
        try:
            self.comm.send(data.encode("utf-8"))

        except NameError as err:
            print(f"[SEND ERROR] >>> {err}")

    def recvData(self):
            try:
                receivedData = self.comm.recv(self.buffSize)
                return receivedData
            
            except NameError as err:
                print(f"[RECEIVE ERROR] >>> {err}")

    def disconnect(self):
        try:
            self.comm.shutdown(socket.SHUT_RDWR)
            self.comm.close()
            self.connected = False
            print("Disconnected Successfully")

        except NameError as err:
            print(f"[DISCONNECT ERROR] >>> {err}")