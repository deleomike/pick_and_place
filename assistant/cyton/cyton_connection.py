
import socket
import numpy as np

from typing import List
from assistant.networking import UDPServer, UDPClient


class CytonConnection:

    def __init__(self, ip: str = "127.0.0.1", send_port: int = 8888, recv_port: int = 8889):
        self.ip = ip
        self.recv_port = recv_port
        self.send_port = send_port

        self.client = UDPClient(ip=self.ip, port=self.send_port)
        self.listener = UDPServer(ip=self.ip, listen_port=self.recv_port)

        # self.listener.start()

    def __del__(self):
        self.disconnect()

    def disconnect(self):
        self.client.disconnect()
        self.listener.disconnect()

    def send_angles(self, q: List[float]):

        data = np.array(q, dtype=np.double)
        data = data.view(np.uint8)

        try:
            self.client.sock.send(data)
        except Exception as e:
            print(f"Could not send data to {self.ip}:{self.send_port} {e}")
            raise e


if __name__ == "__main__":

    connection = CytonConnection(send_port=8888, recv_port=8889)

    # connection.send_angles([0, 0.7, 0, 0.7, 0, 0.7, 0, 0.01])

    # connection.send_angles([0, 0, 0, 0.7, 0, 0.7, 0, 0.01])

    connection.send_angles([0, 0, 0, 0.4, 0, 0, 0, 0.0])