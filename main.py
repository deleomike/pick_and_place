import streamlit as st
from assistant.sensors import MyoController, LeapController
from assistant.cyton.cyton_connection import CytonConnection
from assistant.cyton.cyton_controller import CytonController
from assistant.scheduler import Scheduler
from assistant.items.Block import Block
from assistant.items.locations import BlockEndLocations
from assistant.state_machine import PickPlaceStateMachine


st.title("Pick and Place Robot")
st.header("Cyton 300 Gamma")

# client = CytonConnection(wait=False)
#
# controller = CytonController(client=client)

if 'leap' not in st.session_state:
    st.session_state['leap'] = LeapController()
    st.session_state.leap.start()

if 'myo' not in st.session_state:
    st.session_state['myo'] = MyoController()
    st.session_state.myo.start()


if 'leap' in st.session_state:
    leap = st.session_state['leap']
    st.write("hello")
    st.metric("Fingers", leap.finger_mode)

if 'myo' in st.session_state:
    myo = st.session_state['myo']

    st.metric("Gesture", myo.gesture)



# #################
# # State Machine #
# #################
#
# state_machine = PickPlaceStateMachine(controller=controller, leap_controller=leap, myo_controller=myo)
#
# state_machine.run()