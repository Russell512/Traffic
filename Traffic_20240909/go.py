import numpy as np
import time
import matplotlib.pyplot as plt
import copy

from configuration import *
from solution import Solution
from encoding import encode
from sumo_traci import simulationStart

class GO():
    def __init__(self, N, phase, lower_bound, upper_bound, max_iter, phi, f=0.5, l=1.5, c_min=0.00001, c_max=1.0):
        self.solutions = [Solution(lower_bound, upper_bound, phase) for i in range(N)]
        self.start = time.time()
        self.history = []
        self.N = N
        self.phase = phase
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.max_iter = max_iter
        self.phi = phi
        self.f = f
        self.l = l
        self.c_min = c_min
        self.c_max = c_max
        
    def calculate_c(self, t):
        if t < self.phi * self.max_iter:
            return 2 * (1 - t / self.max_iter)
        else:
            return self.c_max - (self.c_max - self.c_min) * (t / self.max_iter)

    def w(self, r):
        return self.f * np.exp(-r / self.l) - np.exp(-r)

    def Social_Interaction(self, i, si, c):
        xi = np.zeros(self.phase)
        for k in range(self.phase):
            interaction_sum = 0
            for j in range(self.N):
                if i != j:
                    d_ij = np.abs(self.solutions[j].duration[k] - si.duration[k])
                    d_hat_ij = (self.solutions[j].duration[k] - si.duration[k]) / (d_ij + 1e-10)
                    interaction_sum += self.w(d_ij) * d_hat_ij
            xi[k] = c**2 * (self.upper_bound - self.lower_bound) / 2 * interaction_sum
        return xi
    
    def run(self):
        print("Initialization")
        for i, si in enumerate(self.solutions):
            i_sumocfg = encode(i, si.duration)
            simulationStart(HIS_PATH + i_sumocfg, SIM_TIME)
            si.evaluate(i)
        self.solutions = sorted(self.solutions, key = lambda s: s.value)

        for t in range(self.max_iter):
            old_solutions = [copy.deepcopy(solution) for solution in self.solutions]
            print(f"\nIter {t+1:4d}/{self.max_iter}\t Time used: {time.time() - self.start:.2f} sec")

            c = self.calculate_c(t)
            tmp_durations = []
            for i, si in enumerate(self.solutions):
                
                tmp_durations.append(self.Social_Interaction(i, si, c))
            for i in range(self.N):
                self.solutions[i].duration = tmp_durations[i]

            for i, si in enumerate(self.solutions):
                si.duration = [int(round(d)) for d in si.duration]
                for j in range(self.phase):
                    if si.duration[j] < self.lower_bound:
                        si.duration[j] = self.lower_bound
                    elif si.duration[j] > self.upper_bound:
                        si.duration[j] = self.upper_bound
                i_sumocfg = encode(i, si.duration)
                simulationStart(HIS_PATH + i_sumocfg, SIM_TIME)
                si.evaluate(i)
            self.solutions = sorted(self.solutions, key = lambda s: s.value)
            if self.solutions[0].value > old_solutions[0].value:
                self.solutions = old_solutions

            print("\nDuration: ", end="")
            print(self.solutions[0].duration)
            print(f"Current objective value = {self.solutions[0].value:.4f}")
            self.history.append(self.solutions[0].value)
            self.plot_history(self.history)

        return self.solutions[0]
    
    def plot_history(self, history):
        fig, ax = plt.subplots()
        ax.plot(history, 'o-')
        ax.set_xticks(range(0, self.max_iter+1, self.max_iter//10))
        ax.set_xlabel("Iteration")
        ax.set_ylabel("Objective Value")
        ax.set_title(self.name + " History")
        plt.savefig(OPT_PATH + self.name + "_history.png")
    
    def show_result(self, name):
        self.name = name
        print()
        print("################### PROGRAM START ###################")
        print()
        print("*************** GO START ***************")

        opt_solution = self.run()
        self.plot_history(self.history)

        print()
        print("************* GO COMPLETED *************")
        print()
        print("Optimized solution founded:")
        print(opt_solution.duration)
        print(f"Objective value = {opt_solution.value:.4f}")
        print(f"Total time used: {time.time() - self.start:.2f} sec")
        print()
        opt_sumocfg = encode(name, opt_solution.duration)
        print(f"Simulation configuration file '{opt_sumocfg}' has been generated.")
        print()
        print("################## PROGRAM END ##################")
        print()
        return self.history

if __name__ == '__main__':
    N = 5
    lower_bound = 5
    upper_bound = 60
    max_iter = 3
    phi = 0.25

    go = GO(N, PHASE, lower_bound, upper_bound, max_iter, phi, f=0.5, l=1.5, c_min=0.00001, c_max=1.0)
    history = go.show_result('GO')