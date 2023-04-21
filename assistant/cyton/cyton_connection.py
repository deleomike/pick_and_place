
import socket
import time

import numpy as np

from typing import List
from assistant.networking import UDPServer, UDPClient
from assistant.cyton.cyton_dummy import CytonDummyServer


class CytonConnection:

    def __init__(self, ip: str = "127.0.0.1", send_port: int = 8888, recv_port: int = 8889, verbose: bool = False):
        self.ip = ip
        self.recv_port = recv_port
        self.send_port = send_port

        self.client = UDPClient(ip=self.ip, port=self.send_port)
        self.listener = CytonDummyServer(listen_port=self.recv_port, round_to=4, verbose=verbose )

        self.listener.start()

    def __del__(self):
        self.disconnect()

    def disconnect(self):
        self.client.disconnect()
        self.listener.disconnect()

    def is_cyton_at_q(self, q: List[float]) -> bool:
        """
        Checks if the cyton is at the set of angles
        """
        ground_truth_angles = self.listener.current_angles

        q_np = np.array(q)

        return (q_np == ground_truth_angles).all()

    def send_angles(self, q: List[float], wait: bool = True):
        """
        Sends angles to cyton. Can also wait for cyton reach these angles
        """

        data = np.array(q, dtype=np.double)
        data = data.view(np.uint8)

        try:
            self.client.sock.send(data)
        except Exception as e:
            print(f"Could not send data to {self.ip}:{self.send_port} {e}")
            raise e

        # while wait:
        #     if self.is_cyton_at_q(q=q):
        #         break
        #     else:
        #         time.sleep(0.1)


if __name__ == "__main__":

    connection = CytonConnection(send_port=8888, recv_port=8889)

    connection.send_angles([0, 0.7, 0, 0.7, 0, 0.7, 0, 0.01])

    # connection.send_angles([0, 0, 0, 0.7, 0, 0.7, 0, 0.01])

    connection.send_angles([0, 0, 0, 0.4, 0, 0, 0, 0.0])

    print("Done")

    connection.disconnect()