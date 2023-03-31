################################################################################
# Copyright (C) 2012-2016 Leap Motion, Inc. All rights reserved.               #
# Leap Motion proprietary and confidential. Not for distribution.              #
# Use subject to the terms of the Leap Motion SDK Agreement available at       #
# https://developer.leapmotion.com/sdk_agreement, or another agreement         #
# between Leap Motion and you, your company or other organization.             #
################################################################################

# This script is based heavily on the Sample.py script provided with the Leap
# SDK. Modifications have been made to count the number of extended fingers.

# This script requires all files from the Leap SDK found at
# https://developer-archive.leapmotion.com/get-started?id=v3-developer-beta&platform=windows&version=3.2.1.45911
# It also must be run in Python 2.7.
# To run:
# 1. Change python version to 2.7
# 2. Add all helper files to your run directory
#   (Leap.py, LeapPython.py. Leap.dll, etc)
# 3. Connect to Leap using Leap software (installed with SDK download)
# 4. Run script in terminal and view output

import Leap, sys, thread, time


class SampleListener(Leap.Listener):

    def on_init(self, controller):
        print "Initialized"

    def on_connect(self, controller):
        print "Connected"

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def on_frame(self, controller):
        # Get the most recent frame
        frame = controller.frame()

        # Get hands
        for hand in frame.hands:

            handType = "Left hand" if hand.is_left else "Right hand"

            # Get the hand's normal vector and direction
            normal = hand.palm_normal
            direction = hand.direction

            # Get fingers and count extended fingers
            extendedFingers = 0
            for finger in hand.fingers:
                 if(finger.is_extended):
                    extendedFingers = extendedFingers +1
            print(extendedFingers)
                
        if not frame.hands.is_empty:
            print ""

def main():
    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        # Remove the sample listener when done
        controller.remove_listener(listener)


if __name__ == "__main__":
    main()
