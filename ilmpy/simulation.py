"""simulation.py - the main ILM simulation framework, which utilizes several modules to execute an 
event-sourcing-like method of simulating disease dynamics.
"""

from events import event_db, infect, constant_recover, geometric_recover

__all__ = ['si_model', 'sicr_model', 'sir_model']

def si_model(pop, init, length, alpha, beta):
    """Discrete SI (susceptible, infected) ILM. `init` are the amount of initial infections which are randomly generated
    at time 0. `length` is the simulation length in days.
    """
    edb = event_db(init, pop)
    for i in range(1, (length+1)):
        edb = infect(pop, alpha, beta, edb, i)
    return edb
    
def sicr_model(pop, init, length, alpha, beta, gamma):
    """Discrete SIR (susceptible, infected, recovered) ILM. `init` are the amount of initial infections which are randomly generated
    at time 0. `length` is the simulation length in days. Recovery period is a constant, `gamma`.
    """
    edb = event_db(init, pop)
    for i in range(1, (length+1)):
        edb = infect(pop, alpha, beta, edb, i)
        edb = constant_recover(pop, edb, i, gamma)
    return edb
    
def sir_model(pop, init, length, alpha, beta, gamma):
    """Discrete SIR (susceptible, infected, recovered) ILM. `init` are the amount of initial infections which are randomly generated
    at time 0. `length` is the simulation length in days. Mean recovery period `gamma` is equivalent to the mean of the geometric
    distribution.
    """
    edb = event_db(init, pop)
    for i in range(1, (length+1)):
        edb = infect(pop, alpha, beta, edb, i)
        edb = geometric_recover(pop, edb, i, gamma)
    return edb