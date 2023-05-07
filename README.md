[![Powered by the Robotics Toolbox](https://raw.githubusercontent.com/petercorke/robotics-toolbox-python/master/.github/svg/rtb_powered.min.svg)](https://github.com/petercorke/robotics-toolbox-python)
[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-310/)
[![Python 2.7](https://img.shields.io/badge/python-2.7-blue.svg)](https://www.python.org/downloads/release/python-270/)

# Pick and Place

2023 semester project for the Human Robotics Interaction course at JHU. A pick and place robot program.

## Authors / Group Members

1. Michael DeLeo - @deleomike
2. Cyrus Hossainian - @chossai1
3. Emma Kaufman - @emmakaufman14
4. Saamahn Mahjouri -  @saams4u

## Requirements

1. Matlab
2. Python 3.10
3. Python 2.7
4. Ultra Leap IR Sensor
5. Myoband
6. Robai 7 DOF Robot

## Development

### Setup

HTTPS Clone
```
git clone https://github.com/deleomike/pick_and_place.git
```

Create your python environment (Mac/Linux)
```commandline
python -m venv env
. ./env/bin/activate
pip install -r requirements.txt
```

## Demonstration

You'll need to be logged into Admin

1. Make sure the leap is connected (check the leap toolbar)
2. Run the Leap Server

run this in the `leap` directory
```commandline
python2.7 Sample.py
```

3. Run the MyoBand Server

Open `myo_matlab.m` with matlab and run it

4. Start the Cyton Actin Viewer
   1. Load the server plugin
   2. Enable Hardware
   3. Hit Play
   4. Start the client terminal script
5. Start the main script

## Testing

To test the controller with a dummy cyton server run

```bash
python simulated_cyton_server.py
```

Which will stand up a UDP server that will act like the cyton and print out positions.

