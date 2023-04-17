[![Powered by the Robotics Toolbox](https://raw.githubusercontent.com/petercorke/robotics-toolbox-python/master/.github/svg/rtb_powered.min.svg)](https://github.com/petercorke/robotics-toolbox-python)

# Pick and Place

2023 semester project for the Human Robotics Interaction course at JHU. A pick and place robot program.

## Development

HTTPS Clone
```
git clone https://github.com/deleomike/pick_and_place.git
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
   1. Load the client plugin
   2. Enable Hardware
   3. Hit Play
5. Start the main script

## Testing

To test the controller with a dummy cyton server run

```bash
python simulated_cyton_server.py
```

Which will stand up a UDP server that will act like the cyton and print out positions.

