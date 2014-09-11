"""individuals.py - a module to define individuals and their attributes"""

import numpy as np
import pandas as pd

def unif_indvs(n, x1, x2, y1, y2, group):
    """Generates `n`, random uniformly distributed individuals over a cartesian study area bounded East-West by x1 and x2,
    and North-South by `y1` and `y2` with group name `group`.
    """
    if not isinstance(group, str):
        raise AssertionError("Group name must be string")
    return pd.DataFrame({'x':np.random.uniform(x1, x2, n),
                  'y':np.random.uniform(y1, y2, n), 'group':np.repeat(group, n), 'ID_ingroup':range(0, n)})
                  
def norm_indvs(n, x_mean, y_mean, x_var, y_var, xy_cov, group):
    """Generates `n`, bivariate normally distributed individuals over a cartesian study area with mean `x_mean, y_mean`, 
    East-West variance of `x_var`, North-South variance of `y_var`, and East-West, North-South covariance `xy_cov`.
    """
    if not isinstance(group, str):
        raise AssertionError("Group name must be string")
    return pd.DataFrame(np.column_stack((range(0, n),np.repeat(group, n),
    (np.random.multivariate_normal([x_mean, y_mean], [[x_var, xy_cov],[xy_cov, y_var]], n)))), columns=['ID_ingroup','group', 'x', 'y'])

def multi_groups(x):
    """Combines multiple groups (unique group names are suggested) into a single database for use in the ILM, with the goal being
    to grant the ability to model disease transmission amongst groups isolated geographically by user-defined extents, or perhaps
    to allow for other group dynamics in the future. The single argument `x` here is tuple of individually defined groups.
    """
    temp=x[0]
    for i in range(1, len(x)):
        temp=temp.append(x[i])
    temp.index=range(0, temp.shape[0])
    return temp