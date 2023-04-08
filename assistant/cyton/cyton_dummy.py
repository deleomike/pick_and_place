import numpy as np

from assistant.networking import UDPServer


class CytonDummyServer(UDPServer):
    """
    Dummy UDP Server

    Will decode angle commands and print them to terminal
    """

    def run(self):
        while True:
            bytesAddressPair = self.sock.recvfrom(self.buffer_size)

            message = bytesAddressPair[0]

            address = bytesAddressPair[1]

            q = np.frombuffer(message)

            output = f"Received command from {address} \n    {q}"
            print(output)