from assistant.sensors.SensorController import SensorController
from assistant.sensors.MyoGestures import MyoGestures


import time


class MyoController(SensorController):
    """
    MyoBand controller

    Listens to the myoband and stores its results
    """

    def __init__(self, listen_port: int = 5006, rolling_buffer_size: int = 10):

        super().__init__(listen_port=listen_port, rolling_buffer_size=rolling_buffer_size)

        self._value_ = 1

    @property
    def gesture(self):
        return MyoGestures(self._value_)


if __name__ == "__main__":
    myo = MyoController()

    myo.start()

    while True:
        print(myo.gesture)