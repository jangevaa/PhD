"""events.py - a module to generate events relevant to disease dynamics"""

import numpy as np
import pandas as pd
from multiprocessing import Pool

def event_db(n, pop):
    """Create an event database, and with `n` initial infection events, based on a specified population, `pop`."""
    return pd.DataFrame({"time":np.repeat(0, n), 
                         "ind_ID":np.random.choice(pop.index, size=n, replace=False), 
                         "event_type":np.repeat("infection_status",n), 
                         "event_details":np.repeat("i",n)})
    
def omega_s(pop):
    """Susceptibility function - generate a vector of individual specific susceptibility (e.g. related to individual 
    covariates), currently only a constant (of 1) is supported.
    """
    return np.repeat(1, pop.shape[0])
    
def omega_t(pop):
    """Transmissability function - generate a vector of individual specific transmissability (e.g. related to 
    individual covariates), currently only a constant (of 1) is supported.
    """
    return np.repeat(1, pop.shape[0])

def find_infectious(pop, event_db, time):
    """Find individuals which are infected at a specified `time` (i.e.had a change in infection status prior to 
    `time`. Function returns the index of infectious individuals)
    """
    return pd.DataFrame({"ind_ID": event_db[(event_db.event_type=="infection_status") & (event_db.event_details=="i") & (event_db.time<time)].ind_ID})

def find_susceptible(pop, event_db, time):
    """Find individuals which are still susceptible at a specified `time` (i.e. have not had a change in infection status prior to 
    `time`. Function returns the index of susceptible individuals)
    """
    return pd.DataFrame({"ind_ID": np.delete(pop.index, event_db[(event_db.event_type=="infection_status") & (event_db.time<time)].ind_ID)})
        
def euclid_dst_helper(pop, beta, infectious, susceptible):
    """Function to find the sum of euclidean distance**`beta` between a susceptible and all infectious individuals... this function is
    then utilizes `map` to apply to all susceptible individuals in `kappa`.
    """
    
    pop.x[], pop.y
    
    
def kappa(pop, event_db, time, alpha, beta):
    """Infection kernel - risk in relation to a measure of seperation of infected and susceptible individuals"""
    infected=np.array(event_db.ind_ID[(event_db.time<time)&(event_db.event_details=="i")])
    pop.index==any(infected)
    susceptible=np.array(event_db.ind_ID[(event_db.time<time)&(event_db.event_details=="i")])
    euclid_dist(pop, beta, infected, susceptible)
    
    
    
def epsilon(pop, time):
    """Sparks term - infection process which describe some other random behaviour (e.g. infections originating from 
    outside influences). Often assumed as 0, but could be set to be individual, time, and/or epidemic specific
    in some manner. Currently only the zero assumption is supported.
    """
    return np.repeat(0, pop.shape[0])

def si_model(alpha, beta):
    """SI (susceptible, infected) ILM."""

def sir_model(I_dur, alpha, beta):
    """SIR (susceptible, infected, recovered/removed) ILM where the recovery period is constant"""
    
def seir_model(I_dur, alpha, beta):
    """SEIR (susceptible, exposed, infected, recovered/removed) ILM where the latent (exposed), and recovery period 
    are constant
    """