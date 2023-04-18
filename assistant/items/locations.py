
import enum
import random

from assistant.items.poses import poses
from typing import Union
from spatialmath import SE3

NUM_BLOCKS = 5

# Assuming we have the q vectors for SHOW and HOME
SHOW_q_vector = [0, 0, 0]  # Replace with the actual values
HOME_q_vector = [0, 0, 0]  # Replace with the actual values


# TODO
class RobotSpecialLocations(enum.Enum):
    SHOW = SHOW_q_vector
    HOME = HOME_q_vector


# Generate random start locations
start_locations = [[random.uniform(0, 1) for _ in range(3)] for _ in range(NUM_BLOCKS)]


class BlockStartLocations(enum.Enum):
    B1 = SE3(0.1, 0.1, 0),  # Pose for cube 1
    B2 = SE3(0.2, 0.1, 0),  # Pose for cube 2
    B3 = SE3(0.3, 0.1, 0),  # Pose for cube 3
    B4 = SE3(0.4, 0.1, 0),  # Pose for cube 4
    B5 = SE3(0.5, 0.1, 0),  # Pose for cube 5
    # B2 = start_locations[1]
    # B3 = start_locations[2]
    # B4 = start_locations[3]
    # B5 = start_locations[4]

# Generate random end locations
end_locations = [[random.uniform(0, 1) for _ in range(3)] for _ in range(NUM_BLOCKS)]

class BlockEndLocations(enum.Enum):
    A = SE3(0.1, 0.1, 0),  # Pose for cube 1
    B = SE3(0.2, 0.1, 0),  # Pose for cube 2
    C = SE3(0.3, 0.1, 0),  # Pose for cube 3
    D = SE3(0.4, 0.1, 0),  # Pose for cube 4
    E = SE3(0.5, 0.1, 0),  # Pose for cube 5
    # A = end_locations[0]
    # B = end_locations[1]
    # C = end_locations[2]
    # D = end_locations[3]
    # E = end_locations[4]

loc_1 = (BlockStartLocations.B1, BlockEndLocations.A)
loc_2 = (BlockStartLocations.B2, BlockEndLocations.B)
loc_3 = (BlockStartLocations.B3, BlockEndLocations.C)
loc_4 = (BlockStartLocations.B4, BlockEndLocations.D)
loc_5 = (BlockStartLocations.B5, BlockEndLocations.E)


if __name__ == "__main__":
    # Iterate through NUM_BLOCKS
    for i in range(1, NUM_BLOCKS):
        # Get the start and end location Enums
        start_loc = BlockStartLocations(start_locations[i])
        end_loc = BlockEndLocations(end_locations[i])

        # Print the start and end location names
        print(f"{start_loc.name}: {start_loc.value}")
        print(f"{end_loc.name}: {end_loc.value}")