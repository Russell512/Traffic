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


def calculate_temperature(t, max_iter, min_temp, max_temp):
    """
    Calculate the temperature based on the current iteration
    """
    return max_temp * (1 - t / max_iter) if t < max_iter else min_temp


def SA(N, phase, max_iter=7500, lower_bound=5, upper_bound=60, max_temp=1.0, min_temp=0.00001):
    # 1: Initialization
    solutions = [Solution(lower_bound, upper_bound, phase) for _ in range(N)]
    start = time.time()
    history = []

    print("Initialization")
    for i, si in enumerate(solutions):
        sumocfg_path = encode(ADD_XML, SUMOCFG, i, si.duration)
        simulationStart(HIS_PATH + sumocfg_path, SIM_TIME)
        si.evaluate(i)

    solutions = sorted(solutions, key=lambda s: s.value)
    best_solution = solutions[0]

    # Iterations start
    for t in range(max_iter):
        print(
            f"\nIter {t + 1:4d}/{max_iter}\t Time used: {time.time() - start:.2f} sec")

        current_solution = solutions[np.random.randint(N)]
        new_solution = Solution(lower_bound, upper_bound, phase)
        new_solution.duration = current_solution.duration.copy()

        # Randomly modify 5 phases
        indices = np.random.choice(phase, 5, replace=False)
        for i in indices:
            new_solution.duration[i] = np.random.randint(
                lower_bound, upper_bound + 1)

        # Evaluate the new solution
        new_solution.duration = [int(round(num))
                                 for num in new_solution.duration]
        new_solution.duration = np.clip(
            new_solution.duration, lower_bound, upper_bound)

        sumocfg_path = encode(ADD_XML, SUMOCFG, 'temp', new_solution.duration)
        simulationStart(HIS_PATH + sumocfg_path, SIM_TIME)
        new_solution.evaluate('temp')

        # Acceptance criteria
        delta = new_solution.value - current_solution.value
        temperature = calculate_temperature(t, max_iter, min_temp, max_temp)

        if delta < 0 or np.random.rand() < np.exp(-delta / temperature):
            # Accept the new solution
            solutions[solutions.index(current_solution)] = new_solution

            # Update best solution found
            if new_solution.value < best_solution.value:
                best_solution = new_solution

        print("\nCurrent Best Duration: ", end="")
        print(best_solution.duration)
        print(f"Current objective value = {best_solution.value:.4f}")
        history.append(best_solution.value)

    return best_solution, history


def GWGO_run(N, phase, max_iter=7500, lower_bound=5, upper_bound=60, max_temp=1.0, min_temp=0.00001):
    print()
    print("################### PROGRAM START ###################")
    print()
    start = time.time()
    print("*************** SA START ***************")

    best_solution, history = SA(N=N, phase=phase, max_iter=max_iter, lower_bound=lower_bound,
                                upper_bound=upper_bound, max_temp=max_temp, min_temp=min_temp)
    plt.plot(history)
    plt.savefig("history.png")

    print()
    print("************* SA COMPLETED *************")
    print()
    print("==========SETTINGS==========")
    print(f"Number of solutions N = {N}")
    print(f"Total phases = {phase}")
    print(f"Lower bound = {lower_bound}")
    print(f"Upper bound = {upper_bound}")
    print(f"Max temperature = {max_temp}")
    print(f"Min temperature = {min_temp}")
    print("============================")
    print()
    print("Best solution found:")
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
    phase = PHASE       # Number of phases a solution has
    max_iter = 300     # Total iterations
    lower_bound = 5     # Min time of each phase
    upper_bound = 60    # Max time of each phase
    max_temp = 1.0     # Maximum temperature
    min_temp = 0.00001  # Minimum temperature

    GWGO_run(N=N, phase=phase, max_iter=max_iter, lower_bound=lower_bound,
             upper_bound=upper_bound, max_temp=max_temp, min_temp=min_temp)
