# Define individuals and their attributes
# September 2014
# Justin Angevaare

import numpy as np
import pandas as pd

"""Individual information contains disease state, location, and any other variables which may relate to probability of infection"""

def unif_indvs(n, x, y):
    """Generates `n`, random uniformly distributed individuals over a cartesian study area bounded East-West by x1 and x2,
    and bounded North-South by `y1` and `y2`.
    """
    return pd.DataFrame({'x':np.random.uniform(x1, x2, n),
                  'y':np.random.uniform(y2, y2, n)})
                  
def norm_indvs(n, x_mean, y_mean, x_var, y_var, xy_cov):
    """Generates `n`, bivariate normally distributed individuals over a cartesian study area with mean `x_mean, y_mean`, 
    East-West variance of `x_var`, North-South variance of `y_var`, and East-West, North-South covariance `xy_cov`.
    """
    return pd.DataFrame(np.random.multivariate_normal([x_mean, y_mean], [[x_var, xy_cov],[xy_cov, y_var]], n), columns=['x', 'y'])
    
    

