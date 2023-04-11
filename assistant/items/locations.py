
import enum
import random
from typing import Union

NUM_BLOCKS = 5

# Assuming we have the q vectors for SHOW and HOME
SHOW_q_vector = [0, 0, 0]  # Replace with the actual values
HOME_q_vector = [0, 0, 0]  # Replace with the actual values

class RobotSpecialLocations(enum.Enum):
    SHOW = SHOW_q_vector
    HOME = HOME_q_vector

# Generate random relative poses for the start locations
start_locations = [[random.uniform(0, 1) for _ in range(3)] for _ in range(NUM_BLOCKS)]

class BlockStartLocations(enum.Enum):
    B1 = start_locations[0]
    B2 = start_locations[1]
    B3 = start_locations[2]
    B4 = start_locations[3]
    B5 = start_locations[4]

# Generate random relative poses for the end locations
end_locations = [[random.uniform(0, 1) for _ in range(3)] for _ in range(NUM_BLOCKS)]

class BlockEndLocations(enum.Enum):
    A = end_locations[0]
    B = end_locations[1]
    C = end_locations[2]
    D = end_locations[3]
    E = end_locations[4]

loc_1 = Union[BlockStartLocations.B1, BlockEndLocations.A]
loc_2 = Union[BlockStartLocations.B2, BlockEndLocations.B]
loc_3 = Union[BlockStartLocations.B3, BlockEndLocations.C]
loc_4 = Union[BlockStartLocations.B4, BlockEndLocations.D]
loc_5 = Union[BlockStartLocations.B5, BlockEndLocations.E]

# Iterate through NUM_BLOCKS
for i in range(1, NUM_BLOCKS):
    # Get the start and end location Enums
    start_loc = BlockStartLocations(start_locations[i])
    end_loc = BlockEndLocations(end_locations[i])

    # Print the start and end location names and poses
    print(f"{start_loc.name}: {start_loc.value}")
    print(f"{end_loc.name}: {end_loc.value}")