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

mcmc=si_infer(pop, test, prior_alpha, init_alpha, prior_beta, init_beta, 100, [[1,0],[0,1]])

plt.plot(mcmc.alpha)
plt.plot(mcmc.beta)
plt.plot(mcmc.density)

isinstance(mcmc.density[89], numbers.Real)