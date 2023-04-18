from assistant.sensors.SensorController import SensorController


class LeapController(SensorController):
    """
    Leap UDP Server. Listens to the Leap sensor
    """

    def __init__(self, listen_port: int = 5005, rolling_buffer_size: int = 10):

        super().__init__(listen_port=listen_port, rolling_buffer_size=rolling_buffer_size)

    @property
    def finger_mode(self):
        return self._value_


if __name__ == "__main__":
    leap = LeapController()

    leap.start()

    while True:
        print(leap.finger_mode)