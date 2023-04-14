from assistant.sensors.SensorController import SensorController
from assistant.sensors.MyoGestures import MyoGestures


class MyoController(SensorController):
    """
    """

    def __init__(self, listen_port: int = 5006):

        super().__init__(listen_port=listen_port)

        self._value_ = 1

    @property
    def gesture(self):
        return MyoGestures(self._value_)