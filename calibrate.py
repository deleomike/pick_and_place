from assistant.cyton import CytonController, CytonConnection

import time

def main():

    client = CytonConnection(send_port=8888, recv_port=8889)

    controller = CytonController(client=client)

    print("Beginning Calibration Procedure")

    print("Going Home")

    controller.go_home()

    time.sleep(3)


if __name__ == "__main__":
    main()

