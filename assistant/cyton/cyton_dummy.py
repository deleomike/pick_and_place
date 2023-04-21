import numpy as np

from assistant.networking import UDPServer


class CytonDummyServer(UDPServer):
    """
    Dummy UDP Server

    Will decode angle commands and print them to terminal
    """

    def __init__(self, listen_port: int = 8889, verbose: bool = True, round_to: int = 4):
        super().__init__(listen_port=listen_port)

        self._current_angles = np.zeros(8).tolist()
        self.verbose = verbose

        self.round = round_to

    @property
    def current_angles(self):
        return self._current_angles

    @current_angles.setter
    def current_angles(self, arr: np.array):
        self._current_angles = arr.round(self.round)


    def run(self):
        while True:
            bytesAddressPair = self.sock.recvfrom(self.buffer_size)

            message = bytesAddressPair[0]

            address = bytesAddressPair[1]

            self.current_angles = np.frombuffer(message)

            if self.verbose:
                output = f"Received command from {address} \n    {self.current_angles}"
                print(output)
