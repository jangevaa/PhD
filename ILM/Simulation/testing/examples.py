"""examples.py - file for easily testing functionality and creating examples as program is built"""

"""Generate population and propagate infection..."""
pop = unif_indvs(100, 0, 10, 0, 10, 'test_pop')
test = si_model(pop, 1, 10, 1, 10)

"""CSV output testing..."""
savedir="/Users/justin/Dropbox/Projects/[in progress] PhD research/ILM/Simulation/testing/"

test.to_csv(savedir+"example_event_database.csv")
pop.to_csv(savedir+"example_pop.csv")

"""Plot output testing..."""
for time in range(0,10):
    plot_infection(pop, test, time)
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


"""Test SIR model simulation..."""
pop = unif_indvs(100, 0, 10, 0, 10, 'test_pop')
test1 = sicr_model(pop, 1, 10, 1, 10, 5)