"""
simulation.py - the main ILM simulation framework, which utilizes several modules to execute an 
event-sourcing-like method of simulating disease dynamics.
"""

import numpy as np
import pandas as pd

def si_model(pop, init, length, alpha, beta):
    """Discrete SI (susceptible, infected) ILM. `init` are the amount of initial infections which are randomly generated
    at time 0. `length` is the simulation length in days."""
    edb = event_db(init, pop)
    for i in range(1, (length+1)):
        edb = infect(pop, alpha, beta, edb, i)
    return edb