import socket
import threading
import time


class UDPServer(threading.Thread):

    def __init__(self, ip: str = "127.0.0.1", listen_port: int = 8888, buffer_size: int = 1024):
        super(UDPServer, self).__init__()
        self.ip = ip
        self.port = listen_port
        self.buffer_size = buffer_size

        # Create a datagram socket

        self.sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

        # Bind to address and ip

        print(f"Binding to {self.ip}:{self.port}")


        try:
            self.sock.bind((self.ip, self.port))
        except OSError as e:
            print(f"Could not bind to {self.ip}:{self.port}")
            raise e

        print(f"UDP server up and listening at {self.ip}:{self.port}")

    def __del__(self):
        self.disconnect()

    def disconnect(self):
        self.sock.close()

    def run(self):
        while True:
            bytesAddressPair = self.sock.recvfrom(self.buffer_size)

            message = bytesAddressPair[0]

            address = bytesAddressPair[1]

            clientMsg = "Message from Client:{}".format(message)
            clientIP = "Client IP Address:{}".format(address)

            print(clientMsg)
            print(clientIP)


if __name__ == "__main__":
    server = UDPServer()

    server.run()