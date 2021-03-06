"""events.py - a module to generate events relevant to disease dynamics"""

import numpy as np
import pandas as pd

__all__ = ['find_infectious', 'find_susceptible', 'find_nonrecovered', 'find_recovered', 'find_recoverytimes', 'infect_prob', 'infect', 'constant_recover', 'geometric_recover']

def event_db(n, pop):
    """Create an event database, and with `n` initial infection events, based on a specified population, `pop`."""
    return pd.DataFrame({"time":np.repeat(0, n), 
                         "ind_ID":np.random.choice(pop.index, size=n, replace=False), 
                         "event_type":np.repeat("infection_status",n), 
                         "event_details":np.repeat("i",n)})
    
def find_infectious(event_db, time):
    """Find individuals which have been infected prior to a specified `time` (i.e. had a change in infection status prior to 
    `time`. Function returns the indices of infectious individuals)
    """
    return pd.DataFrame({"ind_ID": event_db[(event_db.event_type=="infection_status") & (event_db.event_details=="i") & (event_db.time<time)].ind_ID})

def find_infectious2(event_db, time):
    """Find individuals which became infected at a specified `time`.
    """
    return pd.DataFrame({"ind_ID": event_db[(event_db.event_type=="infection_status") & (event_db.event_details=="i") & (event_db.time==(time-1))].ind_ID})
    
def find_susceptible(pop, event_db, time):
    """Find individuals which are still susceptible at a specified `time` (i.e. have not had a change in infection status prior to 
    `time`. Function returns the indices of susceptible individuals)
    """
    return pd.DataFrame({"ind_ID": np.delete(pop.index, event_db[(event_db.event_type=="infection_status") & (event_db.time<time)].ind_ID)})
    
def find_nonrecovered(event_db, time):
    """Find individuals which have been infected prior to `time`, but which have not yet recovered.
    """
    recovered = pd.DataFrame({"ind_ID": event_db[(event_db.event_type=="infection_status") & (event_db.event_details=="r") & (event_db.time<time)].ind_ID})
    nonrecovered = pd.DataFrame({"ind_ID": event_db[(event_db.event_type=="infection_status") & (event_db.event_details=="i") & (event_db.time<time)].ind_ID})
    def find_nonrecovered_helper(x):
        return np.any(nonrecovered.ind_ID[x] == recovered.ind_ID)
    return nonrecovered[np.invert(map(find_nonrecovered_helper, nonrecovered.index))]        

def find_recovered(event_db, time):
    """Find individuals which have recovered prior to a specified `time` (i.e.had a change in infection status prior to 
    `time`. Function returns the indices of recovered individuals)
    """
    return pd.DataFrame({"ind_ID": event_db[(event_db.event_type=="infection_status") & (event_db.event_details=="r") & (event_db.time<time)].ind_ID})
    
def find_recoverytimes(event_db):
    """List infection times for all individuals which have recovered..."""
    recovered = np.array(event_db.ind_ID[(event_db.event_type == "infection_status") & (event_db.event_details == "r")])
    def find_recoverytimes_helper(x):
        return np.array(event_db.time[(event_db.event_type == "infection_status") &
                                      (event_db.event_details == "r") & 
                                      (event_db.ind_ID==recovered[x])])[0] - np.array(event_db.time[
                                      (event_db.event_type == "infection_status") & 
                                      (event_db.event_details == "i") & 
                                      (event_db.ind_ID==recovered[x])])[0]
    return np.array(map(find_recoverytimes_helper, range(0, recovered.shape[0])))
    
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
    infectious = find_nonrecovered(event_db, time)
    susceptible = find_susceptible(pop, event_db, time)
    prob = infect_prob(pop, alpha, beta, infectious, susceptible)
    new_infections = susceptible.ind_ID[np.asarray(np.where(np.greater(prob,np.random.uniform(0, 1, size=prob.size)))).flat]
    return pd.DataFrame({"time":np.append(event_db.time, np.repeat(time, new_infections.size)), 
                         "ind_ID":np.append(event_db.ind_ID, new_infections), 
                         "event_type":np.append(event_db.event_type, np.repeat("infection_status",new_infections.size)), 
                         "event_details":np.append(event_db.event_details, np.repeat("i",new_infections.size))})

def constant_recover(pop, event_db, time, gamma):
    """Individuals recover after a specified infection duration, `gamma` (constant)."""
    recovered = np.array(find_infectious2(event_db, time-gamma).ind_ID)
    return pd.DataFrame({"time":np.append(event_db.time, np.repeat(time, recovered.size)), 
                         "ind_ID":np.append(event_db.ind_ID, recovered), 
                         "event_type":np.append(event_db.event_type, np.repeat("infection_status",recovered.size)), 
                         "event_details":np.append(event_db.event_details, np.repeat("r",recovered.size))})
    
def geometric_recover(pop, event_db, time, gamma):
    """Individuals recover following a memoryless recovery probability each time invoked (i.e. geometric).
    The mean recovery period is `gamma` - which is equal to 1/p in the geometric distribution.
    """
    nonrecovered=find_nonrecovered(event_db, time)
    recovered = np.array(nonrecovered.ind_ID[(1./gamma)>np.random.uniform(0,1, nonrecovered.shape[0])])
    return pd.DataFrame({"time":np.append(event_db.time, np.repeat(time, recovered.size)), 
                         "ind_ID":np.append(event_db.ind_ID, recovered), 
                         "event_type":np.append(event_db.event_type, np.repeat("infection_status",recovered.size)), 
                         "event_details":np.append(event_db.event_details, np.repeat("r",recovered.size))})
