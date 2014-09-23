"""inference.py - functionality to perform Bayesian inference using MCMC
(Metropolis-Hastings for now) of specific infectious disease models
"""

import scipy as sp
import scipy.special as special
import numpy as np

def pdf_gamma(gamma_alpha, gamma_beta, x):
    """Gamma pdf"""
    return((gamma_beta**gamma_alpha)*(x**(gamma_alpha-1))*np.exp(-gamma_beta*x))/special.gamma(gamma_alpha)

def pdf_unif(lower, upper, x):
    """Uniform pdf"""
    def pdf_unif(x):
        if lower < x < upper:
            return 1./(upper-lower)
        else:
            return 0.
    return map(pdf_unif, x)
    
def pdf_norm(mean, var, x):
    """Normal pdf"""
    return np.exp(-((x-mean)**2)/(2*var))/np.sqrt(2*np.pi*var)

def si_likelihood(pop, event_db, alpha, beta):
    """Determine the likelihood of the data from an SI simulation given alpha 
    and beta
    """
    t=2
    # Probability of staying susceptible = 1-probability of infection
    #for t in range(1, np.max(event_db.time))
    infectious=find_infectious(pop, event_db, t)
    susceptible=find_susceptible(pop, event_db, t)
    new_infectious=find_infectious(pop, event_db, t+1)
    new_susceptible=find_susceptible(pop, event_db, t+1)
    infection_probs=infect_prob(pop, alpha, beta, infectious, susceptible)
    def new_infections_func(x):
        return any(susceptible.ind_ID[x] == new_infectious.ind_ID)
    new_infections = map(new_infections_func, susceptible.index)
    return np.prod(np.subtract(1, infection_probs[np.where(np.invert(new_infections))]))*np.prod(infection_probs[np.where(new_infections)])

                
    #still_susceptible = susceptible.ind_ID == any(find_susceptible(pop, event_db, t+1).ind_ID)
    return new_infections
    #return np.where(new_infections)
    #return infection_probs[np.where(new_infections)]
    
    #find_susceptible(pop, event_db, t+1)
    
    
def si_infer(pop, event_db, prior_alpha, prior_beta, iterations):
    """perform simple Metropolis-Hastings for an SI model with specified
    prior pdfs for alpha and beta (these functions should take a single parameter)
    """
