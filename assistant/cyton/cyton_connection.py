
import socket
import numpy as np

from typing import List


class CytonConnection:

    def __init__(self, ip: str = "127.0.0.1", send_port: int = 8888, recv_port: int = 8889):
        self.ip = ip
        self.recv_port = recv_port
        self.send_port = send_port

        self.send_sock: socket.socket = None
        self.recv_sock: socket.socket = None

        self.connect()

    def __del__(self):
        self.close_sockets()

    def _create_socket_(self, port):
        sock = socket.socket(socket.AF_INET,  # Internet
                             socket.SOCK_DGRAM)  # UDP

        print(f"Establishing Connection to {self.ip}:{port}")

        sock.connect((self.ip, port))

        sock.setblocking(0)

        return sock

    def close_sockets(self):
        if self.send_sock is not None:
            self.send_sock.close()

        if self.recv_sock is not None:
            self.recv_sock.close()

    def connect(self):
        """
        Establishes a connection to the robot
        :return: True/False whether the connection was successful
        """

        self.close_sockets()

        self.send_sock = self._create_socket_(self.send_port)
        self.recv_sock = self._create_socket_(self.recv_port)

    def send_angles(self, q: List[float]):

        data = np.array(q, dtype=np.double)
        data = data.view(np.uint8)

        try:
            self.send_sock.send(data)
        except Exception as e:
            print(f"Could not send data to {self.ip}:{self.send_port} {e}")
            raise e


if __name__ == "__main__":

    connection = CytonConnection(send_port=8888, recv_port=8889)

    # connection.send_angles([0, 0.7, 0, 0.7, 0, 0.7, 0, 0.01])

    # connection.send_angles([0, 0, 0, 0.7, 0, 0.7, 0, 0.01])

    connection.send_angles([0, 0, 0, 0.4, 0, 0, 0, 0.0])