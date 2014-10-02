"""events.py - a module to generate events relevant to disease dynamics"""

import numpy as np
import pandas as pd

def event_db(n, pop):
    """Create an event database, and with `n` initial infection events, based on a specified population, `pop`."""
    return pd.DataFrame({"time":np.repeat(0, n), 
                         "ind_ID":np.random.choice(pop.index, size=n, replace=False), 
                         "event_type":np.repeat("infection_status",n), 
                         "event_details":np.repeat("i",n)})
    
def find_infectious(pop, event_db, time):
    """Find individuals which have been infected prior to a specified `time` (i.e.had a change in infection status prior to 
    `time`. Function returns the indices of infectious individuals)
    """
    return pd.DataFrame({"ind_ID": event_db[(event_db.event_type=="infection_status") & (event_db.event_details=="i") & (event_db.time<time)].ind_ID})

def find_infectious2(pop, event_db, time):
    """Find individuals which became infected at a specified `time`.
    """
    return pd.DataFrame({"ind_ID": event_db[(event_db.event_type=="infection_status") & (event_db.event_details=="i") & (event_db.time==(time-1))].ind_ID})

def find_susceptible(pop, event_db, time):
    """Find individuals which are still susceptible at a specified `time` (i.e. have not had a change in infection status prior to 
    `time`. Function returns the indices of susceptible individuals)
    """
    return pd.DataFrame({"ind_ID": np.delete(pop.index, event_db[(event_db.event_type=="infection_status") & (event_db.time<time)].ind_ID)})

def find_recovered(pop, event_db, time):
    """Find individuals which have recovered prior to a specified `time` (i.e.had a change in infection status prior to 
    `time`. Function returns the indices of recovered individuals)
    """
    return pd.DataFrame({"ind_ID": np.delete(pop.index, event_db[(event_db.event_type=="infection_status") & (event_db.event_details=="r") & (event_db.time<time)].ind_ID)})


def kappa_helper_1(pop, beta, infectious, susceptible, i, j):
    """Find euclidean distance ^ -`beta` between a susceptible individual `i` and an infectious individual `j`."""
    return np.power(np.sqrt(np.sum(np.power([(pop.x[susceptible.ind_ID[i]] - pop.x[infectious.ind_ID[j]]), (pop.y[susceptible.ind_ID[i]] - pop.y[infectious.ind_ID[j]])], 2))), -beta)
    
def kappa_helper_2(pop, beta, infectious, susceptible, i):
    """Sum the euclidean distance ^-'beta' between all infectious individuals, and a susceptible individual `i`."""
    def kappa_helper_2_sub(j):
        return kappa_helper_1(pop, beta, infectious, susceptible, i, j)
    return np.sum(map(kappa_helper_2_sub, infectious.index))
    
def kappa(pop, beta, infectious, susceptible):
    """Determine which individuals in the `pop` are infectious and susceptible at a specified `time` from the `event_db`,
    then find the euclidean distance between each infectious and susceptible individuals to the power of -`beta`. Return 
    the sum of this for each susceptible individual 
    """
    def kappa_sub(i):
        return kappa_helper_2(pop, beta, infectious, susceptible, i)
    return map(kappa_sub, susceptible.index)
    
def infect_prob(pop, alpha, beta, infectious, susceptible):
    """Determine infection probabilities for each susceptible individual following ILM framework."""
    return 1-np.exp(np.multiply(-alpha, kappa(pop, beta, infectious, susceptible)))

def infect(pop, alpha, beta, event_db, time):
    """Probablistically propagate disease, and return an updated event database."""
    infectious = find_infectious(pop, event_db, time)
    susceptible = find_susceptible(pop, event_db, time)
    prob = infect_prob(pop, alpha, beta, infectious, susceptible)
    new_infections = susceptible.ind_ID[np.asarray(np.where(prob > np.random.uniform(0, 1, size=prob.size))).flat]
    return pd.DataFrame({"time":np.append(event_db.time, np.repeat(time, new_infections.size)), 
                         "ind_ID":np.append(event_db.ind_ID, new_infections), 
                         "event_type":np.append(event_db.event_type, np.repeat("infection_status",new_infections.size)), 
                         "event_details":np.append(event_db.event_details, np.repeat("i",new_infections.size))})

def constant_recover(pop, event_db, time, gamma):
    """Individuals recover after a specified infection duration, `gamma` (constant)."""
    recovered = np.array(find_infectious2(pop, event_db, time-gamma).ind_ID)
    return pd.DataFrame({"time":np.append(event_db.time, np.repeat(time, recovered.size)), 
                         "ind_ID":np.append(event_db.ind_ID, recovered), 
                         "event_type":np.append(event_db.event_type, np.repeat("infection_status",recovered.size)), 
                         "event_details":np.append(event_db.event_details, np.repeat("r",recovered.size))})
    

#Unused or incomplete functions currently below this line
#
#def omega_s(pop):
#    """Susceptibility function - generate a vector of individual specific susceptibility (e.g. related to individual 
#    covariates), currently only a constant (of 1) is supported.
#    """
#    return np.repeat(1, pop.shape[0])
#    
#def omega_t(pop):
#    """Transmissability function - generate a vector of individual specific transmissability (e.g. related to 
#    individual covariates), currently only a constant (of 1) is supported.
#    """
#    return np.repeat(1, pop.shape[0])
#
#
#def epsilon(pop, time):
#    """Sparks term - infection process which describe some other random behaviour (e.g. infections originating from 
#    outside influences). Often assumed as 0, but could be set to be individual, time, and/or epidemic specific
#    in some manner. Currently only the zero assumption is supported.
#    """
#    return np.repeat(0, pop.shape[0])
#
#def sir_model(I_dur, alpha, beta):
#    """SIR (susceptible, infected, recovered/removed) ILM where the recovery period is constant"""
#    
#def seir_model(I_dur, alpha, beta):
#    """SEIR (susceptible, exposed, infected, recovered/removed) ILM where the latent (exposed), and recovery period 
#    are constant
#    """
