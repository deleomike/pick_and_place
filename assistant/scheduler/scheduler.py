from assistant.scheduler.forward_planner import forward_planner
from assistant.items import Block, BlockStartLocations, BlockEndLocations, RobotSpecialLocations
from typing import List
from copy import deepcopy


def _item_(name):
    return f"(item {name})"


def _start_place_(name):
    return f"(start_place {name})"


def _end_place_(name):
    return f"(end_place {name})"


def _special_place_(name):
    return f"(special_place {name})"


def _at_place_(thing, place):
    return f"(at {thing} {place})"


class Scheduler:
    def __init__(self, blocks: List[Block]):

        self.blocks = blocks
        self.blocks.sort(key=lambda b: b.pos_id)

        # Items
        items = [_item_(block) for block in self.blocks]

        # Places
        start_locations = [_end_place_(e.name) for e in BlockStartLocations]
        end_locations = [_start_place_(e.name) for e in BlockEndLocations]
        special_places = [_special_place_(e.name) for e in RobotSpecialLocations]

        places = []
        places.extend(end_locations)
        places.extend(start_locations)
        places.extend(special_places)

        # at <ITEM> <LOCATION>

        robot_location = _at_place_("Cyton", RobotSpecialLocations.HOME.name)

        item_start_locations = [_at_place_(block, block.location.name) for block in self.blocks]
        item_end_locations = [_at_place_(block, e.name) for e, block in zip(BlockStartLocations, self.blocks)]

        item_start_locations.append(robot_location)
        item_end_locations.append(robot_location)

        # Agent(s)
        agents = ["(agent Cyton)"]

        # Occupied states
        occ_states = ["(state Cyton EMPTY)"]
        occ_states.extend([f"(state {e.name} EMPTY)" for e, block in zip(BlockStartLocations, self.blocks)])

        # Requirements

        requirements = [f"(require {block} {block.home_location.name})" for block in self.blocks]

        # START State

        base_state = []
        base_state.extend(items)
        base_state.extend(places)
        base_state.extend(agents)
        base_state.extend(requirements)

        self.start = deepcopy(base_state)
        self.start.extend(item_start_locations)
        self.start.extend(occ_states)

        # GOAL State

        self.goal = deepcopy(base_state)
        self.goal.extend(item_end_locations)
        self.goal.append(occ_states[0])

        self.actions = {
            "move_to_block": {
                "action": "(move_to_block ?agent ?from ?to)",
                "conditions": [
                    "(agent ?agent)",
                    "(special_place ?from)",
                    "(start_place ?to)",
                    "(item ?item)",
                    "(state ?agent EMPTY)",
                    "(at ?item ?to)",
                    "(at ?agent ?from)"
                ],
                "add": [
                    "(at ?agent ?to)"
                ],
                "delete": [
                    "(at ?agent ?from)"
                ]
            },
            "move_to_place_block": {
                "action": "(move_to_place_block ?agent ?from ?to)",
                "conditions": [
                    "(agent ?agent)",
                    "(special_place ?from)",
                    "(end_place ?to)",
                    "(item ?item)",
                    "(state ?to EMPTY)",
                    "(require ?item ?to)",
                    "(at ?item ?agent)",
                    "(at ?agent ?from)"
                ],
                "add": [
                    "(at ?agent ?to)"
                ],
                "delete": [
                    "(at ?agent ?from)"
                ]
            },
            "show_block": {
                "action": f"(show_block ?agent ?from ?to)",
                "conditions": [
                    "(item ?item)",
                    "(agent ?agent)",
                    "(start_place ?from)",
                    f"(special_place ?to)",
                    "(at ?item ?agent)",
                    "(at ?agent ?from)"
                ],
                "add": [
                    f"(at ?agent ?to)"
                ],
                "delete": [
                    "(at ?agent ?from)"
                ]
            },
            "go_home": {
                "action": f"(go_home ?agent ?from ?to)",
                "conditions": [
                    "(item ?item)",
                    "(agent ?agent)",
                    "(end_place ?from)",
                    f"(special_place ?to)",
                    "(state ?agent EMPTY)",
                    "(at ?agent ?from)"
                ],
                "add": [
                    f"(at ?agent ?to)"
                ],
                "delete": [
                    "(at ?agent ?from)"
                ]
            },
            "pickup": {
                "action": "(pickup ?agent ?location ?item)",
                "conditions": [
                    "(item ?item)",
                    "(start_place ?location)",
                    "(agent ?agent)",
                    "(state ?agent EMPTY)",
                    "(at ?item ?location)",
                    "(at ?agent ?location)"
                ],
                "add": [
                    "(at ?item ?agent)"
                ],
                "delete": [
                    "(at ?item ?location)",
                    "(state ?agent EMPTY)"
                ]
            },
            "place": {
                "action": "(place ?agent ?location ?item)",
                "conditions": [
                    "(item ?item)",
                    "(end_place ?location)",
                    "(agent ?agent)",
                    "(at ?item ?agent)",
                    "(at ?agent ?location)"
                ],
                "add": [
                    "(at ?item ?location)",
                    "(state ?agent EMPTY)"
                ],
                "delete": [
                    "(at ?item ?agent)",
                    "(state ?location EMPTY)",
                ]
            }
        }

    def execute(self):
        print("Working...")
        plan = forward_planner(self.start, self.goal, self.actions)
        print(f"Plan found - {len(plan)} actions")
        return plan


if __name__ == "__main__":
    blocks = [Block(idx+1, color="blue", location=e) for idx, e in enumerate(BlockEndLocations)]
    # blocks = [Block(1, color="blue", location=BlockEndLocations.A)]
    scheduler = Scheduler(blocks)

    print("PLAN: ", scheduler.execute())