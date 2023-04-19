import threading
import time

import numpy as np

from threading import Thread
from assistant.networking.UDPClient import UDPClient


class DummySensorServer(UDPClient, Thread):

    def __init__(self, port: int = 5005):
        threading.Thread.__init__(self)
        super(DummySensorServer, self).__init__(port=port)

    def run(self):
        while True:
            data = np.array([1], dtype=np.int8)
            self.sock.send(data)
            time.sleep(0.1)


if __name__ == "__main__":
    server = DummySensorServer()

    server.run()