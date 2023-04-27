import time

from assistant.sensors.SensorController import SensorController


class LeapController(SensorController):
    """
    Leap UDP Server. Listens to the Leap sensor
    """

    def __init__(self, listen_port: int = 5005, rolling_buffer_size: int = 10):

        super().__init__(listen_port=listen_port, rolling_buffer_size=rolling_buffer_size)

    @property
    def finger_mode(self):
        self.count = 0
        printed_pause = 0
        while self.count < 10:
            while self.pause:
                if not printed_pause:
                    print('pausing for now')
                    printed_pause = 1
                self.count = 0
            printed_pause = 0
            pass
        return self.get_most_frequent()


if __name__ == "__main__":
    leap = LeapController()

    leap.start()

    time.sleep(3)

    # leap.stop()

    leap.join()

    # while True:
    #     print(leap.finger_mode)