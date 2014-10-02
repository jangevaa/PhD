"""output.py - a number of output options (visualizations and text)"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation

"""csv output instructions: you can easily export a csv of the population file or the
event database by using the `DF.to_csv("/dir/ect/ory/")`, where DF represents the data
that will be exported.
"""

def plot_si(pop, event_db, time):
    """This will create a simple scatterplot of susceptible and infectious individuals at
    a given time
    """
    i=find_infectious(pop, event_db, time)
    s=find_susceptible(pop, event_db, time)
    status=pd.DataFrame({"status":np.append(np.repeat("i", i.shape[0]), np.repeat("s", s.shape[0])), 
                         "colour":np.append(np.repeat("k", i.shape[0]), np.repeat("b", s.shape[0])),
                         "ind_ID":np.append(i.ind_ID, s.ind_ID),
                         "x":pop.iloc[np.append(i.ind_ID, s.ind_ID)].x,
                         "y":pop.iloc[np.append(i.ind_ID, s.ind_ID)].y})
    plt.scatter(status.x, status.y, c=status.colour)

def plot_sicr(pop, event_db, time):
    """This will create a simple scatterplot of susceptible, infectious, and recovered
    individuals at a given time
    """
    i=find_nonrecovered(pop, event_db, time)
    s=find_susceptible(pop, event_db, time)
    r=find_recovered(pop, event_db, time)
    status=pd.DataFrame({"status":np.append(np.append(np.repeat("i", i.shape[0]), np.repeat("s", s.shape[0])),np.repeat("r", r.shape[0])),
                         "colour":np.append(np.append(np.repeat("k", i.shape[0]), np.repeat("b", s.shape[0])),np.repeat("m", r.shape[0])), 
                         "ind_ID":np.append(np.append(i.ind_ID, s.ind_ID), r.ind_ID),
                         "x":pop.iloc[np.append(np.append(i.ind_ID, s.ind_ID), r.ind_ID)].x,
                         "y":pop.iloc[np.append(np.append(i.ind_ID, s.ind_ID), r.ind_ID)].y})
    return status
    plt.scatter(status.x, status.y, c=status.colour)


#Unused or incomplete functions currently below this line    
#            
#def infection_animation(pop, event_db):
#    """This will create an animation of infection spread."""
#    fig = plt.figure()
#    ax = plt.axes(xlim=(np.floor(min(pop.x)), np.ceil(max(pop.x))), ylim=(np.floor(min(pop.y)), np.ceil(max(pop.y))))
#    scatter, = ax.plot([], [], lw=2)
#    def init():
#        scatter.set_data([], [])
#        return scatter,
#    def animate(time):
#        i = find_infectious(pop, event_db, time)
#        s = find_susceptible(pop, event_db, time)
#        c = np.append(np.repeat("r", i.shape[0]), np.repeat("k", s.shape[0]))
#        x=pop.iloc[np.append(i.ind_ID, s.ind_ID)].x
#        y=pop.iloc[np.append(i.ind_ID, s.ind_ID)].y
#        scatter.set_data(x, y)
#        return scatter,
#    anim = animation.FuncAnimation(fig, animate, init_func=init,
#                                   frames=10, interval=1, blit=True)        
#    anim.save('infection_spread.mp4', fps=1, extra_args=['-vcodec', 'libx264'])
#    
#def main(pop, event_db):
#    numframes = max(np.ceil(event_db.time))
#    time=0
#    d = find_infectious(pop, event_db, time)
#    s = find_susceptible(pop, event_db, time)
#    c = np.append(np.repeat("r", d.shape[0]), np.repeat("k", s.shape[0]))
#    x=pop.iloc[np.append(d.ind_ID, s.ind_ID)].x
#    y=pop.iloc[np.append(d.ind_ID, s.ind_ID)].y
#    fig = plt.figure()
#    scat = plt.scatter(x=x, y=y, c=c)
#    def update_plot(i):
#        d = find_infectious(pop, event_db, i)
#        s = find_susceptible(pop, event_db, i)
#        c = np.append(np.repeat("r", d.shape[0]), np.repeat("k", s.shape[0]))
#        scat.set_data(x=x,y=y,c=c)
#        return scat,
#    ani = animation.FuncAnimation(fig, update_plot, frames=10)
#    #ani.save('infection_spread.mp4', fps=1, extra_args=['-vcodec', 'libx264'])
#
#main(pop, test)     