import  matplotlib.pyplot as plt

from gwgo import GWGO
from gwo import GWO
from go import GO
from configuration import *

if __name__ == '__main__':
    N = 10
    lower_bound = 5
    upper_bound = 60
    max_iter = 10
    phi = 0.25

    # go = GO(N=N, phase=PHASE, lower_bound=lower_bound, upper_bound=upper_bound, max_iter=max_iter, phi=phi, f=0.5, l=1.5, c_min=0.00001, c_max=1.0)
   
    gwgo = GWGO(N=N, phase=PHASE, lower_bound=lower_bound, upper_bound=upper_bound, max_iter=max_iter, phi=phi, f=0.5, l=1.5, c_min=0.00001, c_max=1.0)
 

    gwo = GWO(N=N, phase=PHASE, lower_bound=lower_bound, upper_bound=upper_bound, max_iter=max_iter, phi=phi, c_min=0.00001, c_max=1.0)
    

    # algorithms = [go, gwo, gwgo]
    # names = ['GO', 'GWO', 'GWGO']
    algorithms = [gwo, gwgo]
    names = ['GWO', 'GWGO']
    historys = []

    for i in range(len(algorithms)):
        historys.append(algorithms[i].show_result(names[i]))

    fig, ax = plt.subplots()
    for i in range(len(historys)):
        ax.plot(historys[i], 'o-', label=names[i])
    ax.set_xticks(range(0, max_iter+1, max_iter//10))
    ax.set_xlabel("Iteration")  
    ax.set_ylabel("Objective Value")
    ax.set_title("Objective Value History")
    ax.legend()
    plt.savefig(OPT_PATH + "history.png")