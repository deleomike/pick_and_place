import collections
import time
import sys

import numpy as np

from threading import Lock
from assistant.networking import UDPServer, UDPClient


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

        self.lock = Lock()

    def __del__(self):
        self.stop()

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
        print(f"Stopping thread listening on port {self.port}")
        with self.lock:
            self.running = False

            # Send a packet to unblock the socket pipeline
            temp_client = UDPClient(ip=self.ip, port=self.port)
            temp_client.sock.send(np.array([-1], dtype=np.int8))

            time.sleep(1)

            self.disconnect()

    def run(self):
        while True:
            self._read_data_()

            self._value_ = self.get_most_frequent()

            with self.lock:
                if not self.running:
                    print(f"THREAD: Stopping Main Thread Listening on {self.ip}:{self.port}")
                    sys.stdout.flush()
                    break

