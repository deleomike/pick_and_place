import streamlit as st
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import roboticstoolbox as rtb

from assistant.cyton import CytonGamma300
from spatialmath import SE3

st.title("Pick and Place Robot")
st.header("Cyton 300 Gamma")

robot = rtb.models.Panda()
robot_txt = f"```console" \
            f"{robot}" \
            f"```"
st.write(robot_txt)

Tep = SE3.Trans(0.6, -0.3, 0.1) * SE3.OA([0, 1, 0], [0, 0, -1])
sol = robot.ik_lm_chan(Tep)         # solve IK
print(sol)

q_pickup = sol[0]
print(robot.fkine(q_pickup))    # FK shows that desired end-effector pose was achieved

qt = rtb.jtraj(robot.qr, q_pickup, 50)

fig = plt.figure()
robot.plot(qt.q, backend="pyplot", fig=fig)

st.pyplot(fig)