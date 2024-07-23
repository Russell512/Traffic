import numpy as np
import math
import random
from encoding import encode_net_xml, encode_sumocfg
from sumo_traci import simulationStart
from eq import ObjectValue

class Solution:
    def __init__(self, lower_bound, upper_bound, phases):
        self.position = np.random.uniform(lower_bound, upper_bound, phases)
        self.value = 0

    def update_objective_value(self, net_path, sumocfg_path):
        obj = ObjectValue(net_path, "final.rou.xml", sumocfg_path, "tripinfo.xml", "fcd.xml")
        self.value = obj.getValue()


def calculate_c(t, T, c_min, c_max, phi):
    """
    Calculate the parameter c based on the current iteration
    """
    if t < phi * T:
        return 2 * (1 - t / T)
    else:
        return c_max - (c_max - c_min) * (t / T)
    
def w(r, f, l):
    """
    Weight function for social interaction
    """
    return f * np.exp(-r / l) - np.exp(-r)

def Hunting(s_alpha, s_beta, s_delta, A1, A2, A3, C1, C2, C3, si, N, K):
    p = np.zeros(K)
    X1 = np.zeros(K)
    X2 = np.zeros(K)
    X3 = np.zeros(K)
    for k in range(K):
        X1[k] = s_alpha.position[k] - A1 * abs(C1 * s_alpha.position[k] - si.position[k])
        X2[k] = s_beta.position[k] - A2 * abs(C2 * s_beta.position[k] - si.position[k])
        X3[k] = s_delta.position[k] - A3 * abs(C3 * s_delta.position[k] - si.position[k])
        p[k] = ( X1[k] + X2[k] + X3[k] ) / 3
    return p

def Social_Interaction(i, solutions, si, c, N, K, lower_bound, upper_bound, f, l):
    xi = np.zeros(K)
    for k in range(K):
        interaction_sum = 0
        for j in range(N):
            if i != j:
                d_ij = np.abs(solutions[j].position[k] - si.position[k])
                if d_ij == 0:
                    d_ij = 1e-8
                d_hat_ij = (solutions[j].position[k] - si.position[k]) / d_ij
                interaction_sum += w(d_ij, f, l) * d_hat_ij
        xi[k] = c**2 * (upper_bound - lower_bound) / 2 * interaction_sum
    return xi 

def Hunting_Interaction(p, xi):
    return p + xi

""" < GWGO() > """
def GWGO(N, K, phi, max_iter=7500, lower_bound=5, upper_bound=60, f=0.5, l=1.5, c_min=0.00001, c_max=1.0):
    # 1: Initialization
    solutions = [Solution(K, lower_bound, upper_bound) for i in range(N)]
    for i, si in enumerate(solutions):
        # Encode si into add.xml
        # Run SUMO
        # Calculate the objective value using tripinfos.xml and Eq.(1)
        si.position = [int(round(num)) for num in si.position]
        net_file_name = encode_net_xml(si.position, i+1)
        sumocfg_file_name = encode_sumocfg(net_file_name, i+1)
        simulationStart(sumocfg_file_name)
        si.update_objective_value(net_file_name, sumocfg_file_name)
    solutions = sorted(solutions, key = lambda s: s.value)
    s_alpha = solutions[0]
    s_beta  = solutions[1]
    s_delta = solutions[2]

    """ Iterations start """
    for t in range(max_iter):
        # Print s_alpha every 10 iterations
        # if t % 10 == 0:
        print(f"Iter {t:4d} best fitness = {s_alpha.value:.4f}")

        # 2: Update 
        c = calculate_c(t, max_iter, c_min, c_max, phi)
        for i, si in enumerate(solutions):
            # grey wolf (GW)
            A1 = c * (2 * random.random() - 1)
            A2 = c * (2 * random.random() - 1)
            A3 = c * (2 * random.random() - 1)
            C1 = 2 * random.random()
            C2 = 2 * random.random()
            C3 = 2 * random.random()

            p = Hunting(s_alpha, s_beta, s_delta, A1, A2, A3, C1, C2, C3, si, N, K)

            # grasshopper (GO)
            xi = Social_Interaction(i, solutions, si, c, N, K, lower_bound, upper_bound, f, l)
            
            si.position = Hunting_Interaction(p, xi)
            
        # 3: Evaluation
        for i, si in enumerate(solutions):
            # Encode si into add.xml
            # Run SUMO
            # Calculate the objective value using tripinfos.xml and Eq.(1)
            si.position = [int(round(num)) for num in si.position]
            print("a")
            net_file_name = encode_net_xml(si.position, i+1)
            print("b")
            sumocfg_file_name = encode_sumocfg(net_file_name, i+1)
            print("c")
            simulationStart(sumocfg_file_name)
            print("d")
            si.update_objective_value(net_file_name, sumocfg_file_name)
        solutions = sorted(solutions, key = lambda s: s.value)
        s_alpha = solutions[0]
        s_beta  = solutions[1]
        s_delta = solutions[2]
    """ One iteration ends """

    return s_alpha
""" < End of GWGO() > """

def show_output(N, K, phi, max_iter=7500, lower_bound=5, upper_bound=60, f=0.5, l=1.5, c_min=0.00001, c_max=1.0):
    np.set_printoptions(precision=5, suppress=True)
    print()
    print("################### PROGRAM START ###################")
    print()
    print("==========SETTINGS==========")
    print(f"Number of solutions N = {N}")
    # print(f"Number of intersections = {K//2}")
    print(f"Total phases K = {K}")
    print(f"Lower bound = {lower_bound}")
    print(f"Upper bound = {upper_bound}")
    print(f"Exchange parameter Φ = {phi}")
    print("============================")
    print()
    print()
    print("*************** GWGO START ***************")
    # GWGO()
    best_solution = GWGO(N=N, K=K, phi=phi, max_iter=max_iter, lower_bound=lower_bound, 
                         upper_bound=upper_bound, f=f, l=l, c_min=c_min, c_max=c_max)
    print("************* GWGO COMPLETED *************")
    print()
    print()
    print("Best solution founded:")
    print(best_solution.position)
    print(f"Objective value = {best_solution.value:.4f}")
    print()
    print("################## PROGRAM END ##################")
    print()

if __name__ == '__main__':
    # arguments
    N = 3              # Number of solutions in s
    K = 6               # Number of phases a solution has (在這次的路網共有12個phase)
    phi = 0.5           # Exchange parameter
    max_iter = 100     # Total iterations
    lower_bound = 5     # Min time of each phase
    upper_bound = 60    # Max time of each phase

    f = 0.5             # Attraction force intensity
    l = 1.5             # Attractive length scale
    c_min = 0.00001     # Minimum value of c
    c_max = 1.0         # Maximum value of c

    # set random seeds
    # 設置隨機數種子
    # rnd = random.Random(42)
    # np.random.seed(42)

    show_output(N=N, K=K, phi=phi, max_iter=max_iter, lower_bound=lower_bound, 
                upper_bound=upper_bound, f=f, l=l, c_min=c_min, c_max=c_max)