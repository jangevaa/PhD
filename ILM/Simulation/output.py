"""output.py - a number of output options (visualizations and text)"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation

"""csv output instructions: you can easily export a csv of the population file or the
event database by using the `DF.to_csv("/dir/ect/ory/")`, where DF represents the data
that will be exported.
""""


plot_infection(pop, event_db, time):
    """This will create a simple scatterplot of susceptible and infectious individuals at
    a given time"
    