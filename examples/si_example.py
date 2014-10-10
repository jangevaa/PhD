"""SI_example.py - demonstrate SI model related functionality of ilmtools"""

import ilmtools as ilm
import time

"""Generate a population over a random uniform 10 x 10 area"""
pop = ilm.unif_indvs(100, 0, 10, 0, 10, 'test_pop')

"""From a single initial case, propagate an SI disease through the simulated
population over 10 days, with `alpha=1`, and `beta=2`
"""
cases = ilm.si_model(pop, 1, 10, 1, 10)

