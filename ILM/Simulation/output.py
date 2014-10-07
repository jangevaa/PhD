"""output.py - a number of output options (visualizations and text)"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

"""csv output instructions: you can easily export a csv of the population file or the
event database by using the `DF.to_csv("/dir/ect/ory/")`, where DF represents the data
that will be exported.
"""

def plot_si(pop, event_db, time):
    """This will create a simple scatterplot of susceptible and infectious individuals at
    a given time
    """
    i=find_infectious(event_db, time)
    s=find_susceptible(pop, event_db, time)
    status=pd.DataFrame({"status":np.append(np.repeat("i", i.shape[0]), np.repeat("s", s.shape[0])), 
                         "colour":np.append(np.repeat("k", i.shape[0]), np.repeat("b", s.shape[0])),
                         "ind_ID":np.append(i.ind_ID, s.ind_ID),
                         "x":pop.iloc[np.append(i.ind_ID, s.ind_ID)].x,
                         "y":pop.iloc[np.append(i.ind_ID, s.ind_ID)].y})
    plt.scatter(status.x, status.y, c=status.colour, s=60, edgecolors='none')

def plot_sir(pop, event_db, time):
    """This will create a simple scatterplot of susceptible, infectious, and recovered
    individuals at a given time
    """
    i=find_nonrecovered(event_db, time)
    s=find_susceptible(pop, event_db, time)
    r=find_recovered(event_db, time)
    status=pd.DataFrame({"status":np.append(np.append(np.repeat("i", i.shape[0]), np.repeat("s", s.shape[0])),np.repeat("r", r.shape[0])),
                         "colour":np.append(np.append(np.repeat("#a6cee3", i.shape[0]), np.repeat("#1f78b4", s.shape[0])),np.repeat("#b2df8a", r.shape[0])), 
                         "ind_ID":np.append(np.append(i.ind_ID, s.ind_ID), r.ind_ID),
                         "x":pop.iloc[np.append(np.append(i.ind_ID, s.ind_ID), r.ind_ID)].x,
                         "y":pop.iloc[np.append(np.append(i.ind_ID, s.ind_ID), r.ind_ID)].y})
    plt.scatter(status.x, status.y, c=status.colour, s=60, edgecolors='none')
    
def epi_curve(event_db):
    """Display curve with the number of infected individuals at each time point"""
    num_infected = [0]*(np.max(event_db.time)-1)
    for t in range(1, np.max(event_db.time)):
        num_infected[t-1] = find_nonrecovered(event_db, t).shape[0]
    plt.plot(range(1, np.max(event_db.time)), num_infected, linewidth=2)
                