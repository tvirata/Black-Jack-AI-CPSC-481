'''
=============================================================================
This code is borrowed from Udacity Reinforcement Nanodegree Course
this is only handles the  plotting Q, when the user presses the P button
from the key board. and this will display the graph of the game status. 
this graph is very important because it proves that the 
Monte Carlo Method of reinforcement learning strategy is working 
after cretan about of time  
I have only the part where player total card sum 
and dealer showing card  and the state value 
=============================================================================
'''
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

def plot_blackjack_values(V, gamesPlayed, wins, losses):

    def get_Z(x, y, usable_ace):
        if (x,y,usable_ace) in V:
            return V[x,y,usable_ace]
        else:
            return 0

    def get_figure(usable_ace, ax):
        x_range = np.arange(11, 22)
        y_range = np.arange(1, 11)
        X, Y = np.meshgrid(x_range, y_range)
        
        Z = np.array([get_Z(x,y,usable_ace) for x,y in zip(np.ravel(X), np.ravel(Y))]).reshape(X.shape)

        surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=plt.cm.coolwarm, vmin=-1.0, vmax=1.0)
        ax.set_xlabel('Player\'s total card Sum')
        ax.set_ylabel('Dealer\'s Showing Card ')
        ax.set_zlabel('State Value')
        ax.view_init(ax.elev, - 120)

    fig = plt.figure(figsize = (10, 10))
    ax = fig.add_subplot(211, projection = '3d')
    
    ax.set_title('Usable Ace: Games Played: ' + str(gamesPlayed) +  ' (Wins: ' + str(wins) + ', Losses: '+str(losses)+')')
    get_figure(True, ax)
    ax = fig.add_subplot(212, projection = '3d')
    ax.set_title('Not Usable Ace: Games Played: ' + str(gamesPlayed) +  ' (Wins: ' + str(wins) + ', Losses: '+str(losses)+')')
    get_figure(False, ax)
    plt.show()
