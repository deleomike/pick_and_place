import collections

import numpy as np

from assistant.networking.UDPServer import UDPServer


class SensorController(UDPServer):
    """
    Base Sensor Controller
    """

    def __init__(self, listen_port: int, rolling_buffer_size: int = 100):
        super().__init__(listen_port=listen_port)

        self.rolling_buffer_size = rolling_buffer_size
        self.rolling_buffer = collections.deque(maxlen=self.rolling_buffer_size)

        self._value_ = 0

        self.running = True

    def _read_data_(self) -> int:
        """
        Internal function. Reads data from the socket and appends it to the circular buffer
        """
        data, _ = self.sock.recvfrom(1)

        value = data[0]

        self.rolling_buffer.append(value)

        return value

    def get_most_frequent(self):
        """
        Gets the most frequent value in the circular buffer
        """
        counts = np.bincount(self.rolling_buffer)
        return np.argmax(counts)

    def stop(self):
        """
        Stops the running thread
        """
        self.running = False

    def run(self):
        while self.running:
            self._read_data_()

            self._value_ = self.get_most_frequent()

