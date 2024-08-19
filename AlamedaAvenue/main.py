import numpy as np
import time
import matplotlib.pyplot as plt

from configuration import *
from encoding import encode
from sumo_traci import simulationStart
from evaluate import ObjectValue


class Solution:
    def __init__(self, lower_bound, upper_bound, phase):
        self.duration = np.random.randint(
            lower_bound, upper_bound + 1, size=phase)
        self.value = 0

    def evaluate(self, i):
        add_path = HIS_PATH + str(i) + '.add.xml'
        tripinfo_path = HIS_PATH + str(i) + '.tripinfo.xml'
        fcd_path = HIS_PATH + str(i) + '.fcd.xml'
        obj = ObjectValue(add_path, tripinfo_path, fcd_path)
        self.value = obj.evaluate()


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
        X1[k] = s_alpha.duration[k] - A1 * \
            abs(C1 * s_alpha.duration[k] - si.duration[k])
        X2[k] = s_beta.duration[k] - A2 * \
            abs(C2 * s_beta.duration[k] - si.duration[k])
        X3[k] = s_delta.duration[k] - A3 * \
            abs(C3 * s_delta.duration[k] - si.duration[k])
        p[k] = (X1[k] + X2[k] + X3[k]) / 3
    return p


def Social_Interaction(i, solutions, si, c, N, K, lower_bound, upper_bound, f, l):
    xi = np.zeros(K)
    for k in range(K):
        interaction_sum = 0
        for j in range(N):
            if i != j:
                d_ij = np.abs(solutions[j].duration[k] - si.duration[k])
                if d_ij == 0:
                    d_ij = 1e-8
                d_hat_ij = (solutions[j].duration[k] - si.duration[k]) / d_ij
                interaction_sum += w(d_ij, f, l) * d_hat_ij
        xi[k] = c**2 * (upper_bound - lower_bound) / 2 * interaction_sum
    return xi


def Hunting_Interaction(p, xi):
    return p + xi


""" < GWGO() > """


def GWGO(N, phase, phi, max_iter=7500, lower_bound=5, upper_bound=60, f=0.5, l=1.5, c_min=0.00001, c_max=1.0):
    # 1: Initialization
    solutions = [Solution(lower_bound, upper_bound, phase) for i in range(N)]
    start = time.time()
    history = []

    print("Initialization")
    for i, si in enumerate(solutions):
        sumocfg_path = encode(ADD_XML, SUMOCFG, i, si.duration)
        simulationStart(HIS_PATH + sumocfg_path, SIM_TIME)
        si.evaluate(i)
    solutions = sorted(solutions, key=lambda s: s.value)
    s_alpha = solutions[0]
    s_beta = solutions[1]
    s_delta = solutions[2]

    """ Iterations start """
    for t in range(max_iter):
        print(
            f"\nIter {t+1:4d}/{max_iter}\t Time used: {time.time() - start:.2f} sec")

        # 2: Update
        c = calculate_c(t, max_iter, c_min, c_max, phi)
        for i, si in enumerate(solutions):
            # grey wolf (GW)
            A1 = c * (2 * np.random.random() - 1)
            A2 = c * (2 * np.random.random() - 1)
            A3 = c * (2 * np.random.random() - 1)
            C1 = 2 * np.random.random()
            C2 = 2 * np.random.random()
            C3 = 2 * np.random.random()

            p = Hunting(s_alpha, s_beta, s_delta, A1,
                        A2, A3, C1, C2, C3, si, N, phase)

            # grasshopper (GO)
            xi = Social_Interaction(
                i, solutions, si, c, N, phase, lower_bound, upper_bound, f, l)

            si.duration = Hunting_Interaction(p, xi)

        # 3: Evaluation
        for i, si in enumerate(solutions):
            si.duration = [int(round(num)) for num in si.duration]
            for j in range(len(si.duration)):
                if si.duration[j] < lower_bound:
                    si.duration[j] = lower_bound
                elif si.duration[j] > upper_bound:
                    si.duration[j] = upper_bound
            sumocfg_path = encode(ADD_XML, SUMOCFG, i, si.duration)
            simulationStart(HIS_PATH + sumocfg_path, SIM_TIME)
            si.evaluate(i)
        solutions = sorted(solutions, key=lambda s: s.value)
        s_alpha = solutions[0]
        s_beta = solutions[1]
        s_delta = solutions[2]

        print("\nDuration: ", end="")
        print(s_alpha.duration)
        print(f"Current objective value = {s_alpha.value:.4f}")
        history.append(s_alpha.value)
    """ One iteration ends """

    return s_alpha, history


""" < End of GWGO() > """


def GWGO_run(N, phase, phi, max_iter=7500, lower_bound=5, upper_bound=60, f=0.5, l=1.5, c_min=0.00001, c_max=1.0):
    print()
    print("################### PROGRAM START ###################")
    print()
    start = time.time()
    print("*************** GWGO START ***************")

    best_solution, history = GWGO(N=N, phase=phase, phi=phi, max_iter=max_iter,
                                  lower_bound=lower_bound, upper_bound=upper_bound, f=f, l=l, c_min=c_min, c_max=c_max)
    plt.plot(history)
    plt.savefig("history.png")

    print()
    print("************* GWGO COMPLETED *************")
    print()
    print("==========SETTINGS==========")
    print(f"Number of solutions N = {N}")
    print(f"Total phases = {phase}")
    print(f"Lower bound = {lower_bound}")
    print(f"Upper bound = {upper_bound}")
    print(f"Exchange parameter Φ = {phi}")
    print("============================")
    print()
    print("Best solution founded:")
    print(best_solution.duration)
    print(f"Objective value = {best_solution.value:.4f}")
    print(f"Total time used: {time.time() - start:.2f} sec")
    print()
    sumocfg_path = encode(ADD_XML, SUMOCFG, 'optimal', best_solution.duration)
    print(
        f"Simulation configuration file '{sumocfg_path}' has been generated.")
    print()
    print("################## PROGRAM END ##################")
    print()


if __name__ == '__main__':
    # arguments
    N = 30              # Number of solutions in s
    phase = PHASE          # Number of phases a solution has
    phi = 0.5           # Exchange parameter
    max_iter = 1000     # Total iterations
    lower_bound = 5     # Min time of each phase
    upper_bound = 60    # Max time of each phase

    f = 0.5             # Attraction force intensity
    l = 1.5             # Attractive length scale
    c_min = 0.00001     # Minimum value of c
    c_max = 1.0         # Maximum value of c

    GWGO_run(N=N, phase=phase, phi=phi, max_iter=max_iter, lower_bound=lower_bound,
             upper_bound=upper_bound, f=f, l=l, c_min=c_min, c_max=c_max)
