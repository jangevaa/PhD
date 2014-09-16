"""examples.py - file for easily testing functionality and creating examples as program is built"""

pop = unif_indvs(500, 0, 10, 0, 10, 'test_pop')
test = si_model(pop, 1, 10, 1, 10)

"""CSV output testing..."""
test.to_csv("/Users/justin/Dropbox/Projects/[in progress] PhD research/ILM/Simulation/examples/example_event_database.csv")
pop.to_csv("/Users/justin/Dropbox/Projects/[in progress] PhD research/ILM/Simulation/examples/example_pop.csv")

"""Plot output testing..."""
for time in range(0,10):
    plot_infection(pop, test, time)
    savefig("/Users/justin/Dropbox/Projects/[in progress] PhD research/ILM/Simulation/examples/example_time", time, ".png")
