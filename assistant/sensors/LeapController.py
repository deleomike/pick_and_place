from assistant.sensors.SensorController import SensorController


class LeapController(SensorController):
    """
    """

    def __init__(self, listen_port: int = 8888):

        super().__init__(listen_port=listen_port)

        self.fingers = 0

    def run(self):
        while True:
            self.read_data()

            self.fingers = self.get_most_frequent()

            print(self.fingers)




    def read_leap(self):
        self.sock = socket.socket(socket.AF_INET,  # Internet
                                  socket.SOCK_DGRAM)  # UDP

        self.sock.bind((self.udp_ip, self.udp_port))
        self.fingers = []
        for ii in range(100):
            data, addr = self.sock.recvfrom(1)
            self.fingers.append(data[0])
        self.finger_mode = mode(self.fingers)
        self.sock.close()