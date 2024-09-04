import  matplotlib.pyplot as plt

from gwgo import GWGO
from gwo import GWO
from configuration import *

if __name__ == '__main__':
    N = 5
    lower_bound = 5
    upper_bound = 60
    max_iter = 2
    phi = 0.25

    gwgo = GWGO(N=N, phase=PHASE, lower_bound=lower_bound, upper_bound=upper_bound, max_iter=max_iter, phi=phi, f=0.5, l=1.5, c_min=0.00001, c_max=1.0)
    gwgo_history = gwgo.show_result('gwgo')

    gwo = GWO(N=N, phase=PHASE, lower_bound=lower_bound, upper_bound=upper_bound, max_iter=max_iter, phi=phi, c_min=0.00001, c_max=1.0)
    gwo_history = gwo.show_result('gwo')

    fig, ax = plt.subplots()
    ax.plot(gwgo_history, label="gwgo")
    ax.plot(gwo_history, label='gwo')
    ax.set_xlabel("Iteration")  
    ax.set_ylabel("Objective Value")
    ax.legend()
    plt.savefig(OPT_PATH + "history.png")