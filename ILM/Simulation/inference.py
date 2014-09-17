"""inference.py - functionality to perform Bayesian inference using MCMC
(Metropolis-Hastings for now) of specific infectious disease models
"""

import scipy as sp
import scipy.special as sp.special
import numpy as np

def pdf_gamma(gamma_alpha, gamma_beta, x):
    return((gamma_beta**gamma_alpha)*(x**(gamma_alpha-1))*np.exp(-gamma_beta*x))/special.gamma(gamma_alpha)

def pdf_unif(lower, upper, x):
    return where(lower < x < upper, 1/(upper-lower), 0)


def si_infer(pop, event_db, prior_alpha, prior_beta, iterations):
    """perform simple Metropolis-Hastings for an SI model with specified
    prior pdfs for alpha and beta (these functions should take a single parameter)
    """
