from assistant.sensors.SensorController import SensorController


class MyoController(SensorController):
    """
    """

    def __init__(self, listen_port: int = 5006):

        super().__init__(listen_port=listen_port)

        self.gesture = 0

    def run(self):
        while True:
            self.read_data()

            self.gesture = self.get_most_frequent()





    def read_myo(self):
        self.sock = socket.socket(socket.AF_INET,  # Internet
                                  socket.SOCK_DGRAM)  # UDP

        self.sock.bind((self.udp_ip, self.udp_port))
        self.movement = []
        for ii in range(5):
            data, addr = self.sock.recvfrom(1)
            self.movement.append(data[0])
        self.movement_mode = mode(self.movement)
        if self.movement_mode == 1:
            print('flexion')
        elif self.movement_mode == 2:
            print('extension')
        elif self.movement_mode == 3:
            print('rest')
        self.sock.close()