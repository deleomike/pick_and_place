To run finger counting with the Leap, download the SDK found at
https://developer-archive.leapmotion.com/get-started?id=v3-developer-beta&platform=windows&version=3.2.1.45911
Then run Sample.py in Python 2.7.
To run:
1. Change system python version to 2.7
2. Add all helper files to your run directory
  (Leap.py, LeapPython.py. Leap.dll, etc)
  (they should all already be contained in this directory)
3. Connect to Leap using Leap software (installed with SDK download)
   (you can debug/make sure you are connected by opening up the visualizer)
4. Run script in terminal and view output
   (place hand in frame to determine total number of extended fingers)