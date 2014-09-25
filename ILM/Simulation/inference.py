"""inference.py - functionality to perform Bayesian inference using MCMC
(Metropolis-Hastings for now) of specific infectious disease models
"""

import scipy as sp
import scipy.special as special
import numpy as np

def pdf_gamma(gamma_alpha, gamma_beta, x):
    """Gamma pdf"""
    if x > 0.:
        return((gamma_beta**gamma_alpha)*(x**(gamma_alpha-1))*np.exp(-gamma_beta*x))/special.gamma(gamma_alpha)
    else:
        return 0.
        
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
    daily_likelihood=[0]*(np.max(event_db.time)-1)
    t=1
    infectious=find_infectious(pop, event_db, t)
    susceptible=find_susceptible(pop, event_db, t)
    for t in range(1, np.max(event_db.time)):
        new_infectious=find_infectious(pop, event_db, t+1)
        new_susceptible=find_susceptible(pop, event_db, t+1)
        infection_probs=infect_prob(pop, alpha, beta, infectious, susceptible)
        def new_infections_func(x):
            return any(susceptible.ind_ID[x] == new_infectious.ind_ID)
        new_infections = map(new_infections_func, susceptible.index)
        daily_likelihood[t-1]=np.prod(np.subtract(1, infection_probs[np.where(np.invert(new_infections))]))*np.prod(infection_probs[np.where(new_infections)])    
        infectious=new_infectious
        susceptible=new_susceptible
    return np.prod(daily_likelihood)
    
def si_infer(pop, event_db, prior_alpha, init_alpha, prior_beta, init_beta, iterations, transition_cov):
    """perform simple Metropolis-Hastings for an SI model with specified
    prior pdfs for alpha and beta (these functions should take a single parameter)
    """
    alpha=[0]*iterations
    beta=[0]*iterations
    density=[0]*iterations
    alpha[0]=init_alpha
    beta[0]=init_beta
    density[0] = si_likelihood(pop, event_db, alpha[0], beta[0])*prior_alpha(alpha[0])*prior_beta(beta[0])
    for i in range(1, iterations):
        proposals = np.random.multivariate_normal([alpha[i-1], beta[i-1]], transition_cov)    
        new_density = si_likelihood(pop, event_db, proposals[0], proposals[1])*prior_alpha(proposals[0])*prior_beta(proposals[1])
        if all([min([1., (new_density/density[i-1])]) > (np.random.uniform(0,1,1)[0]),isinstance(new_density, float)]):
            density[i] = new_density
            alpha[i] = proposals[0]
            beta[i] = proposals[1]
        else:
            density[i] = density[i-1]
            alpha[i] = alpha[i-1]
            beta[i] = beta[i-1]
    return pd.DataFrame({'alpha':alpha, 'beta':beta, 'density':density})
