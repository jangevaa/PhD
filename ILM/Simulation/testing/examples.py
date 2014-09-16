"""test.py - file for easily testing functionality as program is built"""

pop = unif_indvs(500, 0, 10, 0, 10, 'test_pop')
test = si_model(pop, 1, 10, 1, 10)

"""Output testing..."
test.to_csv("/Users/justin/Dropbox/Projects/[in progress] PhD research/ILM/Simulation/example_event_database.csv")
pop.to_csv("/Users/justin/Dropbox/Projects/[in progress] PhD research/ILM/Simulation/example_pop.csv")