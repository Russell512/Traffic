import numpy as np
import time

from configuration import *

from evaluate import ObjectValue
from encoding import encode_add_xml, encode_sumocfg
from sumo_traci import simulationStart


class Solution:
    def __init__(self, lower_bound, upper_bound, phase):
        self.duration = np.random.uniform(lower_bound, upper_bound, phase)
        self.duration = [int(round(dur)) for dur in self.duration]
        self.value = 0

    def evaluate(self, add_path, sumocfg_path, i):
        tripinfo_path = str(i) + ".tripinfo.xml"
        fcd_path = str(i) + ".fcd.xml"
        obj = ObjectValue(NET_XML, ROU_XML, add_path, sumocfg_path, tripinfo_path, fcd_path)
        self.value = obj.evaluate()

def SA(phase, lower_bound, upper_bound, max_temp, min_temp, alpha, max_iter):
    # Initialize solution
    current_solution = Solution(lower_bound, upper_bound, phase)
    add_path = encode_add_xml(ADD_XML, "initial", current_solution.duration)
    sumocfg_path = encode_sumocfg(SUMOCFG, "initial", add_path)
    simulationStart(sumocfg_path, SIM_TIME)
    current_solution.evaluate(add_path, sumocfg_path, "initial")
    
    best_solution = current_solution
    temperature = max_temp

    start = time.time()
    for t in range(max_iter):
        print(f"\nIter {t+1:4d}/{max_iter}\t Time used: {time.time() - start:.2f} sec")

        # Generate new candidate solution by modifying current solution
        new_solution = Solution(lower_bound, upper_bound, phase)
        new_solution.duration = current_solution.duration.copy()
        i = np.random.randint(phase)
        new_solution.duration[i] = np.random.randint(lower_bound, upper_bound)

        # Evaluate the new candidate solution
        add_path = encode_add_xml(ADD_XML, t, new_solution.duration)
        sumocfg_path = encode_sumocfg(SUMOCFG, t, add_path)
        simulationStart(sumocfg_path, SIM_TIME)
        new_solution.evaluate(add_path, sumocfg_path, t)

        # Acceptance criterion
        delta = new_solution.value - current_solution.value
        if delta > 0 or np.random.rand() < np.exp(delta / temperature):
            current_solution = new_solution
            if current_solution.value > best_solution.value:
                best_solution = current_solution

        # Update temperature
        temperature *= alpha

        # Print current best duration and value
        print("\nDuration: [ ", end="")
        for dur in best_solution.duration:
            print(dur, end=" ")
        print("]")
        print(f"Current objective value = {best_solution.value:.4f}")

    return best_solution

def main(phase=6, lower_bound=5, upper_bound=60, max_temp=1.0, min_temp=0.00001, alpha=0.9, max_iter=1000):
    print()
    print("################### PROGRAM START ###################")
    print()
    start = time.time()
    print("*************** SA START ***************")

    best_solution = SA(phase=phase, lower_bound=lower_bound, upper_bound=upper_bound, 
                       max_temp=max_temp, min_temp=min_temp, alpha=alpha, max_iter=max_iter)

    print()
    print("************* SA COMPLETED *************")
    print()
    print("==========SETTINGS==========")
    print(f"Total phases = {phase}")
    print(f"Lower bound = {lower_bound}")
    print(f"Upper bound = {upper_bound}")
    print(f"Max temperature = {max_temp}")
    print(f"Min temperature = {min_temp}")
    print(f"Cooling rate (alpha) = {alpha}")
    print("============================")
    print()
    print("Best solution found:")
    print(best_solution.duration)
    print(f"Objective value = {best_solution.value:.4f}")
    print(f"Total time used: {time.time() - start:.2f} sec")
    print()
    add_path = encode_add_xml(ADD_XML, 'optimal', best_solution.duration)
    sumocfg_path = encode_sumocfg(SUMOCFG, 'optimal', add_path)
    print(f"Simulation configuration file '{sumocfg_path}' has been generated.")
    print()
    print("################## PROGRAM END ##################")
    print()

if __name__ == '__main__':
    main(phase=6, lower_bound=5, upper_bound=60, max_temp=1.0, min_temp=0.00001, alpha=0.9, max_iter=1000)
