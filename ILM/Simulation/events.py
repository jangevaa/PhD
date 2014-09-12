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
    `time`. Function returns the indices of infectious individuals)
    """
    return pd.DataFrame({"ind_ID": event_db[(event_db.event_type=="infection_status") & (event_db.event_details=="i") & (event_db.time<time)].ind_ID})

def find_susceptible(pop, event_db, time):
    """Find individuals which are still susceptible at a specified `time` (i.e. have not had a change in infection status prior to 
    `time`. Function returns the indices of susceptible individuals)
    """
    return pd.DataFrame({"ind_ID": np.delete(pop.index, event_db[(event_db.event_type=="infection_status") & (event_db.time<time)].ind_ID)})

def kappa_helper_1(pop, beta, infectious, susceptible, i, j):
    """Find euclidean distance ^ -`beta` between a susceptible individual `i` and an infectious individual `j`."""
    return np.power(np.sqrt(np.sum(np.power([(pop.x[susceptible.ind_ID[i]] - pop.x[infectious.ind_ID[j]]), (pop.y[susceptible.ind_ID[i]] - pop.y[infectious.ind_ID[j]])], 2))), -beta)
    
def kappa_helper_2(pop, beta, infectious, susceptible, i):
    """Sum the euclidean distance ^-'beta' between all infectious individuals, and a susceptible individual `i`."""
    def kappa_helper_2_sub(j):
        return kappa_helper_1(pop, beta, infectious, susceptible, i, j)
    return np.sum(map(kappa_helper_2_sub, infectious.index))
    
def kappa(pop, beta, event_db, time):
    """Determine which individuals in the `pop` are infectious and susceptible at a specified `time` from the `event_db`,
    then find the euclidean distance between each infectious and susceptible individuals to the power of -`beta`. Return 
    the sum of this for each susceptible individual 
    """
    infectious = find_infectious(pop, event_db, time)
    susceptible = find_susceptible(pop, event_db, time)
    def euclid_dst_sub(i):
        return euclid_dst_helper_2(pop, beta, infectious, susceptible, i)
    return map(euclid_dst_sub, susceptible.index) 
    
def epsilon(pop, time):
    """Sparks term - infection process which describe some other random behaviour (e.g. infections originating from 
    outside influences). Often assumed as 0, but could be set to be individual, time, and/or epidemic specific
    in some manner. Currently only the zero assumption is supported.
    """
    return np.repeat(0, pop.shape[0])

def infect_prob(pop, alpha, beta, event_db, time):
    """Determine infection probabilities for each susceptible individual following ILM framework."""
    return 1-np.exp(np.multiply(-alpha, kappa(pop, beta, event_db, time)))

def si_model(alpha, beta):
    """SI (susceptible, infected) ILM."""

def sir_model(I_dur, alpha, beta):
    """SIR (susceptible, infected, recovered/removed) ILM where the recovery period is constant"""
    
def seir_model(I_dur, alpha, beta):
    """SEIR (susceptible, exposed, infected, recovered/removed) ILM where the latent (exposed), and recovery period 
    are constant
    """