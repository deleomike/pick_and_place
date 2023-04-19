import socket
import numpy as np

from typing import List


class UDPClient:

    def __init__(self, ip: str = "127.0.0.1", port: int = 8888):
        self.ip = ip
        self.port = port

        self.sock: socket.socket = self._create_socket_()

    def __del__(self):
        self.disconnect()

    def _create_socket_(self):
        sock = socket.socket(socket.AF_INET,  # Internet
                             socket.SOCK_DGRAM)  # UDP

        print(f"Establishing Connection to {self.ip}:{self.port}")

        sock.connect((self.ip, self.port))

        sock.setblocking(0)

        return sock

    def disconnect(self):
        if self.sock is not None:
            print(f"Closing socket on {self.ip}:{self.port}")
            self.sock.close()

    def reconnect(self):
        """
        Establishes a connection to the robot
        :return: True/False whether the connection was successful
        """

        self.disconnect()

        self.sock = self._create_socket_()
