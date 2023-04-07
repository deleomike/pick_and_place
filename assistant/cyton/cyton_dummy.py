import numpy as np

from assistant.networking import UDPServer


class CytonDummyServer(UDPServer):

    def run(self):
        while True:
            bytesAddressPair = self.sock.recvfrom(self.buffer_size)

            message = bytesAddressPair[0]

            address = bytesAddressPair[1]

            clientMsg = "Message from Client:{}".format(message)
            clientIP = "Client IP Address:{}".format(address)

            q = np.frombuffer(message)

            output = f"Received command from {address} - {q}"
            print(output)