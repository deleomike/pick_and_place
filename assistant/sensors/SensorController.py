import collections

import numpy as np

from assistant.networking.UDPServer import UDPServer


class SensorController(UDPServer):
    """
    """

    def __init__(self, listen_port: int, rolling_buffer_size: int = 100):
        super().__init__(listen_port=listen_port)

        self.rolling_buffer_size = rolling_buffer_size
        self.rolling_buffer = collections.deque(maxlen=self.rolling_buffer_size)

    def read_data(self) -> int:
        data, _ = self.sock.recvfrom(1)

        value = data[0]

        self.rolling_buffer.append(value)

        return value

    def get_most_frequent(self):
        counts = np.bincount(self.rolling_buffer)
        return np.argmax(counts)

    def run(self):
        while True:
            self.read_data()
