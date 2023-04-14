"""
This is intended to test and debug that the sensors are in fact connected
"""

import time

from assistant.sensors import MyoController, LeapController


def main():
    leap = LeapController()
    myo = MyoController()

    leap.start()
    myo.start()

    while True:
        print("-----------------------")
        print(f"Fingers {leap.fingers}")
        print(f"Gesture {myo.gesture.name}")

        time.sleep(1)


if __name__ == "__main__":
    main()