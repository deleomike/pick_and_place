from assistant.sensors import MyoController, LeapController, DummySensorServer

import time


def simulate_leap():

    leap = LeapController()
    leap.start()

    leap_server = DummySensorServer(port=5005)

    leap_server.start()

    time.sleep(1)

    leap.stop()


if __name__ == "__main__":
    simulate_leap()