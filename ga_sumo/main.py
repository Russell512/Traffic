import numpy as np
import time

from configuration import *

from evaluate import ObjectValue
from encoding import encode
from sumo_traci import simulationStart

class Solution:
    def __init__(self, lower_bound, upper_bound, phase):
        self.duration = np.random.randint(lower_bound, upper_bound + 1, size=phase)
        self.value = 0

    def evaluate(self, i):
        add_path = HIS_PATH + str(i) + ".add.xml"
        tripinfo_path = HIS_PATH + str(i) + ".tripinfo.xml"
        fcd_path = HIS_PATH + str(i) + ".fcd.xml"          
        obj = ObjectValue(add_path, tripinfo_path, fcd_path)
        self.value = obj.evaluate()


def D2B(decimal, B):
    """
    Decimal(10) to Binary(2):
    eg. D2B(15, 6) returns [0, 0, 1, 1, 1, 1]
    """
    bin = []
    while B > 0:
        base = 2 ** (B-1)
        if decimal >= base:
            bin.append(1)
        else:
            bin.append(0)
        decimal %= base
        B -= 1
    return bin

def B2D(bin):
    """
    Binary(2) to Decimal(10):
    eg. B2D([0, 1, 0, 0, 0, 1]) returns 17
    """
    dec = 0
    for bit in range(len(bin)):
        dec += bin[bit]
        dec *= 2
    return dec // 2

def crossover(parent1, parent2, cr, mr):
    """
    Pass in 2 parent, cr(crossover rate), and mr(mutation rate),
    returns a child
    """
    child = []
    for i in range(len(parent1)):
        f = np.random.rand()
        if f <= cr:
            cross_pos = np.random.randint(len(parent1[i]))
            child.append((parent1[i][:cross_pos] + parent2[i][cross_pos:]))
        else:
            child.append(parent1[i])
    return mutation(child, mr)

def mutation(child, mr):
    """
    Pass in a child and mr(mutation rate),
    returns a possibly mutant
    """
    for i in range(len(child)):
        f = np.random.rand()
        if f <= mr:
            mutation_pos = np.random.randint(len(child[i]))
            child[i][mutation_pos] = 1 if child[i][mutation_pos] == 0 else 0
    return child


def GA(N, phase, B, n, cr, mr, max_iter, lower_bound, upper_bound):
    solutions = [Solution(lower_bound, upper_bound, phase) for i in range(N)]
    start = time.time()

    print("Initialization")
    for i, si in enumerate(solutions):
        sumocfg_path = encode(ADD_XML, SUMOCFG, i, si.duration)
        simulationStart(HIS_PATH + sumocfg_path, SIM_TIME)
        si.evaluate(i)
        si.duration = [D2B(dur, B) for dur in si.duration]      # D -> B
    solutions = sorted(solutions, key = lambda si: si.value)

    for t in range(max_iter):
        print(f"\nIter {t+1:4d}/{max_iter}\t Time used: {time.time() - start:.2f} sec")

        parents = solutions[:n].copy()
        childs = []
        for i in range(N - n):
            parent1 = parents[np.random.randint(n)]
            parent2 = parents[np.random.randint(n)]
            child = Solution(lower_bound, upper_bound, phase)
            child.duration = crossover(parent1.duration, parent2.duration, cr, mr)
            childs.append(child)
        
        solutions = parents + childs
        
        for i, si in enumerate(solutions):
            si.duration = [B2D(dur) for dur in si.duration]     # B -> D
            for j in range(phase):
                if si.duration[j] < lower_bound:
                    si.duration[j] = lower_bound
                elif si.duration[j] > upper_bound:
                    si.duration[j] = upper_bound
            sumocfg_path = encode(ADD_XML, SUMOCFG, i, si.duration)
            simulationStart(HIS_PATH + sumocfg_path, SIM_TIME)
            si.evaluate(i)
            si.duration = [D2B(dur, B) for dur in si.duration]  # D -> B
        solutions = sorted(solutions, key = lambda si: si.value)
        
        print("\nDuration: [ ", end="")
        for i in solutions[0].duration:
            print(B2D(i), end=" ")
        print("]")
        print(f"Current objective value = {solutions[0].value:.4f}")

    best_solution = solutions[0]
    best_solution.duration = [B2D(dur) for dur in best_solution.duration]   # B -> D
    for j in range(phase):
        if best_solution.duration[j] < lower_bound:
            best_solution.duration[j] = lower_bound
        elif best_solution.duration[j] > upper_bound:
            best_solution.duration[j] = upper_bound
    return best_solution

def GA_run(N=10, phase=6, B=6, n=4, cr=0.9, mr=0.15, max_iter=1000, lower_bound=5, upper_bound=60):
    print()
    print("################### PROGRAM START ###################")
    print()
    start = time.time()
    print("*************** GA START ***************")

    best_solution = GA(N=N, phase=phase, B=B, n=n, cr=cr, mr=mr, max_iter=max_iter, lower_bound=lower_bound, upper_bound=upper_bound)

    print()
    print("************* GA COMPLETED *************")
    print()
    print("==========SETTINGS==========")
    print(f"Number of solutions N = {N}")
    print(f"Total phases = {phase}")
    print(f"Lower bound = {lower_bound}")
    print(f"Upper bound = {upper_bound}")
    print(f"Crossover rate = {cr}")
    print(f"Mutate rate = {mr}")
    print("============================")
    print()
    print("Best solution founded:")
    print(best_solution.duration)
    print(f"Objective value = {best_solution.value:.4f}")
    print(f"Total time used: {time.time() - start:.2f} sec")
    print()
    sumocfg_path = encode(ADD_XML, SUMOCFG, 'optimal', best_solution.duration)
    print(f"Simulation configuration file '{sumocfg_path}' has been generated.")
    print()
    print("################## PROGRAM END ##################")
    print()

if __name__ == '__main__':
    GA_run(N=5, phase=6, B=6, n=4, cr=0.9, mr=0.15, max_iter=10, lower_bound=5, upper_bound=60)