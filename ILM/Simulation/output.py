"""output.py - a number of output options (visualizations and text)"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation

"""csv output instructions: you can easily export a csv of the population file or the
event database by using the `DF.to_csv("/dir/ect/ory/")`, where DF represents the data
that will be exported.
"""

def plot_si(pop, event_db, time):
    """This will create a simple scatterplot of susceptible and infectious individuals at
    a given time
    """
    i=find_infectious(pop, event_db, time)
    s=find_susceptible(pop, event_db, time)
    status=pd.DataFrame({"status":np.append(np.repeat("i", i.shape[0]), np.repeat("s", s.shape[0])), 
                         "colour":np.append(np.repeat("k", i.shape[0]), np.repeat("b", s.shape[0])),
                         "ind_ID":np.append(i.ind_ID, s.ind_ID),
                         "x":pop.iloc[np.append(i.ind_ID, s.ind_ID)].x,
                         "y":pop.iloc[np.append(i.ind_ID, s.ind_ID)].y})
    plt.scatter(status.x, status.y, c=status.colour, s=60, edgecolors='none')

def plot_sicr(pop, event_db, time):
    """This will create a simple scatterplot of susceptible, infectious, and recovered
    individuals at a given time
    """
    i=find_nonrecovered(pop, event_db, time)
    s=find_susceptible(pop, event_db, time)
    r=find_recovered(pop, event_db, time)
    status=pd.DataFrame({"status":np.append(np.append(np.repeat("i", i.shape[0]), np.repeat("s", s.shape[0])),np.repeat("r", r.shape[0])),
                         "colour":np.append(np.append(np.repeat("#e0ecf4", i.shape[0]), np.repeat("#9ebcda", s.shape[0])),np.repeat("#8856a7", r.shape[0])), 
                         "ind_ID":np.append(np.append(i.ind_ID, s.ind_ID), r.ind_ID),
                         "x":pop.iloc[np.append(np.append(i.ind_ID, s.ind_ID), r.ind_ID)].x,
                         "y":pop.iloc[np.append(np.append(i.ind_ID, s.ind_ID), r.ind_ID)].y})
    plt.scatter(status.x, status.y, c=status.colour, s=60, edgecolors='none')