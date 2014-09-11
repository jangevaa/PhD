""""
individuals.py
Define individuals and their attributes
September 2014
Justin Angevaare
""""

import numpy as np
import pandas as pd

"""Individual information contains disease state, location, group ID, and any other variables which may relate to probability of infection"""

def unif_indvs(n, x1, x2, y1, y2, group):
    """Generates `n`, random uniformly distributed individuals over a cartesian study area bounded East-West by x1 and x2,
    and North-South by `y1` and `y2` with group name `group`.
    """
    if not isinstance(group, str):
        raise AssertionError("Group name must be string")
    return pd.DataFrame({'x':np.random.uniform(x1, x2, n),
                  'y':np.random.uniform(y1, y2, n), 'group':np.repeat(group, n)})
                  
def norm_indvs(n, x_mean, y_mean, x_var, y_var, xy_cov, group):
    """Generates `n`, bivariate normally distributed individuals over a cartesian study area with mean `x_mean, y_mean`, 
    East-West variance of `x_var`, North-South variance of `y_var`, and East-West, North-South covariance `xy_cov`.
    """
    if not isinstance(group, str):
        raise AssertionError("Group name must be string")
    return pd.DataFrame(np.column_stack((np.repeat(group, n),(np.random.multivariate_normal([x_mean, y_mean], [[x_var, xy_cov],[xy_cov, y_var]], n)))), columns=['group', 'x', 'y'])

def multi_groups(x):
    """Combines multiple groups (unique group names are suggested) into a single database for use in the ILM, with the goal being
    to grant the ability to model disease transmission amongst groups isolated geographically by user-defined extents, or
    perhaps to allow for other group dynamics in the future. `x` is tuple of individually defined groups.
    """
    temp=x[0]
    for i in range(1, len(x)):
        temp=temp.append(x[i])
    return temp