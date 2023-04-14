from assistant.sensors.SensorController import SensorController


class LeapController(SensorController):
    """
    Leap UDP Server. Listens to the Leap sensor
    """

    def __init__(self, listen_port: int = 8888):

        super().__init__(listen_port=listen_port)

    @property
    def finger_mode(self):
        return self._value_
