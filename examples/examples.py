"""examples.py - file for easily testing functionality and creating examples as program is built"""

import time

"""Generate population and propagate infection with SI model..."""
pop = unif_indvs(100, 0, 10, 0, 10, 'test_pop')
test1 = si_model(pop, 1, 10, 1, 10)

"""CSV output testing..."""
savedir="/Users/justin/Dropbox/Projects/[in progress] PhD research/ILM/Simulation/testing/"

test.to_csv(savedir+"example_event_database.csv")
pop.to_csv(savedir+"example_pop.csv")

"""Plot output testing..."""
for time in range(0,10):
    plot_si(pop, test, time)
    savefig(savedir + "example_time" + str(time) + ".png")

"""Inference testing..."""

"""Define prior distributions for alpha and beta"""

def prior_alpha(x):
    gamma_alpha=5
    gamma_beta=1
    return pdf_gamma(gamma_alpha, gamma_beta, x)
    
def prior_beta(x):
    gamma_alpha=5
    gamma_beta=1
    return pdf_gamma(gamma_alpha, gamma_beta, x)
    
init_alpha=np.random.gamma(5, 1)

init_beta=np.random.gamma(5, 1)

mcmc=si_infer(pop, test, prior_alpha, 1, prior_beta, 10, 1000, [[1,0],[0,4]])

plt.plot(mcmc.alpha)
plt.plot(mcmc.beta)
plt.plot(mcmc.density)

"""Estimate optimal proposal covariance as (Rosenthal)"""
optcov=numpy.cov(mcmc.alpha, mcmc.beta)*((2.38**2.)/2.)

mcmc=si_infer(pop, test, prior_alpha, 1, prior_beta, 10, 5000, optcov)

plt.plot(mcmc.alpha)
savefig(savedir + "example_mcmc_alpha.png")

plt.plot(mcmc.beta)
savefig(savedir + "example_mcmc_beta.png")

plt.plot(mcmc.density)
savefig(savedir + "example_mcmc_density.png")

################

"""Test SIcR model simulation..."""
pop = unif_indvs(100, 0, 10, 0, 10, 'test_pop')
test2 = sicr_model(pop, 1, 30, 1, 10, 3)

for time in range(1,30):
    plot_sir(pop, test1, time)
    savefig(savedir + "SIcR_example_time" + str(time) + ".png")
 
################
      
"""Test SIR model simulation..."""
pop = unif_indvs(100, 0, 10, 0, 10, 'test_pop')
test3 = sir_model(pop, 1, 30, 1, 10, 3)

"""SIR Plotting..."""
for time in range(1,(np.max(test3.time)+1)):
    plot_sir(pop, test3, time)
    savefig(savedir + "SIR_example_time" + str(time) + ".png")
    
"""SIR Inference..."""
def prior_alpha(x):
    gamma_alpha=5
    gamma_beta=1
    return pdf_gamma(gamma_alpha, gamma_beta, x)

def prior_beta(x):
    gamma_alpha=5
    gamma_beta=1
    return pdf_gamma(gamma_alpha, gamma_beta, x)

def prior_gamma(x):
    gamma_alpha=5
    gamma_beta=1
    return pdf_gamma(gamma_alpha, gamma_beta, x)
                
init_alpha=np.random.gamma(5, 1)

init_beta=np.random.gamma(5, 1)

init_gamma=np.random.gamma(5, 1)

start_time=time.time()
mcmc=sir_infer(pop, test3, prior_alpha, init_alpha, prior_beta, init_beta, init_gamma, prior_gamma, 500, [[1,0,0,],[0,4,0],[0,0,1]])
end_time = time.time() - start_time