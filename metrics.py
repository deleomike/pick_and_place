import pandas as pd
import numpy as np

import time

from cyton_control_UPDATE_04_25_23 import number_good_pickup
from cyton_control_UPDATE_04_25_23 import number_bad_pickup
from cyton_control_UPDATE_04_25_23 import number_pickups
from cyton_control_UPDATE_04_25_23 import number_good_place
from cyton_control_UPDATE_04_25_23 import number_bad_place
from cyton_control_UPDATE_04_25_23 import number_place

df = pd.Dataframe(columns = ['Pickup Success', 'Pickup Fail', 'Pickup Attempts', 'Place Success', 'Place Fail', 'Place Attempts'])
df.loc[len(df)] = [number_good_pickup, number_bad_pickup, number_pickups, number_good_place, number_bad_place, number_place]
df

